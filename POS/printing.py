
from ast import excepthandler
from PIL import Image

from PIL import ImageFont
from PIL import ImageDraw 
from .scripts.custom_escpos import Escpos
# from escpos.printer import Usb
import usb.core
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
    
class Usb(Escpos):
    """USB printer
    This class describes a printer that natively speaks USB.
    inheritance:
    .. inheritance-diagram:: escpos.printer.Usb
        :parts: 1
    """

    def __init__(
        self,
        idVendor,
        idProduct,
        usb_args=None,
        timeout=0,
        in_ep=0x82,
        out_ep=0x01,
        *args,
        **kwargs
    ):  # noqa: N803
        """
        :param idVendor: Vendor ID
        :param idProduct: Product ID
        :param usb_args: Optional USB arguments (e.g. custom_match)
        :param timeout: Is the time limit of the USB operation. Default without timeout.
        :param in_ep: Input end point
        :param out_ep: Output end point
        """
        Escpos.__init__(self, *args, **kwargs)
        self.timeout = timeout
        self.in_ep = in_ep
        self.out_ep = out_ep

        usb_args = usb_args or {}
        if idVendor:
            usb_args["idVendor"] = idVendor
        if idProduct:
            usb_args["idProduct"] = idProduct
        self.open(usb_args)

    def open(self, usb_args):
        """Search device on USB tree and set it as escpos device.
        :param usb_args: USB arguments
        """
        for dev in usb.core.find(find_all = True):
            if dev.idVendor == int(usb_args["idVendor"], 16) and int(dev.idProduct, 16) == usb_args["idProduct"]:
                self.device = dev

        # self.device = usb.core.find(**usb_args)
        if self.device is None:
            raise Exception("Device not found or cable not plugged in.")

        self.idVendor = self.device.idVendor
        self.idProduct = self.device.idProduct

        # pyusb has three backends: libusb0, libusb1 and openusb but
        # only libusb1 backend implements the methods is_kernel_driver_active()
        # and detach_kernel_driver().
        # This helps enable this library to work on Windows.
        if self.device.backend.__module__.endswith("libusb1"):
            check_driver = None

            try:
                check_driver = self.device.is_kernel_driver_active(0)
            except NotImplementedError:
                pass

            if check_driver is None or check_driver:
                try:
                    self.device.detach_kernel_driver(0)
                except NotImplementedError:
                    pass
                except usb.core.USBError as e:
                    if check_driver is not None:
                        print("Could not detatch kernel driver: {0}".format(str(e)))

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print("Could not set configuration: {0}".format(str(e)))

    def _raw(self, msg):
        """Print any command sent in raw format
        :param msg: arbitrary code to be printed
        :type msg: bytes
        """
        self.device.write(self.out_ep, msg, self.timeout)

    def _read(self):
        """Reads a data buffer and returns it to the caller."""
        return self.device.read(self.in_ep, 16)

    def close(self):
        """Release USB interface"""
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None