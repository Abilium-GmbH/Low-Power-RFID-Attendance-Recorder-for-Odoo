#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from lib.simplemfrc import SimpleMFRC522
from lib.waveshare_epd import epd2in7
from os import path
from PIL import Image,ImageDraw,ImageFont
from gpiozero import Button
import time
resources = path.join(path.dirname(__file__), "..", "resources")
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

def writeTextOnEpaper(text):
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((epd.height/2-100, epd.width/2-15), text, font = font18, fill = 0)
    epd.display(epd.getbuffer(Himage))

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON1_GPIO, GPIO.FALLING,callback=button1_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON2_GPIO, GPIO.FALLING,callback=button2_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON3_GPIO, GPIO.FALLING,callback=button3_pressed_callback, bouncetime=100)
GPIO.add_event_detect(BUTTON4_GPIO, GPIO.FALLING,callback=button4_pressed_callback, bouncetime=100)

#Test display
font18 = ImageFont.truetype(path.join(resources,"Font.ttc"), 18) 
epd.init()
writeTextOnEpaper('The Display works')
writeTextOnEpaper('You have 3s per step')
epd.sleep()

#Test Buttons 
epd.init()
writeTextOnEpaper('Press button 1')
time.sleep(3)
if key1Pressed:
    writeTextOnEpaper('button 1 works')
else:
    writeTextOnEpaper('button 1 does not work')
time.sleep(3)

writeTextOnEpaper('Press button 2')
time.sleep(3)
if key2Pressed:
    writeTextOnEpaper('button 2 works')
else:
    writeTextOnEpaper('button 2 does not work')
time.sleep(3)

writeTextOnEpaper('Press button 3')
time.sleep(3)
if key3Pressed:
    writeTextOnEpaper('button 3 works')
else:
    writeTextOnEpaper('button 3 does not work')
time.sleep(3)

writeTextOnEpaper('Press button 4')
time.sleep(3)
if key4Pressed:
    writeTextOnEpaper('button 4 works')
else:
    writeTextOnEpaper('button 4 does not work')
time.sleep(3)
epd.sleep()

#Test RFID scanner
reader = SimpleMFRC522()
writeTextOnEpaper('Hold a RFID tag to the reader')
time.sleep(3)
try:
  id, text = reader.read()
  writeTextOnEpaper('RFID works if this is ID:')
  time.sleep(3)
  writeTextOnEpaper('Your ID: ' + id)
finally:
  GPIO.cleanup()

time.sleep(3)
writeTextOnEpaper('Test is now over')