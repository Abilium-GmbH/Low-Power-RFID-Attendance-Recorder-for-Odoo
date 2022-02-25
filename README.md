# Low-Power-RFID-Attendance-Recorder-for-Odoo

## Setup
1. Flash raspberry OS to microSD card using https://www.raspberrypi.com/software/
2. Create a file called 'ssh' on microSD card root
3. Create a file called 'wpa_supplicant.conf' on microSD card root containing the following lines, change SSID and password to your WLAN
```console
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
ssid="SSID"
psk="password"
key_mgmt=WPA-PSK
}
```
4. Insert microSD card into the raspberri PI and power it up using USB-C cable
5. Scan the IPs in your network for the raspberri PI
6. Connect to the raspberry using ssh pi@<IP-ADDR> and password 'raspberry'
7. Run sudo raspi-config and enable interface SPI

## Test display
1. Run command
```console
git clone https://github.com/waveshare/e-Paper.git
```
2. Run the following commands
```console
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
```
3. Run example
```console
cd e-Paper/RaspberryPi_JetsonNano/python/examples/
python epd_2in7_test.py
```
## Test RFID
1. Install the library
```console
sudo pip3 install mfrc522
```
2. Create the simplemfrc library file (this library contains the selection of the correct Slave-Select pin)
```console
sudo nano simplemfrc.py
```
3. Insert the following code
```python
from mfrc522 import MFRC522
import RPi.GPIO as GPIO
  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [8, 9, 10]
  
  def __init__(self):
    self.READER = MFRC522(device=1) # device defines slave select pin, CE0 used for display, CE1 used for RFID
  
  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)
  
  def read_no_block(self):
    (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.MFRC522_SelectTag(uid)
    status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in self.BLOCK_ADDRS:
            block = self.READER.MFRC522_Read(block_num) 
            if block:
                        data += block
        if data:
             text_read = ''.join(chr(i) for i in data)
    self.READER.MFRC522_StopCrypto1()
    return id, text_read
    
  def write(self, text):
      id, text_in = self.write_no_block(text)
      while not id:
          id, text_in = self.write_no_block(text)
      return id, text_in

  def write_no_block(self, text):
      (status, TagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.MFRC522_Anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.MFRC522_SelectTag(uid)
      status = self.READER.MFRC522_Auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
      self.READER.MFRC522_Read(11)
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
          i = 0
          for block_num in self.BLOCK_ADDRS:
            self.READER.MFRC522_Write(block_num, data[(i*16):(i+1)*16])
            i += 1
      self.READER.MFRC522_StopCrypto1()
      return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n

```
2. Create an example file
```console
sudo nano rfid_read.py
```
3. Insert the following code
```python
#!/usr/bin/env python

import RPi.GPIO as GPIO
from simplemfrc import SimpleMFRC522

reader = SimpleMFRC522()

try:
  id, text = reader.read()
  print(id)
  print(text)
finally:
  GPIO.cleanup()
```
4. Save the file and run it:
```console
python rfid_read.py
```
5. Hold an RFID tag to the reader and see it's ID

