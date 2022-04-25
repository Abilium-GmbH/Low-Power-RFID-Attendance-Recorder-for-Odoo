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

resources = path.join(path.dirname(__file__),"resources")


epd = epd2in7.EPD()

try:
  illustrator = Illustrator()
  while(True):
    illustrator.initialScreen()

    # wait for a nfc token from an employee
    reader = SimpleMFRC522()
    id, text = reader.read()

    odoo_handler = Interpreter()
    try:
        employee = odoo_handler.getEmployee(id)
        if employee.isCheckedOut :
            odoo_handler.check_in(employee)
            illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)), True)
            
        if not employee.isCheckedOut:
            odoo_handler.check_out(employee)
            illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)), False)

    except ValueError:
        illustrator.unknownScreen()

                
    time.sleep(5)

except KeyboardInterrupt:
    exit()
