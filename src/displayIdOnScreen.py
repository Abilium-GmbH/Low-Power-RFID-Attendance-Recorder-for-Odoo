#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import RPi.GPIO as GPIO
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from simplemfrc import SimpleMFRC522
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont


epd = epd2in7.EPD()


try:
  epd.init() 
  while(True):
    epd.Clear(0xFF)
    font18 = ImageFont.truetype('Font.ttc', 18)
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((epd.height/2-90, epd.width/2-17), 'Bitte Karte einfuehren.', font = font18, fill = 0)
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
    reader = SimpleMFRC522()
    id, text = reader.read()
    epd.init()
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((epd.height/2-47, epd.width/2-35), 'Ihre ID ist:', font = font18, fill = 0)
    draw.text((epd.height/2-60, epd.width/2+20), str(id), font = font18, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(5)

except KeyboardInterrupt:
    epd2in7.epdconfig.module_exit()
    exit()
