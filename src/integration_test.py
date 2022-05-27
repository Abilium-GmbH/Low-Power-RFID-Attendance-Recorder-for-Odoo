#!/usr/bin/python
# -*- coding:utf-8 -*-
from lib.simplemfrc import SimpleMFRC522
from lib.waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from datetime import timedelta
from odoo.integrationIllustrator import integrationIllustrator
from os import path
from gpiozero import Button  # import the Button control from gpiozero
import RPi.GPIO as GPIO
import signal
import sys

resources = path.join(path.dirname(__file__), "resources")
epd = epd2in7.EPD()

BUTTON1_GPIO = 5
BUTTON2_GPIO = 6
BUTTON3_GPIO = 13
BUTTON4_GPIO = 19

global key1Pressed
key1Pressed = False
global key2Pressed
key2Pressed = False
global key3Pressed
key3Pressed = False
global key4Pressed
key4Pressed = False

def button1_pressed_callback(channel):
    global key1Pressed
    print("Button 1 pressed!")
    key1Pressed = True

def button2_pressed_callback(channel):
    global key2Pressed
    print("Button 2 pressed!")
    key2Pressed = True

def button3_pressed_callback(channel):
    global key3Pressed
    print("Button 3 pressed!")
    key3Pressed = True

def button4_pressed_callback(channel):
    global key4Pressed
    print("Button 4 pressed!")
    key4Pressed = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON1_GPIO, GPIO.FALLING,callback=button1_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON2_GPIO, GPIO.FALLING,callback=button2_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON3_GPIO, GPIO.FALLING,callback=button3_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON4_GPIO, GPIO.FALLING,callback=button4_pressed_callback, bouncetime=100)

try:
  illustrator = integrationIllustrator()

  # Here we check, if the e-Ink-Display works
  illustrator.eInkOk()

  # Here we check, if the rfid-Reader works
  illustrator.rfidCheck()
  reader = SimpleMFRC522()
  id, text = reader.read()

  # No check needed
  illustrator.rfidOk()


  # Here we check, if the four buttons work
  illustrator.button1Check()
  if key1Pressed:
    illustrator.button1Ok()

  illustrator.button2Check()
  if key2Pressed:
    illustrator.button2Ok()

  illustrator.button3Check()
  if key3Pressed:
    illustrator.button3Ok()

  illustrator.button4Check()
  if key4Pressed:
     illustrator.button4Ok()

  # After all checks passed, the hardware is working as intended
  if not key1Pressed or not key2Pressed or not key3Pressed or not key4Pressed:
      if not key1Pressed:
         illustrator.button1Defect()
      if not key2Pressed:
         illustrator.button2Defect()
      if not key3Pressed:
         illustrator.button3Defect()
      if not key4Pressed:
         illustrator.button4Defect()
  else:
      illustrator.hardwareOk()



except KeyboardInterrupt:
    exit()