import argparse
import sys
import time
import serial
from serial import SerialException
import io

def main(read, write, port, baudrate, parity, stopbits, bytesize):
    if len(read) == 0:
        read = None
    else:
        read = read

    if len(write) == 0:
        write = None
    else:
        write = write

    if read is None and write is None:
        raise ValueError("You must either read or write. Both cannot be empty.")

    if read is not None and write is not None:
        raise ValueError("You must either read or write. Both cannot be empty. Both cannot be used at the same time.")

    if port == "":
        port = "/dev/ttyUSB0"
    else:
        port = port

    if baudrate == None:
        baudrate = 9600
    else:
        if baudrate == 9600 or baudrate == 14400 or baudrate == 19200 or baudrate == 38400 or baudrate == 57600 or baudrate == 115200:
            baudrate = baudrate
        else:
            raise ValueError("Please enter valid baudrates like 9600, 14400, 19200, 38400, 57600, 115200 (bps).")

    if parity == "None":
        parity = serial.PARITY_NONE
    elif parity == "Even":
        parity = serial.PARITY_EVEN
    elif parity == "Odd":
        parity = serial.PARITY_ODD
    elif parity == "Mark":
        parity = serial.PARITY_MARK
    elif parity == "Space":
        parity = serial.PARITY_SPACE
    else:
        raise ValueError("If nothing else is defined, the parity check is disabled with None. Possible values are None, Even, Odd, Mark or Space.")

    if stopbits == 1.0:
        stopbits = serial.STOPBITS_ONE
    elif stopbits == 1.5:
        stopbits = serial.STOPBITS_ONE_POINT_FIVE
    elif stopbits == 2.0:
        stopbits = serial.STOPBITS_TWO
    else:
        raise ValueError("If nothing else is defined, 1.0 will be used. Posible values are 1.0, 1.5 or 2.0.")

    if bytesize == 5:
        bytesize = serial.FIVEBITS
    elif bytesize == 6:
        bytesize = serial.SIXBITS
    elif bytesize == 7:
        bytesize = serial.SEVENBITS
    elif bytesize == 8:
        bytesize = serial.EIGHTBITS
    else:
        raise ValueError("If nothing else is defined, 8 will be used. Possible values are 5, 6, 7 or 8.")

    # configure the serial connections (the parameters differs on the device you are connecting to)
    ser = serial.Serial(
        port=port,
        baudrate=baudrate,
        parity=parity,
        stopbits=stopbits,
        bytesize=bytesize
    )

    if read:
        operate(ser, read)
    elif write:
        operate(ser, write)

def portIsUsable(portName):
    try:
       ser = serial.Serial(port=portName)
       return True
    except:
        return False

def operate(serial, command):
    while True:
        if portIsUsable(serial.port):
            serial.isOpen()
            break
        time.sleep(1)

    try:
        while True:
            if command == "exit":
                serial.flushInput()
                serial.flushOutput()
                serial.close()
                exit()
            else:
                # send the character to the device
                # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
                serial.write((command + "\r\n").encode())

                # let's wait one second before reading output (let's give device time to answer)
                time.sleep(1)

                while True:
                    data_raw = serial.readline()
                    print(data_raw.decode('utf-8'))
                    break
                serial.flushInput()
                serial.flushOutput()
                serial.close()
                break
    except SerialException:
        print('port already open')
    finally:
        serial.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--read", type=str, default="", help="Uses rs232 to read from device (as example a state)", required=False)
    parser.add_argument("--write", type=str, default="", help="Uses rs232 to write to device (as example a command)", required=False)
    parser.add_argument("--port", type=str, default="/dev/ttyUSB0", help="Specifies which port is to be used for the RS232 interface. If nothing else is defined, /dev/ttyUSB0 is used.", required=True)
    parser.add_argument("--baudrate", type=int, default=9600, help="Specifies the baudrate which will be used for the RS232 interface. If nothing else is defined, 9600 is used. Please enter valid baudrates like 9600, 14400, 19200, 38400, 57600, 115200 (bps).", required=True)
    parser.add_argument("--parity", type=str, default="None", help="Specifies the parity checking. If nothing else is defined, the parity check is disabled with None. Possible values are None, Even, Odd, Mark or Space.", required=True)
    parser.add_argument("--stopbits", type=float, default=1.0, help="Specifies the number of stop bits. If nothing else is defined, 1.0 will be used. Posible values are 1.0, 1.5 or 2.0.", required=True)
    parser.add_argument("--bytesize", type=int, default=8, help="Specifies the number of data bits. If nothing else is defined, 8 will be used. Possible values are 5, 6, 7 or 8.", required=True)
    parser.add_argument("--timeout", type=float, default=None, help="Set a read timeout value in seconds.", required=False)
    parser.add_argument("--xonxoff", type=bool, default=None, help="Enable software flow control.", required=False)
    parser.add_argument("--rtscts", type=bool, default=None, help="Enable hardware (RTS/CTS) flow control.", required=False)
    parser.add_argument("--dsrdtr", type=bool, default=None, help="Enable hardware (DSR/DTR) flow control.", required=False)
    parser.add_argument("--write_timeout", type=float, default=None, help="Set a write timeout value in seconds.", required=False)
    parser.add_argument("--inter_byte_timeout", type=float, default=None, help="Inter-character timeout, None to disable (default).", required=False)
    parser.add_argument("--exclusive", type=bool, default=None, help="Set exclusive access mode (POSIX only). A port cannot be opened in exclusive access mode if it is already open in exclusive access mode.", required=False)

    args = parser.parse_args()
    main(args.read, args.write, args.port, args.baudrate, args.parity, args.stopbits, args.bytesize)
