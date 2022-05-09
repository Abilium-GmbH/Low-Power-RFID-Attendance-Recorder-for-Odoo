#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from datetime import timedelta
from odoo.interpreter import Interpreter
from os import path

odoo_handler = Interpreter()

odoo_handler.getLogoTest()
