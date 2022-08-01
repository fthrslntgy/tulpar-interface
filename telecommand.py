import serial
import serial.tools.list_ports
import constants as cns


class Telecommand:

    def __init__(self, widget):

        self.widget = widget
        self.ser = serial.Serial()

    def connect(self, port, baud):

        self.portName = port
        self.baudrate = baud

        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
            print("TELE Connected : ", self.portName)
            return True

        except serial.serialutil.SerialException:
            print("TELE Can't open : ", self.portName)
            return False

    def disconnect(self):

        if self.ser.isOpen():
            self.ser.close()
            print("TELE Disconnected : ", self.portName)

    def sendTelecommand(self, telecommand):

        index = telecommand.index(".")
        selected = int(telecommand[0:index])

        if selected == 1:
            self.ser.write(b'\x00')
        elif selected == 2:
            self.ser.write(b'\x01')
        elif selected == 3:
            self.ser.write(b'\x02')
        elif selected == 4:
            self.ser.write(b'\x03')
        elif selected == 5:
            self.ser.write(b'\x04')
        elif selected == 6:
            self.ser.write(b'\x05')
        elif selected == 7:
            self.ser.write(b'\x06')
        elif selected == 8:
            self.ser.write(b'\x07')

    def sendServoOpen(self):

        self.ser.write(b'\x08')

    def sendServoClose(self):

        self.ser.write(b'\x09')

    def sendEngineRun(self, throttle):

        value = throttle + 128
        byte = bytes([value])
        self.ser.write(byte)

    def sendEngineStop(self):

        self.ser.write(b'\x0A')
