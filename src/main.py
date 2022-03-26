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
from datetime import datetime
import xmlrpc.client
import json
from os import environ


epd = epd2in7.EPD()

url = 'https://rostmytomato.odoo.com'
db = 'rostmytomato'
username = 'autorfidcard@informee.ch'
password= environ['ODOO_PASSWORD']  # set on linux with: export ODOO_PASSWORD=< password >
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True)

try:
  epd.init() 
  while(True):
    #epd.Clear(0xFF)
    font18 = ImageFont.truetype('Font.ttc', 18)
    Himage = Image.open('abilium.bmp')
    #Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    draw.text((epd.height/2-90, epd.width/2-70), 'Bitte Karte einfuehren.', font = font18, fill = 0)
    now = datetime.utcnow()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    draw.text((epd.height/2-68, epd.width/2+55), dt_string, font = font18, fill = 0)
    epd.display(epd.getbuffer(Himage))
    epd.sleep()
    reader = SimpleMFRC522()
    id, text = reader.read()
    now = datetime.utcnow()
    times = now.strftime("%Y-%m-%d %H:%M:%S")
    emp_id = models.execute(db, uid, password, 'hr.employee', 'search', [('barcode','=', str(id))])
    namea = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [], {'fields':['name']})
    namep = 0
    for item in namea:
       if list(item.values())[0] == emp_id[0]:
           namep =  list(item.values())[1]
    temp_id = models.execute(db, uid, password, 'hr.attendance', 'search', [('check_out','=', None), ('employee_id', '=', emp_id[0])])
    if(temp_id):
      try:
        models.execute_kw(db, uid, password, 'hr.attendance', 'write', [temp_id,{'check_out': str(times)}] )
      except Exception as e:
        pass
        # do nothing
      epd.init()
      Himage = Image.new('1', (epd.height, epd.width), 255)
      draw = ImageDraw.Draw(Himage)
      draw.text((epd.height/2-70, epd.width/2-15), 'Tschuess ' + namep, font = font18, fill = 0)
      #draw.text((epd.height/2-85, epd.width/2+20), 'Ausgecheckt !', font = font18, fill = 0)
      epd.display(epd.getbuffer(Himage))
    else:
      attn_record = {'employee_id': emp_id[0], 'check_in': str(times)}
      models.execute(db, uid, password, 'hr.attendance', 'create', attn_record)
      epd.init()
      Himage = Image.new('1', (epd.height, epd.width), 255)
      draw = ImageDraw.Draw(Himage)
      draw.text((epd.height/2-70, epd.width/2-15), 'Hallo    ' + namep, font = font18, fill = 0)
      #draw.text((epd.height/2-85, epd.width/2+20), 'Eingecheckt !', font = font18, fill = 0)
      epd.display(epd.getbuffer(Himage))
    time.sleep(5)

except KeyboardInterrupt:
    epd2in7.epdconfig.module_exit()
    exit()
