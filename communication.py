import random
import serial
import serial.tools.list_ports
from time import sleep

class Communication:

    baudrate = ''
    portName = ''
    widget = ''
    q = 1

    ser = serial.Serial()

    def __init__(self, port, baud, widget):
        self.baudrate = baud
        self.portName = port
        self.widget = widget

    def connect(self):

        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
            print("Connected : ", self.portName)
            self.q = 0
            return True


        except serial.serialutil.SerialException:
            print("Can't open : ", self.portName)
            return False

    def getData(self):

        line = []
        last = b'\x00'
        lastlast = b'\x00'

        while self.q == 0:
            byte = self.ser.read()
            if byte == b'\xcd' and len(line) == 0:
                1 == 1

            elif byte == b'\xab' and last == b'\xcd' and len(line) == 0:
                line.append(last)
                line.append(byte)

            elif byte and last == b'\xdc' and lastlast == b'\xba' and len(line) == 87:
                line.append(byte)
                row = self.widget.pckParser(line)
                line = []
                sleep(1)

            elif byte and len(line) != 0:
                line.append(byte)

            if len(line) >= 88:
                line = []

            lastlast = last
            last = byte


    def close(self):
        if(self.ser.isOpen()):
            self.q = 1
            self.ser.close()
        else:
            print(self.portName, " it's already closed")

