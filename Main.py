# ================================================================
#  weys — Raspberry Pi Pico W
#  Full script: WiFi server + USB HID keyboard + 1.8" TFT display
#
#  TFT wiring:
#    VCC  -> 3.3V  (pin 36)
#    GND  -> GND   (pin 38)
#    SCK  -> GP10  (pin 14)
#    MOSI -> GP11  (pin 15)
#    CS   -> GP9   (pin 12)
#    DC   -> GP8   (pin 11)
#    RST  -> GP12  (pin 16)
#    BL   -> 3.3V  (backlight always on)
#
#  Libraries needed in Pico W root:
#    ST7735.py and sysfont.py
#    (see File 2 and File 3 below)
# ================================================================

import wifi
import socketpool
import json
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from machine import Pin, SPI
from ST7735 import TFT
from sysfont import sysfont

# ── CHANGE THESE ────────────────────────────────────────────────
WIFI_SSID     = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
SERVER_PORT   = 5000
# ────────────────────────────────────────────────────────────────

def rgb(r, g, b):
    return TFT.color(r, g, b)

BLACK  = TFT.BLACK
WHITE  = TFT.WHITE
DARK   = rgb(13,  17,  23)
CARD   = rgb(22,  27,  34)
PANEL  = rgb(33,  38,  45)
LGRAY  = rgb(48,  54,  61)
GRAY   = rgb(139, 148, 158)
BLUE   = rgb(37,  99,  235)
LBLUE  = rgb(96,  165, 250)
GREEN  = rgb(74,  222, 128)
DGREEN = rgb(22,  163,  74)
AMBER  = rgb(217, 119,   6)
YELLOW = rgb(251, 188,   4)
RED    = rgb(220,  38,  38)
ORANGE = rgb(234,  67,  53)
PURPLE = rgb(124, 108, 252)
TEAL   = rgb(16,  163, 127)

LANG_COLORS = {
    "COBOL":      (AMBER,  DARK),
    "JCL":        (RED,    WHITE),
    "Java":       (BLUE,   WHITE),
    "Python":     (LBLUE,  DARK),
    "C++":        (PURPLE, WHITE),
    "JavaScript": (YELLOW, DARK),
    "Kotlin":     (PURPLE, WHITE),
    "Go":         (LBLUE,  DARK),
    "TypeScript": (BLUE,   WHITE),
    "Rust":       (ORANGE, WHITE),
}

PROVIDER_COLORS = {
    "gemini":     (BLUE,   WHITE),
    "openai":     (TEAL,   WHITE),
    "claude":     (AMBER,  DARK),
    "groq":       (RED,    WHITE),
    "openrouter": (PURPLE, WHITE),
    "custom":     (PANEL,  GRAY),
}

print("Initialising TFT display...")
_spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
           sck=Pin(10), mosi=Pin(11), miso=None)
tft  = TFT(_spi, dc=Pin(8), rst=Pin(12), cs=Pin(9))
tft.initr()
tft.rgb(True)
tft.rotation(1)
print("TFT OK")

def d_fill(x, y, w, h, color):
    tft.fillrect((x, y), (w, h), color)

def d_text(string, x, y, color, scale=1):
    tft.text((x, y), str(string), color, sysfont, scale)

def d_hline(x1, x2, y, color):
    tft.line((x1, y), (x2, y), color)

def d_circle(cx, cy, r, color):
    tft.fillcircle((cx, cy), r, color)

def d_rect(x, y, w, h, color):
    tft.rect((x, y), (w, h), color)

def d_badge(x, y, w, h, label, bg, fg, scale=1):
    d_fill(x, y, w, h, bg)
    char_w = 6 * scale
    tx = x + max(2, (w - len(label) * char_w) // 2)
    ty = y + max(1, (h - 8 * scale) // 2)
    d_text(label, tx, ty, fg, scale)

def d_progress_bar(x, y, w, h, pct, bg, fg):
    d_fill(x, y, w, h, bg)
    if pct > 0:
        fw = max(1, int((w - 2) * min(pct, 1.0)))
        d_fill(x + 1, y + 1, fw, h - 2, fg)

def draw_w_logo(ox, oy, scale, color):
    pts = [
        (0,0),(1,0),(2,0),(3,0),(4,0),
        (0,1),                  (4,1),
        (0,2),      (2,2),      (4,2),
              (1,3),      (3,3),
              (1,4),      (3,4),
    ]
    for col, row in pts:
        d_fill(ox + col * scale, oy + row * scale, scale, scale, color)

def screen_splash():
    tft.fill(DARK)
    for i in range(5):
        d_rect(80 - 28 - i * 8, 44 - 28 - i * 8,
               56 + i * 16, 56 + i * 16, PANEL)
    SCALE = 7
    lx = (160 - 5 * SCALE) // 2
    ly = 10
    draw_w_logo(lx, ly, SCALE, WHITE)
    d_text("weys", 62, ly + 5 * SCALE + 6, WHITE, 2)
    d_hline(20, 140, ly + 5 * SCALE + 20, BLUE)
    d_text("AI  Pico W  USB", 22, ly + 5 * SCALE + 26, GRAY, 1)
    d_text("v1.0", 68, 118, LBLUE, 1)

def screen_connecting():
    tft.fill(DARK)
    d_fill(0, 0, 160, 22, CARD)
    draw_w_logo(6, 4, 4, LBLUE)
    d_text("weys", 36, 6, WHITE, 2)
    d_hline(0, 160, 22, LGRAY)
    d_text("Connecting to WiFi", 6, 34, GRAY, 1)
    d_text(WIFI_SSID[:22], 6, 48, LBLUE, 1)
    for i in range(3):
        d_circle(52 + i * 22, 82, 7, BLUE)
    d_text("Please wait...", 28, 106, GRAY, 1)

def screen_error(msg):
    tft.fill(DARK)
    d_fill(0, 0, 160, 22, RED)
    d_text("weys ERROR", 10, 6, WHITE, 2)
    d_hline(0, 160, 22, LGRAY)
    d_text("Could not start:", 6, 34, RED, 1)
    words = str(msg).split()
    line, y = "", 50
    for word in words:
        if len(line + word) * 6 < 150:
            line += word + " "
        else:
            d_text(line.strip(), 6, y, GRAY, 1)
            y += 14
            line = word + " "
    if line:
        d_text(line.strip(), 6, y, GRAY, 1)
    d_text("Power cycle to retry", 2, 114, LGRAY, 1)

def screen_ready(ip, lang="COBOL", provider="gemini"):
    tft.fill(DARK)
    d_fill(0, 0, 160, 22, CARD)
    draw_w_logo(6, 3, 4, LBLUE)
    d_text("weys", 36, 6, WHITE, 2)
    d_circle(150, 9, 6, DGREEN)
    d_circle(150, 9, 4, GREEN)
    d_hline(0, 160, 22, LGRAY)
    d_text("IP ADDRESS", 8, 28, GRAY, 1)
    d_text(ip, 8, 40, LBLUE, 2)
    d_hline(8, 152, 60, LGRAY)
    d_text("LANGUAGE", 8, 66, GRAY, 1)
    lbg, lfg = LANG_COLORS.get(lang, (BLUE, WHITE))
    lw = min(len(lang) * 6 + 12, 72)
    d_badge(8, 76, lw, 14, lang, lbg, lfg, 1)
    d_text("PROVIDER", 88, 66, GRAY, 1)
    pbg, pfg = PROVIDER_COLORS.get(provider.lower(), (PANEL, GRAY))
    pname = provider.capitalize()[:8]
    pw = min(len(pname) * 6 + 12, 66)
    d_badge(88, 76, pw, 14, pname, pbg, pfg, 1)
    d_hline(8, 152, 96, LGRAY)
    d_text("STATUS", 8, 102, GRAY, 1)
    d_text("Ready to type...", 8, 114, GREEN, 1)

def screen_typing(typed, total, lang="COBOL",
                  provider="gemini", delay_ms=50):
    tft.fill(DARK)
    d_fill(0, 0, 160, 22, CARD)
    d_text("weys", 6, 6, LBLUE, 2)
    lbg, lfg = LANG_COLORS.get(lang, (BLUE, WHITE))
    lw = min(len(lang) * 6 + 8, 64)
    d_badge(160 - lw - 4, 3, lw, 16, lang, lbg, lfg, 1)
    d_hline(0, 160, 22, LGRAY)
    d_text("TYPING IN PROGRESS", 6, 29, GRAY, 1)
    pct = typed / total if total > 0 else 0
    pct_str = str(int(pct * 100)) + "%"
    d_text(pct_str, 150 - len(pct_str) * 6, 29, LBLUE, 1)
    d_progress_bar(6, 39, 148, 14, pct, PANEL, BLUE)
    d_hline(6, 154, 59, LGRAY)
    d_text("CHARS", 6, 66, GRAY, 1)
    count_str = str(typed) + "/" + str(total)
    d_text(count_str, 6, 76, WHITE, 2)
    d_text("DELAY", 100, 66, GRAY, 1)
    d_text(str(delay_ms) + "ms", 100, 76, GREEN, 2)
    d_hline(6, 154, 96, LGRAY)
    pbg, pfg = PROVIDER_COLORS.get(provider.lower(), (PANEL, GRAY))
    pname = provider.capitalize()[:8]
    pw = min(len(pname) * 6 + 10, 68)
    d_badge(6, 104, pw, 14, pname, pbg, pfg, 1)
    d_circle(148, 111, 5, GREEN)
    d_text("WiFi", 128, 107, GRAY, 1)

def screen_done(total, lang="COBOL", provider="gemini"):
    tft.fill(DARK)
    d_fill(0, 0, 160, 22, CARD)
    d_text("weys", 6, 6, LBLUE, 2)
    d_badge(96, 3, 58, 16, " DONE! ", DGREEN, WHITE, 1)
    d_hline(0, 160, 22, LGRAY)
    d_circle(80, 64, 30, DGREEN)
    d_circle(80, 64, 26, GREEN)
    d_fill(76, 58, 4, 18, DGREEN)
    d_fill(68, 70, 16, 4, DGREEN)
    d_text("OK", 70, 57, DGREEN, 2)
    summary = str(total) + " chars typed"
    sx = (160 - len(summary) * 6) // 2
    d_text(summary, sx, 102, GREEN, 1)
    lbg, lfg = LANG_COLORS.get(lang, (BLUE, WHITE))
    lw = min(len(lang) * 6 + 10, 52)
    d_badge(6, 114, lw, 12, lang, lbg, lfg, 1)
    pbg, pfg = PROVIDER_COLORS.get(provider.lower(), (PANEL, GRAY))
    pname = provider.capitalize()[:8]
    pw = min(len(pname) * 6 + 10, 66)
    d_badge(lw + 10, 114, pw, 12, pname, pbg, pfg, 1)

kbd    = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
print("USB HID keyboard ready")

UPDATE_EVERY = 25

def type_code(text, delay_ms=50, lang="COBOL",
              provider="gemini", total_chars=None):
    total = total_chars or len(text)
    delay = max(0.01, delay_ms / 1000)
    typed = 0
    for char in text:
        try:
            layout.write(char)
            typed += 1
        except ValueError:
            print("Skip: " + repr(char))
        except Exception as e:
            print("Type error: " + repr(char) + " " + str(e))
        if typed % UPDATE_EVERY == 0:
            screen_typing(typed, total, lang, provider, delay_ms)
        time.sleep(delay)
    screen_typing(typed, total, lang, provider, delay_ms)
    return typed

def http_response(conn, status="200 OK", body="{}"):
    body_bytes = body.encode("utf-8")
    response = (
        "HTTP/1.1 " + status + "\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: " + str(len(body_bytes)) + "\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8") + body_bytes
    try:
        conn.sendall(response)
    except Exception as e:
        print("Send error: " + str(e))

def handle_request(conn, server_ip, cur_lang, cur_provider):
    try:
        buf  = bytearray(8192)
        size = conn.recv_into(buf)
        if not size:
            return cur_lang, cur_provider
        raw   = buf[:size].decode("utf-8", errors="replace")
        first = raw.split("\r\n")[0]
        parts = first.split(" ")
        if len(parts) < 2:
            return cur_lang, cur_provider
        method = parts[0]
        path   = parts[1]
        print("  " + method + " " + path)

        if method == "OPTIONS":
            http_response(conn, "200 OK", '{"ok":true}')
            return cur_lang, cur_provider

        if method == "GET" and path == "/ping":
            http_response(conn, "200 OK", json.dumps({
                "status":   "ok",
                "ip":       server_ip,
                "lang":     cur_lang,
                "provider": cur_provider,
            }))
            return cur_lang, cur_provider

        if method == "POST" and path == "/type":
            sep = raw.find("\r\n\r\n")
            if sep == -1:
                http_response(conn, "400 Bad Request", '{"error":"no body"}')
                return cur_lang, cur_provider
            body_str = raw[sep + 4:].strip()
            if not body_str:
                http_response(conn, "400 Bad Request", '{"error":"empty body"}')
                return cur_lang, cur_provider
            try:
                data = json.loads(body_str)
            except Exception:
                http_response(conn, "400 Bad Request", '{"error":"invalid JSON"}')
                return cur_lang, cur_provider

            text     = data.get("text", "").strip()
            delay_ms = int(data.get("delay", 50))
            lang     = data.get("lang",     cur_lang)
            provider = data.get("provider", cur_provider)

            if not text:
                http_response(conn, "400 Bad Request", '{"error":"no text"}')
                return cur_lang, cur_provider

            total = len(text)
            print("  Received " + str(total) + " chars")

            http_response(conn, "200 OK", json.dumps({
                "status":   "typing",
                "chars":    total,
                "delay_ms": delay_ms,
                "lang":     lang,
                "provider": provider,
            }))
            conn.close()

            screen_typing(0, total, lang, provider, delay_ms)
            print("  Waiting 1.5s — switch to your editor!")
            time.sleep(1.5)

            typed = type_code(text, delay_ms, lang, provider, total)
            print("  Done! Typed " + str(typed) + "/" + str(total))

            screen_done(typed, lang, provider)
            time.sleep(3)

            screen_ready(server_ip, lang, provider)
            return lang, provider

        http_response(conn, "404 Not Found", '{"error":"not found"}')
        return cur_lang, cur_provider

    except Exception as e:
        print("  Handler error: " + str(e))
        try:
            http_response(conn, "500 Internal Server Error",
                          json.dumps({"error": str(e)}))
        except Exception:
            pass
        return cur_lang, cur_provider

def main():
    cur_lang     = "COBOL"
    cur_provider = "gemini"

    print("=" * 44)
    print("  weys - Raspberry Pi Pico W")
    print("=" * 44)

    screen_splash()
    time.sleep(2)
    screen_connecting()
    print("Connecting to WiFi: " + WIFI_SSID)

    try:
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
        ip = str(wifi.radio.ipv4_address)
        print("Connected!  IP: " + ip)
        print("")
        print(">>> In the mobile app, set Pico IP to: " + ip + " <<<")
        print("")
    except Exception as e:
        print("WiFi error: " + str(e))
        screen_error(str(e))
        while True:
            time.sleep(1)

    screen_ready(ip, cur_lang, cur_provider)

    pool   = socketpool.SocketPool(wifi.radio)
    server = pool.socket()
    server.setsockopt(socketpool.Socket.SOL_SOCKET,
                      socketpool.Socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", SERVER_PORT))
    server.listen(2)
    server.setblocking(False)

    print("Server running on port " + str(SERVER_PORT))
    print("Waiting for commands from the weys mobile app...")
    print("-" * 44)

    while True:
        try:
            conn, addr = server.accept()
            conn.setblocking(True)
            conn.settimeout(5)
            print("Connection from " + addr[0])
            cur_lang, cur_provider = handle_request(
                conn, ip, cur_lang, cur_provider
            )
            try:
                conn.close()
            except Exception:
                pass
        except OSError:
            pass
        time.sleep(0.01)

main()