from lib.waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
from os import path
from datetime import datetime
import netifaces as ni  # Importing netifaces to gather network information

resources = path.join(path.dirname(__file__), "..", "resources")

epd = epd2in7.EPD()

class Illustrator():

    def __init__(self) -> None:
        """
        Initializes logo, font and the ip address
        """
        self.font = ImageFont.truetype(path.join(resources,"Font.ttc"), 18) 
        self.logo = Image.open(path.join(resources,"resizedCompanyLogo.bmp"))
        self.ip = self.get_ips()

    @staticmethod
    def get_ips():
        """
        Searches the networkinterface for the ip address of the device and returns the first one it finds
        """
        interfaces = ni.interfaces()
        interfaces.remove('lo')

        for interface in interfaces:
            addrs = ni.ifaddresses(interface)
            if ni.AF_INET in addrs.keys() and 'addr' in addrs[ni.AF_INET][0]:
                return addrs[ni.AF_INET][0]['addr']
        raise Exception("no internet") # honestly, if this happens you have bigger problems

    def initialScreen(self):
        """
        Draws the image for the initial screen on the display
        """
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        bmp = Image.open(path.join(resources,"resizedCompanyLogo.bmp")) 
        Himage.paste(bmp, (0,0))
        draw.text((epd.height/2-100, epd.width/2-70), 'Bitte Karte einführen.', font = self.font, fill = 0)
        now = datetime.now() 
        dt_string = now.strftime("%d/%m/%Y %H:%M") # get time
        draw.text((epd.height/2-68, epd.width/2+55), dt_string, font = self.font, fill = 0)
        epd.display(epd.getbuffer(Himage))
        bmp.close() # helps to contain overflow on the raspberry pi
        epd.sleep()


    def checkInOutScreen(self, employeeName : str, employeeHours : str, checkInScreen : bool):
        """
        Checks the user In or Out

        Args:
        employeeName: Name of the employee
        employeeHours: Number of hours the employee has worked
        checkInScreen: Bool that checks the user In if True, or Out if False
        """
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        if checkInScreen:
            draw.text((epd.height/2-100, epd.width/2-15), 'Hallo ' + employeeName, font = self.font, fill = 0)
        else:
            draw.text((epd.height/2-100, epd.width/2-15), 'Tschüss ' + employeeName, font = self.font, fill = 0)
        draw.text((epd.height/2-100, epd.width/2+5), 'Arbeitsstunden:', font = self.font, fill = 0)
        draw.text((epd.height / 2 - 100, epd.width / 2 + 25), employeeHours, font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
    
    def unknownScreen(self):
        """
        Displays a question
        Is used to tell that for example a card is unknown to the odoo server
        """
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height/2-70, epd.width/2-15), 'Wie bitte?' , font = self.font, fill = 0)
        epd.display(epd.getbuffer(Himage))

    def isCheckedInOutScreen(self, employeeName : str, isCheckedInScreen : bool):
        """
        Tells the user whether he is Checked In or Out by writing it on the display

        Args:
        employeeName: Name of the employee
        isCheckedInScreen: Bool if True it displays that the user is Checked In. Else it displays that the user is checked out
        """
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 35), 'Hallo ' + employeeName, font=self.font, fill=0)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 15), 'Du bist aktuell', font=self.font, fill=0)
        if isCheckedInScreen:
            draw.text((epd.height / 2 - 100, epd.width / 2 + 5), 'eingecheckt', font=self.font, fill=0)
        else:
            draw.text((epd.height / 2 - 100, epd.width / 2 + 5), 'ausgecheckt', font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))

    def checkIpAdress(self):
        """
        Draws the IP on the display
        """
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height / 2 - 100, epd.width / 2 - 15), 'IP: ' + self.ip, font=self.font, fill=0)
        epd.display(epd.getbuffer(Himage))
