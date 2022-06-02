# This Python file uses the following encoding: utf-8
import os
import sys
import struct
import serial.tools.list_ports
import threading
from pathlib import Path

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt
from PySide2.QtUiTools import loadUiType

from communication import Communication

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "form.ui"))


class Widget(Base, Form):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.image = None
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowTitle("TULPAR Model Uydu Takımı")

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
        self.setPalette(dark_palette)

        self.setMinimumSize(1083, 621)
        self.setMaximumSize(1083, 621)
        self.setWindowOpacity(0.95)

        self.logo.setStyleSheet("background: url(logo.jpg)")

        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.ports_combobox.addItem(str(element).split()[0])
        self.baud_combobox.addItem("2400".split()[0])
        self.baud_combobox.addItem("4800".split()[0])
        self.baud_combobox.addItem("9600".split()[0])
        self.baud_combobox.addItem("14400".split()[0])
        self.baud_combobox.addItem("19200".split()[0])
        self.baud_combobox.addItem("28800".split()[0])
        self.baud_combobox.addItem("38400".split()[0])
        self.baud_combobox.addItem("57600".split()[0])
        self.baud_combobox.addItem("115200".split()[0])
        self.button_connect.setStyleSheet("background-color: green")

        self.button_connect.clicked.connect(self.connect)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def connect(self):

        global com

        port = self.ports_combobox.currentText()
        baud = self.baud_combobox.currentText()
        com = Communication(port, baud, self)
        isConnected = com.connect()

        if isConnected:
            t1 = threading.Thread(target=com.getData)
            t1.start()

    def pckParser(self, line):
        # header = line[0] + line[1]
        length = line[2]
        length = int.from_bytes(length, "little", signed=False)

        takim_no = line[3] + line[4]
        takim_no = int.from_bytes(takim_no, "little", signed=False)

        paket_no = line[5] + line[6]
        paket_no = int.from_bytes(paket_no, "little", signed=False)
        day = line[7]
        day = int.from_bytes(day, "little", signed=False)
        month = line[8]
        month = int.from_bytes(month, "little", signed=False)
        year = line[9]
        year = int.from_bytes(year, "little", signed=False)
        hour = line[10]
        hour = int.from_bytes(hour, "little", signed=False)
        minute = line[11]
        minute = int.from_bytes(minute, "little", signed=False)
        second = line[12]
        second = int.from_bytes(second, "little", signed=False)

        pressure_pl = line[13] + line[14] + line[15] + line[16]
        [pressure_pl] = struct.unpack("f", pressure_pl)
        pressure_car = line[17] + line[18] + line[19] + line[20]
        [pressure_car] = struct.unpack("f", pressure_car)

        height_pl = line[21] + line[22] + line[23] + line[24]
        [height_pl] = struct.unpack("f", height_pl)
        height_car = line[25] + line[26] + line[27] + line[28]
        [height_car] = struct.unpack("f", height_car)
        height_diff = line[29] + line[30] + line[31] + line[32]
        [height_diff] = struct.unpack("f", height_diff)

        speed = line[33] + line[34] + line[35] + line[36]
        [speed] = struct.unpack("f", speed)
        tempe = line[37] + line[38] + line[39] + line[40]
        [tempe] = struct.unpack("f", tempe)
        b_voltage = line[41] + line[42] + line[43] + line[44]
        [b_voltage] = struct.unpack("f", b_voltage)

        latitude_pl = line[45] + line[46] + line[47] + line[48]
        [latitude_pl] = struct.unpack("f", latitude_pl)
        longitude_pl = line[49] + line[50] + line[51] + line[52]
        [longitude_pl] = struct.unpack("f", longitude_pl)
        altitude_pl = line[53] + line[54] + line[55] + line[56]
        [altitude_pl] = struct.unpack("f", altitude_pl)

        altitude_car = line[57] + line[58] + line[59] + line[60]
        [altitude_car] = struct.unpack("f", altitude_car)
        latitude_car = line[61] + line[62] + line[63] + line[64]
        [latitude_car] = struct.unpack("f", latitude_car)
        longitude_car = line[65] + line[66] + line[67] + line[68]
        [longitude_car] = struct.unpack("f", longitude_car)

        status = line[69]
        status = int.from_bytes(status, "little", signed=False)
        yaw = line[70]+line[71]+line[72]+line[73]
        [yaw] = struct.unpack("f", yaw)
        roll = line[74]+line[75]+line[76]+line[77]
        [roll] = struct.unpack("f", roll)
        pitch = line[78]+line[79]+line[80]+line[81]
        [pitch] = struct.unpack("f", pitch)
        return_number = line[82]
        return_number = int.from_bytes(return_number, "little", signed=False)
        video_status = line[83]
        video_status = int.from_bytes(video_status, "little", signed=False)
        weather_forecast = line[84]
        weather_forecast = int.from_bytes(weather_forecast, "little", signed=False)
        # finish = line[85:87]
        # crc = line[87]

        row = []
        row.append(takim_no)
        row.append(paket_no)
        date = str(hour) + ":" + str(minute) + ":" + str(second) + " " + str(day) + "/" + str(month) + "/" + str(year)
        row.append(date)
        row.append(float("{:.2f}".format(pressure_pl)))
        row.append(float("{:.2f}".format(pressure_car)))
        row.append(float("{:.2f}".format(height_pl)))
        row.append(float("{:.2f}".format(height_car)))
        row.append(float("{:.2f}".format(height_diff)))
        row.append(float("{:.2f}".format(speed)))
        row.append(float("{:.2f}".format(tempe)))
        row.append(float("{:.2f}".format(b_voltage)))
        row.append(float("{:.2f}".format(latitude_pl)))
        row.append(float("{:.2f}".format(altitude_pl)))
        row.append(float("{:.2f}".format(latitude_pl)))
        row.append(float("{:.2f}".format(latitude_car)))
        row.append(float("{:.2f}".format(altitude_car)))
        row.append(float("{:.2f}".format(latitude_car)))
        row.append(status)
        row.append(float("{:.2f}".format(yaw)))
        row.append(float("{:.2f}".format(roll)))
        row.append(float("{:.2f}".format(pitch)))
        row.append(return_number)
        row.append(video_status)
        row.append(weather_forecast)
        print(row)


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
