import uio
import lcdF7D

class LcdConsole(uio.IOBase):
    def __init__(self):
        self.lcd = lcdF7D
        self.lcd.set_font(12)
        self.width = self.lcd.get_x_size()
        self.height = self.lcd.get_y_size()
        self.line_height()
        self.cls()

    def cls(self):
        self.x = 0
        self.y = 0
        self.lcd.clear()

    def line_height(self):
        self.line_h = self.lcd.font_height()
        self.font_w = self.lcd.font_width()
        self.w =  self.width // self.font_w
        self.h =  self.height // self.line_h

    def _putc(self, c):
        c = chr(c)
        if c == '\n':
            self.x = 0
            self._newline()
        elif c == '\x08':
            self._backspace()
        elif c >= ' ':
            self.lcd.display_char(self.x * self.font_w, self.y * self.line_h, ord(c))
            self.x += 1
            if self.x >= self.w:
                self._newline()
                self.x = 0

    def write(self, buf):
        i = 0
        while i < len(buf):
            c = buf[i]
            if c == 0x1b: # skip escape sequence
                i += 1
                while chr(buf[i]) in '[;0123456789':
                    i += 1
            else:
                self._putc(c)
            i += 1
        return len(buf)

    def readinto(self, buf, nbytes=0):
        return None
        
    def _newline(self):
        self.y += 1
        if self.y >= self.h:
            self.lcd.scroll(0, -self.line_h)            
            self.y = self.h - 1
            self.lcd.clear_string_line(self.y)

    def _erase_current(self):
        self.lcd.clear_string_line(self.y)

    def _backspace(self):
        if self.x == 0:
            if self.y > 0:
                self.y -= 1
                self.x = self.w - 1
                self.lcd.clear_string_line(self.y)
        else:
            self.x -= 1
            self._putc(0x20)
            self.x -= 1

