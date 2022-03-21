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
  epd.Clear(0xFF)
  Himage = Image.open('abilium.bmp')
  draw = ImageDraw.Draw(Himage)
  epd.display(epd.getbuffer(Himage))
  epd.sleep()

except KeyboardInterrupt:
    epd2in7.epdconfig.module_exit()
    exit()
