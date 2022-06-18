# This Python file uses the following encoding: utf-8
import os
import serial.tools.list_ports
import threading
import csv
from time import strftime
from pathlib import Path

from PySide2.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView, QMessageBox, QFileDialog
from PySide2.QtCore import QFile, QRect
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt
from PySide2.QtUiTools import loadUiType

from communication import Communication
from telemetry_table import TelemetryTable
from graphs import Graphs
import constants as cns

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, cns.UI_FILE))

output_dir = os.path.join(current_dir, r'output_files')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


class Widget(Base, Form):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        # Main window options
        self.image = None
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.setWindowTitle(cns.MAIN_TITLE)
        self.setFixedSize(cns.MAIN_WIDTH, cns.MAIN_HEIGHT)
        self.setWindowOpacity(cns.MAIN_OPACITY)

        # Palette options
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

        # Logo component
        self.logo.setStyleSheet("background: url(images/logo.jpg)")

        # Port and baud components
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])
        for element in cns.MAIN_BAUDS:
            self.combobox_bauds.addItem(element)
        self.button_refresh.setIcon(QIcon("images/refresh.png"))
        self.button_refresh.clicked.connect(self.refreshPorts)

        # Connect button component
        self.button_connection.setStyleSheet("background-color: green")
        self.button_connection.clicked.connect(self.connection)

        # Telemetry table component
        self.table_telemetry = TelemetryTable(self)
        self.table_telemetry.setStyleSheet("background-color: white")
        self.table_telemetry.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_telemetry.setGeometry(QRect(cns.TABLE_X, cns.TABLE_Y, cns.TABLE_WIDTH, cns.TABLE_HEIGHT))

        # Status components
        for element in cns.SAT_STATUS_VARS:
            self.combobox_command.addItem(element)
        self.button_sendcommand.clicked.connect(self.send_telecommand)

        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("background-color: red; font-size: 10pt; font-weight: bold;")
        self.label_status.setText("UNCONNECTED")

        # Video send components
        self.button_select_video.clicked.connect(self.uploadVideo)

        # Gyro and height_diff compontents
        self.label_gyro.setAlignment(Qt.AlignCenter)
        self.label_gyro.setStyleSheet("background-color: darkred; font-size: 8pt; font-weight: bold; color: white")
        self.label_height_diff.setAlignment(Qt.AlignCenter)
        self.label_height_diff.setStyleSheet("background-color: darkred; font-size: 10pt; font-weight: bold; color: white")
        self.label_video_status.setAlignment(Qt.AlignCenter)
        self.label_video_status.setStyleSheet("background-color: black; font-size: 8pt; font-weight: bold; color: white")
        self.label_video_status.setText("Aktarım Durumu: -")

        # Graph components
        self.graphs = Graphs(self)

        # Global variables about connection status
        global com, first_connect, connected, quit
        first_connect = True
        connected = False
        quit = False

    def uploadVideo(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if fileName != '':
            self.lineedit_select_video.setText(fileName)

    def send_telecommand(self):

        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)
        telecommand = self.combobox_command.currentText()
        index = telecommand.index(".")
        selected = int(telecommand[0:index])

        if selected == 1:
            ser.write(b'\x00')
        elif selected == 2:
            ser.write(b'\x01')
        elif selected == 3:
            ser.write(b'\x02')
        elif selected == 4:
            ser.write(b'\x03')
        elif selected == 5:
            ser.write(b'\x04')
        elif selected == 6:
            ser.write(b'\x05')
        elif selected == 7:
            ser.write(b'\x06')
        elif selected == 8:
            ser.write(b'\x07')
        elif selected == 9:
            ser.write(b'\x08')
        elif selected == 10:
            ser.write(b'\x09')
        elif selected == 11:
            throttle = self.spinbox_value.value()
            value = throttle + 128
            byte = bytes([value])
            ser.write(byte)
        elif selected == 12:
            ser.write(b'\x0A')
        ser.close()

    def load_ui(self):

        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / cns.UI_FILE)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def closeEvent(self, event):

        global quit
        close = QMessageBox.question(self, cns.MAIN_EXIT_TITLE, cns.MAIN_EXIT_MESSAGE, QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            quit = True
            event.accept()
            self.connection()
        else:
            quit = False
            event.ignore()

    def refreshPorts(self):

        self.combobox_ports.clear()
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])

    def addRow(self, list):

        numRows = self.table_telemetry.rowCount() - 1
        self.table_telemetry.insertRow(numRows)

        i = 0
        for item in list:
            self.table_telemetry.setItem(numRows, i, QTableWidgetItem(str(item)))
            i = i+1
        self.table_telemetry.scrollToBottom()

    def setStatus(self, stat):

        self.label_status.setText(cns.SAT_STATUS_VARS[stat])

    def setPRY(self, pitch, roll, yaw):

        text = "PITCH: " + str(pitch) + " ROLL: " + str(roll) + " YAW: " + str(yaw)
        self.label_gyro.setText(text)

    def setHeightDiff(self, height_diff):

        text = "Yükseklik Farkı: " + str(height_diff)
        self.label_height_diff.setText(text)

    def setVideoStatus(self, status):

        if status == 0:
            self.label_video_status.setText("Aktarım Durumu: Evet")
        else:
            self.label_video_status.setText("Aktarım Durumu: Hayır")

    def connection(self):

        global com, first_connect, connected, quit

        if quit and connected:
            com.disconnect()

        elif quit:
            return

        elif first_connect:
            port = self.combobox_ports.currentText()
            baud = self.combobox_bauds.currentText()
            com = Communication(port, baud, self)
            if com.connect():
                self.session_directory = output_dir + strftime("/%Y-%m-%d_%H%M%S")
                os.makedirs(self.session_directory)
                with open(self.session_directory + "/Telemetry.csv", 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerow(cns.TABLE_TITLE)
                first_connect = False
                connected = True
                self.button_connection.setStyleSheet("background-color: red")
                self.button_connection.setText(cns.MAIN_DISCONNECT)
                self.label_status.setStyleSheet("background-color: green; font-size: 12pt; font-weight: bold;")
                self.label_status.setText("CONNECTED")
                t1 = threading.Thread(target=com.getData)
                t1.start()

        else:
            isConnected = com.q
            if not isConnected:
                port = self.combobox_ports.currentText()
                baud = self.combobox_bauds.currentText()
                com = Communication(port, baud, self)
                if com.connect():
                    self.session_directory = output_dir + strftime("/%Y-%m-%d_%H%M%S")
                    os.makedirs(self.session_directory)
                    with open(self.session_directory + "/Telemetry.csv", 'w', newline='') as file:
                        writer = csv.writer(file, delimiter=',')
                        writer.writerow(cns.TABLE_TITLE)
                    connected = True
                    self.button_connection.setStyleSheet("background-color: red")
                    self.button_connection.setText(cns.MAIN_DISCONNECT)
                    self.label_status.setStyleSheet("background-color: green; font-size: 12pt; font-weight: bold;")
                    self.label_status.setText("CONNECTED")
                    t1 = threading.Thread(target=com.getData)
                    t1.start()

            else:
                com.disconnect()
                connected = False
                self.button_connection.setStyleSheet("background-color: green")
                self.button_connection.setText(cns.MAIN_CONNECT)
                self.label_status.setStyleSheet("background-color: red; font-size: 12pt; font-weight: bold;")
                self.label_status.setText("UNCONNECTED")


def main():

    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()


if __name__ == "__main__":

    main()
