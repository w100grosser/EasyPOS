
from ast import excepthandler
from PIL import Image

from PIL import ImageFont
from PIL import ImageDraw 
from escpos.printer import Usb
import arabic_reshaper
from bidi.algorithm import get_display

class print_receipt:
    def __init__(self):
        jerash = Image.open('/root/EasyPOS/static/ims/123.jpg')
        jerash.thumbnail((300, 100000))
        self.jerash = jerash
        try:
            self.p = Usb(0x1504, 0x006e, 0,in_ep=0x81, out_ep=0x02)
        except:
            print("can't connect")
            

    
    def print_r(self, items):
        total = 0
        with open('/root/EasyPOS/POS/readme.txt', 'r') as f:
            if ('readme' in f.read()):
                return 2
            
        with open('/root/EasyPOS/POS/readme.txt', 'w') as f:
            f.write('readme')

        try:
            nlines = 0
            for i in items.keys():
                lines = self.name_p(items[i]['name'])
                nlines += len(lines)
                nlines += 0.5
            print(nlines)
            widthj, heightj = self.jerash.size
            height = 30 + nlines * 30 + 55
            img = Image.new('RGB', size=(500, int(height)), color='white')
            font1 = ImageFont.truetype("/root/EasyPOS/static/fonts/Arial.ttf", 30)
            font2 = ImageFont.truetype("/root/EasyPOS/static/fonts/Arial.ttf", 50)
            draw = ImageDraw.Draw(img)
            draw.line([(0, 28), (500, 28)], (0, 0, 0), 2)
            draw.line([(268, 28), (268, height - 55)], (0, 0, 0), 2)
            draw.line([(358, 28), (358, height - 55)], (0, 0, 0), 2)
            draw.line([(408, 28), (408, height - 55)], (0, 0, 0), 2)
            draw.line([(0, height - 55), (500, height - 55)], (0, 0, 0), 2)
            draw.line([(0, height-2), (500, height-2)], (0, 0, 0), 2)
            draw.text((10, 0), "Name", (0, 0, 0), font=font1)
            draw.text((275, 0), "Price", (0, 0, 0), font=font1)
            draw.text((360, 0), "N", (0, 0, 0), font=font1)
            draw.text((410, 0), "Total", (0, 0, 0), font=font1)
            counter = 1
            for i in items.keys():
                draw.text((270, counter * 30),
                        str(round(items[i]['price'], 2)), (0, 0, 0), font=font1)
                draw.text((360, counter * 30),
                        str(items[i]['Ni']), (0, 0, 0), font=font1)
                draw.text((410, counter * 30),
                        str(round(items[i]['price'] * items[i]['Ni'], 2)), (0, 0, 0), font=font1)
                total += items[i]['price'] * items[i]['Ni']

                lines = self.name_p(items[i]['name'])
                for line in lines:
                    draw.text((10, counter * 30), get_display(arabic_reshaper.reshape(
                        str(line))), (0, 0, 0), font=font1)
                    counter += 1
                counter += 0.5
            draw.text((20, counter * 30), "Total: " + str(total), (0, 0, 0), font=font2)
            dst = Image.new('RGB', (500, img.height + 150 +
                            self.jerash.height), color='white')
            dst.paste(self.jerash, (100, 30))
            dst.paste(img, (0, self.jerash.height + 55))

            draw = ImageDraw.Draw(dst)
            draw.text((180, 0), get_display(arabic_reshaper.reshape(
                "اوراق الزيتون")), (0, 0, 0), font=font1)
            # dst.save('/root/EasyPOS/POS/migrations/1.png')
            self.p.image(dst)
            self.p.cut()
            # self.p.close()
        
            with open('/root/EasyPOS/POS/readme.txt', 'w') as f:
                f.write('')
            return 1
        except Exception as e:
            print(e)
            with open('/root/EasyPOS/POS/readme.txt', 'w') as f:
                f.write('')
            
            try:
                self.p = Usb(0x1504, 0x006e, 0,in_ep=0x81, out_ep=0x02)
            except:
                print("can't connect")
            return 0
    def name_p(self, name):
        print('yess')
        lines = []
        while len(name) > 16:
            lines.append(name[:16])
            name = name[16:]
        if len(name) > 0:
            lines.append(name)
        if len(lines) == 0:
            lines = ['']
        return lines
    