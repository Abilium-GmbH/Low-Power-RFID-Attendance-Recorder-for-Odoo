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
sudo apt-get install libgl1-mesa-glx
sudo pip3 install RPi.GPIO
sudo pip3 install gpiozero netifaces spidev rpi.gpio pillow
sudo pip3 install mfrc522
sudo pip3 install opencv-python
```

## Connect with Odoo
There are two ways to connect the project with the odoo server:

1. Enter the directory for enviroment variables
```console
sudo nano etc/environment
```
2. Add the following lines with the information of the relevant odoo server. This is possible with API keys or hardcoded letters
```console
ODOO_URL="YOUR-URL"
ODOO_USERNAME="YOUR-USERNAME"
ODOO_DB="DATABASE_NAME"
ODOO_PASSWORD="YOUR_PASSWORD"
```
3. Save the file and test with the commands below
```console
echo $ODOO_URL
echo $ODOO_USERNAME
echo $ODOO_DB
echo $ODOO_PASSWORD
```

The second variant works by hardcoding the information into the responsible file

1. Run the following commands
```console
cd Low-Power-RFID-Attendance-Recorder-for-Odoo/src/odoo
sudo nano interpreter.py
```
2. Write the information from the server into the init method instead of the enviroment variables. They are marked with the comments.
```python
    def __init__(self) -> None:
        url = environ['ODOO_URL'] #"YOUR-URL"
        user = environ['ODOO_USERNAME'] #"YOUR-USERNAME"
        self.db = environ['ODOO_DB'] #"DATABASE_NAME"
        self.password = environ['ODOO_PASSWORD'] #"YOUR_PASSWORD"
        self.common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url), allow_none=True)
        self.uid = self.common.authenticate(self.db, user, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url),
                                                allow_none=True) 
```
3. Save the file and quit it

FOR BOTH VARIANTS IMPORTANT!

Save the number of the card of an employee into odoo as the Badge ID

## Test Hardware
1. Run commands
```console
cd Low-Power-RFID-Attendance-Recorder-for-Odoo/src
python testHardware.py
```
2. Follow the instructions written on the display to see if the hardware works

## How to use the attendance recorder
1. Hold the Badge or Token near to the scanner to Check-In or to Check-Out. Just to state the obvious: If an employee is Checked-Out this will Check the employee In and vice versa. It is still possible to manually Check-In or Out by connecting to odoo.

2. Holding a Badge or Token near the RFID-Reader while pressing one of the four buttons will lead to the following results. They are labeled from top to bottom.
    1. By pressing the first button one can see whether an employee is Checked-In or Out
    2. By pressing the second button one can see the IP-Address of the device.

## References
- WaveShare 2.7Inch e-Paper Display Wiki https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)
- MFRC522 library https://github.com/pimylifeup/MFRC522-python
- MFRC522 datasheet https://www.nxp.com/docs/en/data-sheet/MFRC522.pdf
- Raspberry PI 4 Pinout https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png
- RFC522 Board Tutorial https://pimylifeup.com/raspberry-pi-rfid-rc522/
