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
2. Create an example file
```console
cd ~/pi-rfid
sudo nano rfid_read.py
```
3. Insert the following code
```python
#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

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
