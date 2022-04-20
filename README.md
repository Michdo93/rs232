# rs232
A simple python handler for rs232 devices

```
git clone https://github.com/Michdo93/rs232.git
cd rs232
sudo chmod +x rs232.py
python3 -m pip install pyserial
python3 rs232.py
```

As example with my 4K Matrix 4x4 HDMI:

```
python3 rs232.py --port /dev/ttyUSB0 --baudrate 9600 --parity "None" --stopbits 1.0 --bytesize 8 --read "cir 01"
```
