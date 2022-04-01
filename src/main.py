#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from lib.simplemfrc import SimpleMFRC522
from lib.waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
import xmlrpc.client
import json
from os import environ,path

resources = path.join(path.dirname(__file__),"resources")


epd = epd2in7.EPD()
# odoo authentification with server
url = 'https://rostmytomato.odoo.com'
db = 'rostmytomato'
username = 'autorfidcard@informee.ch'
password= environ['ODOO_PASSWORD']  # set on linux with: export ODOO_PASSWORD=< password >
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), allow_none=True) # authentification Endpoint
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), allow_none=True) # this Endpoint allows to call methods of odoo models with execute_kw

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

    # updates time (currently only if token is read and at the start)
    now = datetime.utcnow()
    times = now.strftime("%Y-%m-%d %H:%M:%S")

    emp_id = models.execute(db, uid, password, 'hr.employee', 'search', [('barcode','=', str(id))]) # get employee id
    namea = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [], {'fields':['name']}) # get all employee names
    namep = 0
    for item in namea: # find employee name in a list of all employee names (maybe a problem with people with the same name)
       if list(item.values())[0] == emp_id[0]:
           namep =  list(item.values())[1]
    temp_id = models.execute(db, uid, password, 'hr.attendance', 'search', [('check_out','=', None), ('employee_id', '=', emp_id[0])])
    if(temp_id): # employee checked-in case
      try:
        models.execute_kw(db, uid, password, 'hr.attendance', 'write', [temp_id,{'check_out': str(times)}] ) # checks-out the employee
      except Exception as e:
        pass
        # do nothing
      # draw check-out image
      epd.init()
      Himage = Image.new('1', (epd.height, epd.width), 255)
      draw = ImageDraw.Draw(Himage)
      draw.text((epd.height/2-70, epd.width/2-15), 'Tschuess ' + namep, font = font18, fill = 0)
      #draw.text((epd.height/2-85, epd.width/2+20), 'Ausgecheckt !', font = font18, fill = 0)
      epd.display(epd.getbuffer(Himage))

    else: # employee checked-out case
      attn_record = {'employee_id': emp_id[0], 'check_in': str(times)} # select employee with id of the token
      models.execute(db, uid, password, 'hr.attendance', 'create', attn_record) # checks-in the employee
      # draw check-in image
      epd.init()
      Himage = Image.new('1', (epd.height, epd.width), 255)
      draw = ImageDraw.Draw(Himage)
      draw.text((epd.height/2-70, epd.width/2-15), 'Hallo    ' + namep, font = font18, fill = 0)
      #draw.text((epd.height/2-85, epd.width/2+20), 'Eingecheckt !', font = font18, fill = 0)
      epd.display(epd.getbuffer(Himage))
    time.sleep(5)

except KeyboardInterrupt:
    # epd2in7.epdconfig.module_exit()
    exit()
