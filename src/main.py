#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from lib.simplemfrc import SimpleMFRC522
from lib.waveshare_epd import epd2in7
import time
from datetime import datetime
from datetime import timedelta
from odoo.interpreter import Interpreter
from odoo.illustrator import Illustrator
from os import path

resources = path.join(path.dirname(__file__),"resources")

# enable Buttons
BUTTON1_GPIO = 5
BUTTON2_GPIO = 6

global key1Pressed 
key1Pressed = False
global key2Pressed
key2Pressed = False
global keypresstimestamp 
keypresstimestamp = 0

def button1_pressed_callback(channel):
    global key1Pressed
    key1Pressed = True
    # needed as a timeout for key presses
    global keypresstimestamp
    keypresstimestamp = time.time()

def button2_pressed_callback(channel):
    global key2Pressed
    key2Pressed = True
    # needed as a timeout for key presses
    global keypresstimestamp
    keypresstimestamp = time.time()

#async. button management
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
  reader = SimpleMFRC522()

  now = datetime.now()
  oldmin = int(now.strftime("%M"))

  while(True):
    start = time.time()
    #once current time is known check if keypresses have expired
    if (keypresstimestamp + 5 < start) and (key1Pressed or key2Pressed):
      keypresstimestamp = 0
      key1Pressed = False
      key2Pressed = False
    #power up the RFID antenna
    reader.READER.MFRC522_Init()
    # listen for 0.25s for an RFID card
    id = reader.read_id_no_block()
    while (time.time() < start + 0.25) and (not id):
       id = reader.read_id_no_block()
    #power down the RFID antenna
    reader.READER.AntennaOff()
    if id:
      odoo_handler = Interpreter()
      try:
          employee = odoo_handler.getEmployee(id)
          if key1Pressed:
              if employee.isCheckedOut:
                  illustrator.isCheckedInOutScreen(employee.name, False)

              if not employee.isCheckedOut:
                  illustrator.isCheckedInOutScreen(employee.name, True)

          if employee.isCheckedOut and not key1Pressed:
              odoo_handler.check_in(employee)
              illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', True)

          if not employee.isCheckedOut and not key1Pressed:
              odoo_handler.check_out(employee)
              illustrator.checkInOutScreen(employee.name, str(timedelta(hours = employee.hours_this_month)).split(':')[0] + 'h  ' + str(timedelta(hours = employee.hours_this_month)).split(':')[1] + 'm', False)

      except ValueError:
            illustrator.unknownScreen()

      if key2Pressed:
          illustrator.checkIpAdress()

      time.sleep(5)
      illustrator.initialScreen()
      #update minute change detector if a login/out already refreshed the clock on home
      now = datetime.now()
      newmin = int(now.strftime("%M"))
      oldmin = newmin
      keypresstimestamp = 0
      key1Pressed = False
      key2Pressed = False

    else:
      #minute change detector to refresh screen on minute change
      now = datetime.now()
      newmin = int(now.strftime("%M"))
      if not oldmin == newmin:
        oldmin = newmin
        illustrator.initialScreen()
      else:
        time.sleep(1)

except KeyboardInterrupt:
    reader.READER.Close_MFRC522()
    exit()
