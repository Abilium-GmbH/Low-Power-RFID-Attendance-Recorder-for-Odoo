#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from lib.simplemfrc import SimpleMFRC522
from lib.waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from datetime import timedelta
from odoo.interpreter import Interpreter
from os import path

resources = path.join(path.dirname(__file__),"resources")


epd = epd2in7.EPD()

try:
  epd.init() 
  while(True):
    # codeblock establishes the default drawing on the e-paper
    #epd.Clear(0xFF)
    font18 = ImageFont.truetype(path.join(resources,"Font.ttc"), 18) 
    Himage = Image.open(path.join(resources,"abilium.bmp"))
    #Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((epd.height/2-90, epd.width/2-70), 'Bitte Karte einfuehren.', font = font18, fill = 0)
    now = datetime.utcnow() # should change depending on where you are
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    draw.text((epd.height/2-68, epd.width/2+55), dt_string, font = font18, fill = 0)
    epd.display(epd.getbuffer(Himage))
    epd.sleep()

    # wait for a nfc token from an employee
    reader = SimpleMFRC522()
    id, text = reader.read()

    odoo_handler = Interpreter()
    try:
        employee = odoo_handler.getEmployee(id)
        if employee.isCheckedOut :
            odoo_handler.check_in(employee)

            # draw check-in image
            epd.init()
            Himage = Image.new('1', (epd.height, epd.width), 255)
            draw = ImageDraw.Draw(Himage)
            draw.text((epd.height/2-70, epd.width/2-15), 'Hallo    ' + employee.name, font = font18, fill = 0)
            epd.display(epd.getbuffer(Himage))
        if not employee.isCheckedOut:
            odoo_handler.check_out(employee)

            # draw check-out image
            epd.init()
            Himage = Image.new('1', (epd.height, epd.width), 255)
            draw = ImageDraw.Draw(Himage)
            draw.text((epd.height/2-70, epd.width/2-15), 'Tschuess ' + employee.name, font = font18, fill = 0)
            draw.text((epd.height/2-100, epd.width/2+5), 'Arbeitsstunden:' + str(timedelta(hours = employee.hours_this_month)), font = font18, fill = 0)
            epd.display(epd.getbuffer(Himage))

    except ValueError:
        # draw unknown image
        epd.init()
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((epd.height/2-70, epd.width/2-15), 'Wie bitte?' , font = font18, fill = 0)
        epd.display(epd.getbuffer(Himage))

                
    time.sleep(5)

except KeyboardInterrupt:
    # epd2in7.epdconfig.module_exit()
    exit()
