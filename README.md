# Low-Power-RFID-Attendance-Recorder-for-Odoo

## Setup Raspberry PI
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
6. Connect to the raspberry using ssh pi@IP-ADDRESS and password 'raspberry'
7. Run sudo raspi-config and enable interface SPI
8. Change the password with the following commands and inputs, write a secure password instead of 'new-password' 
```console
passwd
rasberry
new-password
```

## Setup display and RFID
1. Run command
```console
git clone https://github.com/Abilium-GmbH/Low-Power-RFID-Attendance-Recorder-for-Odoo.git
```
2. Run the following commands
```console
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo apt-get install python3-venv
sudo apt-get install python3-rpi.gpio python-pil python-smbus python-dev libopenjp2-7
sudo pip3 install RPi.GPIO
sudo pip3 install gpiozero netifaces spidev rpi.gpio pillow
sudo pip3 install mfrc522
```

## Test Hardware
1. Run commands
```console
cd Low-Power-RFID-Attendance-Recorder-for-Odoo/src
python testHardware.py
```
2. Follow the instructions written on the display to see if the hardware works

## References
- WaveShare 2.7Inch e-Paper Display Wiki https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)
- MFRC522 library https://github.com/pimylifeup/MFRC522-python
- MFRC522 datasheet https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf
- Raspberry PI 4 Pinout https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png
- RFC522 Board Tutorial https://pimylifeup.com/raspberry-pi-rfid-rc522/
