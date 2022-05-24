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
import signal
import sys

resources = path.join(path.dirname(__file__),"resources")

BUTTON1_GPIO = 5
BUTTON2_GPIO = 6

global key1Pressed 
key1Pressed = False
global key2Pressed
key2Pressed = False

def button1_pressed_callback(channel):
    global key1Pressed
    print("Button 1 pressed!")
    key1Pressed = True

def button2_pressed_callback(channel):
    global key2Pressed
    print("Button 2 pressed!")
    key2Pressed = True


GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON1_GPIO, GPIO.FALLING,callback=button1_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON2_GPIO, GPIO.FALLING,callback=button2_pressed_callback, bouncetime=100)

try:
  odoo_handler = Interpreter()
  odoo_handler.getLogo()
  illustrator = Illustrator()
  illustrator.initialScreen()

  now = datetime.now()
  oldmin = int(now.strftime("%M"))
  
  while(True):
    # wait for a nfc token from an employee
    reader = SimpleMFRC522()
    start = time.time()
    id = reader.read_id_no_block()
    while (time.time() < start + 0.25) and (not id):
       id = reader.read_id_no_block()
    #reader.READER.MFRC522_Reset()
    if id:
      
      try:
          employee = odoo_handler.getEmployee(id)
          if key1Pressed: #key1.is_pressed:
              #keyPressed = True
              if employee.isCheckedOut:
                  illustrator.isCheckedInOutScreen(employee.name, True)

              if not employee.isCheckedOut:
                  illustrator.isCheckedInOutScreen(employee.name, False)

          if employee.isCheckedOut and not key1Pressed and not key2Pressed:
              odoo_handler.check_in(employee)
              illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', True)
              #illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', False)

          if not employee.isCheckedOut and not key1Pressed and not key2Pressed:
              odoo_handler.check_out(employee)
              illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', False)
              #illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', True)

      except ValueError:
            illustrator.unknownScreen()

      if key2Pressed: #key2.is_pressed:
          illustrator.checkIpAdress()

      time.sleep(5)
      illustrator.initialScreen()
      now = datetime.now()
      newmin = int(now.strftime("%M"))
      oldmin = newmin
      key1Pressed = False
      key2Pressed = False

    else:
      now = datetime.now()
      newmin = int(now.strftime("%M"))
      if not oldmin == newmin:
        oldmin = newmin
        illustrator.initialScreen()
      else:
        time.sleep(1)

except KeyboardInterrupt:
    exit()
