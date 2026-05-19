# ST7735 MicroPython driver
# Source: github.com/AnthonyKNorman/MicroPython_ST7735
# MIT License

import ustruct
import time
from micropython import const

# Colours
BLACK   = const(0x0000)
RED     = const(0xF800)
GREEN   = const(0x07E0)
BLUE    = const(0x001F)
CYAN    = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW  = const(0xFFE0)
WHITE   = const(0xFFFF)

# Commands
NOP      = const(0x00)
SWRESET  = const(0x01)
RDDID    = const(0x04)
RDDST    = const(0x09)
SLPIN    = const(0x10)
SLPOUT   = const(0x11)
PTLON    = const(0x12)
NORON    = const(0x13)
INVOFF   = const(0x20)
INVON    = const(0x21)
DISPOFF  = const(0x28)
DISPON   = const(0x29)
CASET    = const(0x2A)
RASET    = const(0x2B)
RAMWR    = const(0x2C)
RAMRD    = const(0x2E)
PTLAR    = const(0x30)
COLMOD   = const(0x3A)
MADCTL   = const(0x36)
FRMCTR1 = const(0xB1)
FRMCTR2 = const(0xB2)
FRMCTR3 = const(0xB3)
INVCTR   = const(0xB4)
DISSET5  = const(0xB6)
PWCTR1   = const(0xC0)
PWCTR2   = const(0xC1)
PWCTR3   = const(0xC2)
PWCTR4   = const(0xC3)
PWCTR5   = const(0xC4)
VMCTR1   = const(0xC5)
RDID1    = const(0xDA)
RDID2    = const(0xDB)
RDID3    = const(0xDC)
RDID4    = const(0xDD)
PWCTR6   = const(0xFC)
GMCTRP1  = const(0xE0)
GMCTRN1  = const(0xE1)


class TFT:

    BLACK   = const(0x0000)
    RED     = const(0xF800)
    GREEN   = const(0x07E0)
    BLUE    = const(0x001F)
    CYAN    = const(0x07FF)
    MAGENTA = const(0xF81F)
    YELLOW  = const(0xFFE0)
    WHITE   = const(0xFFFF)

    @staticmethod
    def color(r, g, b):
        # Convert RGB888 to RGB565
        return (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3))

    def __init__(self, spi, dc, rst, cs):
        self._spi  = spi
        self._dc   = dc
        self._rst  = rst
        self._cs   = cs
        self._dc.init(self._dc.OUT, value=0)
        self._rst.init(self._rst.OUT, value=0)
        self._cs.init(self._cs.OUT, value=1)
        self._width  = 128
        self._height = 160
        self._x      = 0
        self._y      = 0
        self._rotation = 0
        self._rgb    = True

    def _reset(self):
        self._rst(0)
        time.sleep_ms(50)
        self._rst(1)
        time.sleep_ms(50)

    def _write_cmd(self, cmd):
        self._dc(0)
        self._cs(0)
        self._spi.write(bytearray([cmd]))
        self._cs(1)

    def _write_data(self, data):
        self._dc(1)
        self._cs(0)
        self._spi.write(data)
        self._cs(1)

    def _write_data_byte(self, data):
        self._dc(1)
        self._cs(0)
        self._spi.write(bytearray([data]))
        self._cs(1)

    def initr(self):
        self._reset()
        self._write_cmd(SWRESET)
        time.sleep_ms(150)
        self._write_cmd(SLPOUT)
        time.sleep_ms(500)
        self._write_cmd(FRMCTR1)
        self._write_data(bytearray([0x01, 0x2C, 0x2D]))
        self._write_cmd(FRMCTR2)
        self._write_data(bytearray([0x01, 0x2C, 0x2D]))
        self._write_cmd(FRMCTR3)
        self._write_data(bytearray([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D]))
        self._write_cmd(INVCTR)
        self._write_data_byte(0x07)
        self._write_cmd(PWCTR1)
        self._write_data(bytearray([0xA2, 0x02, 0x84]))
        self._write_cmd(PWCTR2)
        self._write_data_byte(0xC5)
        self._write_cmd(PWCTR3)
        self._write_data(bytearray([0x0A, 0x00]))
        self._write_cmd(PWCTR4)
        self._write_data(bytearray([0x8A, 0x2A]))
        self._write_cmd(PWCTR5)
        self._write_data(bytearray([0x8A, 0xEE]))
        self._write_cmd(VMCTR1)
        self._write_data_byte(0x0E)
        self._write_cmd(INVOFF)
        self._write_cmd(MADCTL)
        self._write_data_byte(0xC8)
        self._write_cmd(COLMOD)
        self._write_data_byte(0x05)
        self._write_cmd(CASET)
        self._write_data(bytearray([0x00, 0x00, 0x00, 0x7F]))
        self._write_cmd(RASET)
        self._write_data(bytearray([0x00, 0x00, 0x00, 0x9F]))
        self._write_cmd(GMCTRP1)
        self._write_data(bytearray([
            0x02, 0x1c, 0x07, 0x12, 0x37, 0x32,
            0x29, 0x2d, 0x29, 0x25, 0x2B, 0x39,
            0x00, 0x01, 0x03, 0x10]))
        self._write_cmd(GMCTRN1)
        self._write_data(bytearray([
            0x03, 0x1d, 0x07, 0x06, 0x2E, 0x2C,
            0x29, 0x2D, 0x2E, 0x2E, 0x37, 0x3F,
            0x00, 0x00, 0x02, 0x10]))
        self._write_cmd(NORON)
        time.sleep_ms(10)
        self._write_cmd(DISPON)
        time.sleep_ms(100)

    def rgb(self, on):
        self._rgb = on
        if on:
            self._write_cmd(MADCTL)
            if self._rotation == 0:
                self._write_data_byte(0xC8)
            elif self._rotation == 1:
                self._write_data_byte(0xA8)
            elif self._rotation == 2:
                self._write_data_byte(0x08)
            else:
                self._write_data_byte(0x68)

    def rotation(self, r):
        self._rotation = r
        if r == 0:
            self._width  = 128
            self._height = 160
            madctl = 0xC8
        elif r == 1:
            self._width  = 160
            self._height = 128
            madctl = 0xA8
        elif r == 2:
            self._width  = 128
            self._height = 160
            madctl = 0x08
        else:
            self._width  = 160
            self._height = 128
            madctl = 0x68
        self._write_cmd(MADCTL)
        self._write_data_byte(madctl)

    def size(self):
        return self._width, self._height

    def _setwindow(self, x0, y0, x1, y1):
        self._write_cmd(CASET)
        self._write_data(ustruct.pack(">HH", x0, x1))
        self._write_cmd(RASET)
        self._write_data(ustruct.pack(">HH", y0, y1))
        self._write_cmd(RAMWR)

    def _color565(self, color):
        return ustruct.pack(">H", color)

    def fill(self, color):
        self._setwindow(0, 0, self._width - 1, self._height - 1)
        buf = self._color565(color) * 32
        total = self._width * self._height
        dc = self._dc
        cs = self._cs
        spi = self._spi
        dc(1); cs(0)
        for _ in range(total // 32):
            spi.write(buf)
        rem = total % 32
        if rem:
            spi.write(self._color565(color) * rem)
        cs(1)

    def pixel(self, pos, color):
        x, y = pos
        if 0 <= x < self._width and 0 <= y < self._height:
            self._setwindow(x, y, x, y)
            self._write_data(self._color565(color))

    def fillrect(self, pos, size, color):
        x, y   = pos
        w, h   = size
        x1 = min(x + w - 1, self._width - 1)
        y1 = min(y + h - 1, self._height - 1)
        x  = max(x, 0); y = max(y, 0)
        if x > x1 or y > y1:
            return
        self._setwindow(x, y, x1, y1)
        buf  = self._color565(color) * 32
        total = (x1 - x + 1) * (y1 - y + 1)
        dc = self._dc; cs = self._cs; spi = self._spi
        dc(1); cs(0)
        for _ in range(total // 32):
            spi.write(buf)
        rem = total % 32
        if rem:
            spi.write(self._color565(color) * rem)
        cs(1)

    def rect(self, pos, size, color):
        x, y = pos
        w, h = size
        self.hline((x, y),         w, color)
        self.hline((x, y + h - 1), w, color)
        self.vline((x,         y), h, color)
        self.vline((x + w - 1, y), h, color)

    def hline(self, pos, length, color):
        x, y = pos
        self.fillrect((x, y), (length, 1), color)

    def vline(self, pos, length, color):
        x, y = pos
        self.fillrect((x, y), (1, length), color)

    def line(self, pos0, pos1, color):
        x0, y0 = pos0
        x1, y1 = pos1
        dx =  abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.pixel((x0, y0), color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0  += sx
            if e2 <= dx:
                err += dx
                y0  += sy

    def fillcircle(self, pos, r, color):
        x0, y0 = pos
        f     = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x, y  = 0, r
        self.vline((x0, y0 - r), 2 * r + 1, color)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f     += ddF_y
            x     += 1
            ddF_x += 2
            f     += ddF_x
            self.vline((x0 + x, y0 - y), 2 * y + 1, color)
            self.vline((x0 - x, y0 - y), 2 * y + 1, color)
            self.vline((x0 + y, y0 - x), 2 * x + 1, color)
            self.vline((x0 - y, y0 - x), 2 * x + 1, color)

    def char(self, pos, char, color, font, size=1):
        x, y   = pos
        index  = (ord(char) - 32) * 5
        for i in range(5):
            line = font[index + i]
            for j in range(8):
                if line & 0x1:
                    if size == 1:
                        self.pixel((x + i, y + j), color)
                    else:
                        self.fillrect((x + i * size, y + j * size),
                                      (size, size), color)
                line >>= 1

    def text(self, pos, string, color, font, size=1, space=1):
        x, y = pos
        for char in string:
            self.char((x, y), char, color, font, size)
            x += (6 * size) + space
            if x + 5 * size > self._width:
                x  = 0
                y += 8 * size + space