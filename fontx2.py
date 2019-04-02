from io import BytesIO

class FontX2:
    def __init__(self, hw, fw, fb):
	self.hw_font = hw
        self.fw_font = fw
        self.fb = fb

        hh, hf = FontX2.file_check(hw)
        if hf != 0:
            raise ValueError('Flag of half-font is not ANK.')

        fh, ff = FontX2.file_check(fw)
        if ff != 1:
            raise ValueError('Flag of full-font in not Shift-JIS.')
        if hh != fh:
            raise ValueError('The height of the font is different.')

    def text_sjis(self, sjis, x, y, c):
        bytes = BytesIO(sjis)
        fp = []
        fw = []
        n = 0
        while True:
            b = bytes.read(1)
            if b == b'':
                break
            code = ord(b)
            if (0x20 <= code <= 0x7e) or (0xa1 <= code <= 0xdf):
    	        fp.append(FontX2.font_pattern(self.hw_font, code))
            elif 0x81 <= code <=0x9f or 0xe0 <= code <= 0xef :
                low = ord(bytes.read(1))
                if 0x40 <= low <= 0x7e or 0x80 <= low <= 0xfc :
                    code = (code << 8) + low
                    fp.append(FontX2.font_pattern(self.fw_font, code))

            fw.append(len(fp[n][0]))
            n += 1

        h = len(fp[0])

        for yy in range(h):
            xxx = x
            for nn in range(len(fw)):
                for xx in range(fw[nn]):
	            self.fb.pixel(xxx, y+yy, fp[nn][yy][xx]*c)
                    xxx += 1

    @staticmethod
    def font_pattern( fontname, code ):

        with open(fontname,'rb') as f:
            type = f.read(6)
            name = f.read(8)
            w = ord(f.read(1))
            h = ord(f.read(1))

            fs = (w+7)//8*h                             # font size
            offset = 0

            if ord(f.read(1)) == 0:
                font_width = 'half'
                if code < 0x100:
                    offset = 17 + code * fs
                else:
                    print('code is not ASCII !')

            else:
                font_width = 'full'

                cb = ord(f.read(1))                     # code block
                ccc = 0
                offset = 0

                for i in range(cb):
                    cbs = int.from_bytes(f.read(2), 'little')
                    cbe = int.from_bytes(f.read(2), 'little')

                    if code >= cbs and code <= cbe :
                        ccc += code -cbs
                        offset = 18 + 4 * cb + ccc * fs
                        break

                    ccc += cbe - cbs + 1

            if offset:
                f.seek(offset)
                fontpat = f.read(fs)
            else:
                print('code not found!!')
                return

            x = 0
            y = 0
            font = [[0 for i in range(w)] for j in range(h)]

            for s in range(fs):
                for b in range(8):
                    if fontpat[s] & 0b10000000 >> b > 0:
                        font[y][x] = 1

                    x += 1
                    if x == w:
                        x = 0
                        y += 1
                        break

            return font

    @staticmethod
    def file_check(file_name):
        with open(file_name, 'rb') as f:
            sig = f.read(6)
            if sig != b'FONTX2':
                raise ValueError("Not FONTX2 file")
            name = f.read(8)
            w = ord(f.read(1))
            h = ord(f.read(1))
            flag = ord(f.read(1))
            return(h, flag)
