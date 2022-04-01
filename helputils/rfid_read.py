#!/usr/bin/env python

import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import RPi.GPIO as GPIO
from simplemfrc import SimpleMFRC522

reader = SimpleMFRC522()

try:
  id, text = reader.read()
  print(id)
  print(text)
finally:
  GPIO.cleanup()
