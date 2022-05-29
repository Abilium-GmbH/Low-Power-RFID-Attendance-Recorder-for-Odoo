import time
from lib.waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont
from os import path

resources = path.join(path.dirname(__file__), "..", "resources")
epd = epd2in7.EPD()

class integrationIllustrator():
    """
    This class is used to draw the results of the integration test on the E-Ink-Display. 
    These methods write on the display what they say they will write.
    """
    # It is just for testing therefore it does not need to be pretty code.
    # Be happy that there are tests

    def __init__(self) -> None:
        self.font = ImageFont.truetype(path.join(resources, "Font.ttc"), 18)

    def eInkOk(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'E-Ink-Display intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def rfidCheck(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Scanne eine Karte/Badge.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        epd.sleep()
        print("sleeped")

    def button1Check(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Drücke "key 1".', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button2Check(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Drücke "key 2".', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button3Check(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Drücke "key 3".', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button4Check(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Drücke "key 4".', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def hardwareOk(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Alle Hardware intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def rfidOk(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Rfid-Reader intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button1Ok(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 1 intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button2Ok(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 2 intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button3Ok(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 3 intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button4Ok(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 4 intakt.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button1Defect(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 1 defect or not pressed.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button2Defect(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 2 defect or not pressed.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button3Defect(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 3 defect or not pressed.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

    def button4Defect(self):
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 70), 'Key 4 defect or not pressed.', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)