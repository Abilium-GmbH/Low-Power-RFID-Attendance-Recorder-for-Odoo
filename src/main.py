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
from odoo.illustrator import Illustrator
from os import path
from gpiozero import Button  # import the Button control from gpiozero


resources = path.join(path.dirname(__file__),"resources")

key1 = Button(5)
key2 = Button(6)
keyPressed = False
epd = epd2in7.EPD()

try:
  tempInterpreter = Interpreter()
  tempInterpreter.getLogoTest()
  illustrator = Illustrator()
  while(True):
    illustrator.initialScreen()
    keyPressed = False

    # wait for a nfc token from an employee
    reader = SimpleMFRC522()
    id, text = reader.read()

    odoo_handler = Interpreter()
    try:
        employee = odoo_handler.getEmployee(id)
        if key1.is_pressed:

            keyPressed = True
            if employee.isCheckedOut:
                illustrator.isCheckedInOutScreen(employee.name, True)

            if not employee.isCheckedOut:
                illustrator.isCheckedInOutScreen(employee.name, False)

        if employee.isCheckedOut and not keyPressed:
            odoo_handler.check_in(employee)
            illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', True)
            
        if not employee.isCheckedOut and not keyPressed:
            odoo_handler.check_out(employee)
            illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', False)

    except ValueError:
        illustrator.unknownScreen()

    if key2.is_pressed:
        illustrator.checkIpAdress()


    time.sleep(5)

except KeyboardInterrupt:
    exit()
