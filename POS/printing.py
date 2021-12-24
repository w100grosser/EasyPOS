
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
    
    def print_r(self, items):
        with open('/root/EasyPOS/POS/readme.txt', 'r') as f:
            if ('readme' in f.read()):
                return 1
            
        with open('/root/EasyPOS/POS/readme.txt', 'w') as f:
            f.write('readme')
        self.p = Usb(0x1504, 0x006e, 0,in_ep=0x81, out_ep=0x02)
        widthj, heightj = self.jerash.size
        height = 30 + len(items) * 30
        img = Image.new('RGB',size=(500,height),color = 'white')
        font1 = ImageFont.truetype("/root/EasyPOS/static/fonts/Arial.ttf", 18)
        draw = ImageDraw.Draw(img)
        draw.line([(0,28),(500,28)],(0,0,0), 2)
        draw.line([(298,28),(298,height)],(0,0,0), 2)
        draw.line([(368,28),(368,height)],(0,0,0), 2)
        draw.line([(408,28),(408,height)],(0,0,0), 2)
        draw.text((10, 0),"Name",(0,0,0),font=font1)
        draw.text((300, 0),"Price",(0,0,0),font=font1)
        draw.text((370, 0),"N",(0,0,0),font=font1)
        draw.text((410, 0),"Total",(0,0,0),font=font1)
        counter = 1
        for i in items.keys():
            draw.text((10, counter * 30),get_display(arabic_reshaper.reshape(str(items[i]['name'][:24]))),(0,0,0),font=font1)
            draw.text((300, counter * 30),str(round(items[i]['price'],2)),(0,0,0),font=font1)
            draw.text((370, counter * 30),str(items[i]['Ni']),(0,0,0),font=font1)
            draw.text((410, counter * 30),str(round(items[i]['price'] * items[i]['Ni'],2)),(0,0,0),font=font1)
            counter +=1
        dst = Image.new('RGB', (500, img.height + 50 + self.jerash.height),color = 'white')
        dst.paste(self.jerash, (100, 30))
        dst.paste(img, (0, self.jerash.height + 50))

        draw = ImageDraw.Draw(dst)
        draw.text((180, 0),get_display(arabic_reshaper.reshape("اوراق الزيتون")),(0,0,0),font=font1)
        self.p.image(dst)
        self.p.cut()
        self.p.close()

        with open('/root/EasyPOS/POS/readme.txt', 'w') as f:
            f.write('')
        return 1
    