# Code Typer

A hardware + software project that lets you describe code on your phone, generate it using an AI API, and have it automatically typed on your PC via a Raspberry Pi Pico W acting as a USB keyboard — no copy-pasting, no switching windows manually.

Primary use case: **COBOL and JCL** code generation, with support for Java, Python, C++, JavaScript, Kotlin, Go, TypeScript, and Rust.

---

## How It Works

```
📱 Mobile App (browser)
      │
      │  HTTP — home WiFi
      ▼
🤖 AI API (Gemini / OpenAI / Claude / Groq / OpenRouter)
      │
      │  generated code (text only)
      ▼
📱 Mobile App sends code
      │
      │  HTTP POST — home WiFi
      ▼
🖥️  Raspberry Pi Pico W  (main.py)
      │
      │  USB HID — acts as a keyboard
      ▼
💻  Your PC — code is typed automatically
```

1. You type a prompt on your phone: *"write a COBOL program to add two numbers"*
2. The app calls the AI API — gets back **only the raw code**, no explanation
3. You tap **Type it on PC** — the app sends the code to the Pico W over WiFi
4. The Pico W types every character into your PC via USB, as if you typed it yourself

---

## Hardware Requirements

| Part | Notes |
|------|-------|
| Raspberry Pi Pico W | Must be the **W** model (has built-in WiFi). Pico 2 W also works. |
| USB cable | Micro-USB for Pico, connects to your PC |
| Your phone | Any phone with a browser — iOS or Android |
| Your PC | Any OS — the Pico appears as a standard USB keyboard |

---

## Software Requirements

### On the Pico W

- **CircuitPython** firmware for Pico W
  - Download: https://circuitpython.org/board/raspberry_pi_pico_w/
- **adafruit_hid** library
  - Download: https://github.com/adafruit/Adafruit_CircuitPython_HID
  - Copy the `adafruit_hid` folder into `/lib` on the Pico W

### On your phone

- Any modern mobile browser (Chrome, Safari, Firefox)
- An API key from at least one AI provider (see AI Providers section)

### No installation needed

The mobile app (`mobile_app.html`) is a single HTML file — open it directly in your phone browser or serve it from any static file host.

---

## Project Files

```
code-typer/
├── mobile_app.html   — Mobile web app (runs in phone browser)
├── main.py           — CircuitPython code for Raspberry Pi Pico W
└── README.md         — This file
```

---

## Setup Guide

### Step 1 — Flash CircuitPython on Pico W

1. Hold the **BOOTSEL** button on your Pico W
2. While holding, plug it into your PC via USB
3. It appears as a USB drive called `RPI-RP2`
4. Download the CircuitPython `.uf2` file for Pico W from https://circuitpython.org/board/raspberry_pi_pico_w/
5. Drag and drop the `.uf2` file onto the `RPI-RP2` drive
6. The Pico W reboots automatically and now appears as `CIRCUITPY`

### Step 2 — Install the HID library

1. Download the CircuitPython library bundle from https://circuitpython.org/libraries
2. Inside the bundle, find the `adafruit_hid` folder
3. Copy the entire `adafruit_hid` folder into the `/lib` folder on your `CIRCUITPY` drive

### Step 3 — Configure and copy main.py

Open `main.py` and edit these two lines:

```python
WIFI_SSID     = "YOUR_WIFI_NAME"       # your home WiFi name
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"   # your home WiFi password
```

Then copy `main.py` to the root of your `CIRCUITPY` drive (not inside any folder).

### Step 4 — Get the Pico W IP address

1. Open **Thonny** (free Python IDE) or any serial monitor
2. Connect to the Pico W serial port
3. You will see output like:

```
========================================
  Code Typer — Pico W
========================================
Keyboard HID ready
Connecting to WiFi: YourWiFiName
Connected! IP address: 192.168.1.42

>>> In the mobile app, set Pico IP to: 192.168.1.42 <<<

Server listening on port 5000
Waiting for commands from mobile app...
```

4. Note the IP address — you will enter it in the mobile app

### Step 5 — Open the mobile app

Open `mobile_app.html` in your phone's browser. You can:
- Transfer it to your phone and open it as a local file
- Serve it from a simple local web server (`python3 -m http.server`)
- Host it on any static file hosting service

### Step 6 — Configure the mobile app

Tap the **status pill** in the top right corner to open settings:

1. **AI Provider** — tap your provider or paste your key (auto-detects)
2. **API Key** — paste your key
3. **Model** — leave as default or change to your preferred model
4. **Pico W IP** — enter the IP from Step 4 (e.g. `192.168.1.42`)
5. **Typing delay** — how fast characters are typed (10–200ms, default 50ms)
6. Tap **Save & Connect**

The status pill turns green when the Pico W is reachable.

### Step 7 — Use it

1. Pick your language (COBOL, JCL, Java, etc.)
2. Type your prompt
3. Tap **Generate** — the AI writes the code
4. Review the code in the preview
5. Click into your editor or terminal on your PC
6. Tap **Type it on PC** — the Pico W types the code automatically

---

## AI Providers

The app supports multiple AI providers. Paste your key and it auto-detects the provider from the key format.

| Provider | Key Format | Free Tier | Get Key |
|----------|-----------|-----------|---------|
| **Gemini** | `AIza...` | ✅ 1,500 req/day, no credit card | aistudio.google.com |
| **Groq** | `gsk_...` | ✅ 30 req/min, no credit card | console.groq.com |
| **OpenRouter** | `sk-or-...` | ✅ 35+ free models | openrouter.ai |
| **OpenAI** | `sk-...` | ❌ Paid | platform.openai.com |
| **Claude** | `sk-ant-...` | ❌ Paid | console.anthropic.com |
| **Custom** | Any | Depends | Your own OpenAI-compatible API |

**Recommended for this project:** Gemini (most generous free tier) or Groq (fastest).

### Default models per provider

| Provider | Default Model | Alternatives |
|----------|--------------|--------------|
| Gemini | `gemini-2.0-flash` | `gemini-2.5-flash-preview-05-20`, `gemini-1.5-flash` |
| Groq | `llama-3.3-70b-versatile` | `llama-3.1-8b-instant`, `mixtral-8x7b-32768` |
| OpenRouter | `meta-llama/llama-3.3-70b-instruct:free` | Any model with `:free` suffix |
| OpenAI | `gpt-4o-mini` | `gpt-4o`, `gpt-4-turbo` |
| Claude | `claude-sonnet-4-20250514` | `claude-haiku-4-5-20251001` |
| Custom | *(you set it)* | Any OpenAI-compatible endpoint |

---

## Supported Languages

| Language | Priority | Notes |
|----------|----------|-------|
| **COBOL** | ⭐ Primary | Proper division structure, column-aware formatting |
| **JCL** | ⭐ Primary | IBM JCL syntax, `//` notation, JOB/EXEC/DD statements |
| Java | Standard | Complete class with main method |
| Python | Standard | Ready to run |
| C++ | Standard | With includes and main function |
| JavaScript | Standard | Clean JS |
| Kotlin | Standard | With main function |
| Go | Standard | With package main |
| TypeScript | Standard | Complete TS |
| Rust | Standard | With fn main() |

---

## API Reference — Pico W HTTP Server

The Pico W runs a simple HTTP server on port 5000. The mobile app communicates with it over your home WiFi.

### GET /ping

Health check. Returns `200 OK` if the Pico W is running.

**Response:**
```json
{ "status": "ok", "ip": "192.168.1.42" }
```

### POST /type

Sends text to be typed via USB HID.

**Request body:**
```json
{
  "text": "IDENTIFICATION DIVISION.\nPROGRAM-ID. HELLO.",
  "delay": 50
}
```

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | The code to type |
| `delay` | integer | Milliseconds between each character (10–200) |

**Response:**
```json
{ "status": "typing", "chars": 42, "delay_ms": 50 }
```

The Pico W responds immediately, then waits 1.5 seconds before typing begins — giving you time to click into your editor.

---

## Code Reference

### mobile_app.html

Single-file mobile web app. No build step, no dependencies, no framework.

#### Provider system

Each AI provider is defined as an object in the `PROVIDERS` map:

```javascript
const PROVIDERS = {
  gemini: {
    name: 'Gemini',
    defaultModel: 'gemini-2.0-flash',
    keyPrefix: 'AIza',                    // used for auto-detection
    getUrl: (model, key) => `...`,        // builds the API endpoint URL
    buildBody: (system, prompt, model) => ({ ... }),  // builds request body
    getHeaders: key => ({ ... }),         // builds auth headers
    extractCode: data => data.candidates[0].content.parts[0].text,
  },
  openai: { ... },
  claude: { ... },
  groq: { ... },
  openrouter: { ... },
  custom: { ... }
};
```

To add a new provider, add a new entry to `PROVIDERS` following the same shape.

#### Auto-detection

When you paste an API key, `autoDetectProvider()` checks the key prefix against each provider's `keyPrefix` field and switches the active provider automatically:

```
AIza...    → Gemini
sk-...     → OpenAI
sk-ant-... → Claude
gsk_...    → Groq
sk-or-...  → OpenRouter
```

#### Language hints

Each language has a system prompt hint in `LANG_HINTS` that tells the AI about formatting rules specific to that language. For example, COBOL's hint enforces proper division structure and column-awareness.

#### Settings storage

Settings are saved to `localStorage` under the key `codetyper_v3`. This means your API key, IP address, and preferences are remembered between sessions on the same browser.

---

### main.py (Pico W)

CircuitPython script that runs automatically when the Pico W boots.

#### Key functions

**`type_code(text, delay_ms)`**

Types each character one at a time using the `adafruit_hid` `KeyboardLayoutUS` layout. Characters that can't be typed in US layout are silently skipped. Returns the number of characters successfully typed.

```python
def type_code(text, delay_ms=50):
    delay = max(0.01, delay_ms / 1000)
    count = 0
    for char in text:
        try:
            layout.write(char)
            count += 1
            time.sleep(delay)
        except ValueError:
            print(f"Skipping unsupported char: {repr(char)}")
    return count
```

**`handle(conn)`**

Parses a raw HTTP request and routes it to the appropriate handler (`/ping` or `/type`). Sends CORS headers on every response so the mobile app (running as a local file) can reach it without browser security errors.

**`http_response(conn, status, body)`**

Sends a minimal HTTP/1.1 response with JSON body and CORS headers.

#### Startup sequence

```
Boot
 └─ Setup USB HID keyboard
 └─ Connect to WiFi
 └─ Print IP address to serial monitor
 └─ Bind HTTP server on port 5000
 └─ Main loop: accept → handle → close
```

---

## Troubleshooting

**Status pill stays "pico offline"**
- Make sure phone and Pico W are on the same WiFi network
- Check the IP address in Thonny serial monitor
- Verify `main.py` is in the root of the CIRCUITPY drive (not in a subfolder)
- Try unplugging and replugging the Pico W

**Characters are typed wrong or missing**
- The Pico W uses the US keyboard layout. If your PC uses a different layout (e.g. UK, AZERTY), some symbols may be wrong
- Increase the typing delay slider — sometimes the PC can't keep up
- Special Unicode characters are skipped; keep code to ASCII

**Gemini returns explanation text instead of just code**
- Try Gemini 2.0 Flash instead of 2.5 (more reliable at following strict instructions)
- Rephrase your prompt to be more specific

**"Pico returned error 500"**
- Open Thonny serial monitor to see the Python traceback
- Usually caused by unsupported characters in the text

**WiFi not connecting**
- Double-check `WIFI_SSID` and `WIFI_PASSWORD` in `main.py`
- The Pico W only supports 2.4 GHz WiFi, not 5 GHz

---

## Tips

- Set the typing delay to **80–100ms** for COBOL and JCL — they have longer lines and some editors do auto-indenting that can interfere at high speeds
- Click into your editor **before** tapping "Type it on PC" — you have 1.5 seconds after tapping
- Use the **copy** button to copy the generated code to clipboard as a backup before sending to Pico
- The app remembers your settings — you only need to configure it once per browser

---

## License

MIT — free to use, modify, and share.