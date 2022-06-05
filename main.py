# This Python file uses the following encoding: utf-8
import os
import serial.tools.list_ports
import threading
from pathlib import Path

from PySide2.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView, QMessageBox
from PySide2.QtCore import QFile, QRect
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt
from PySide2.QtUiTools import loadUiType

from communication import Communication
from telemetry_table import TelemetryTable

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "form.ui"))


class Widget(Base, Form):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        # Main window options
        self.image = None
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.setWindowTitle("TULPAR Model Uydu Takımı")
        self.setFixedSize(1083, 621)
        self.setWindowOpacity(0.95)

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
        self.combobox_bauds.addItem("2400".split()[0])
        self.combobox_bauds.addItem("4800".split()[0])
        self.combobox_bauds.addItem("9600".split()[0])
        self.combobox_bauds.addItem("14400".split()[0])
        self.combobox_bauds.addItem("19200".split()[0])
        self.combobox_bauds.addItem("28800".split()[0])
        self.combobox_bauds.addItem("38400".split()[0])
        self.combobox_bauds.addItem("57600".split()[0])
        self.combobox_bauds.addItem("115200".split()[0])
        self.button_refresh.setIcon(QIcon("images/refresh.png"))
        self.button_refresh.clicked.connect(self.refreshPorts)

        # Connect button component
        self.button_connection.setStyleSheet("background-color: green")
        self.button_connection.clicked.connect(self.connection)

        # Telemetry table component
        self.table_telemetry = TelemetryTable(self)
        self.table_telemetry.setStyleSheet("background-color: white")
        self.table_telemetry.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_telemetry.setGeometry(QRect(10, 420, 1061, 192))

        global com
        global first_connect
        global connected
        global quit
        first_connect = True
        connected = False
        quit = False

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def closeEvent(self, event):

        global quit
        close = QMessageBox.question(self, "EXIT", "Cikmak istediginizden emin misiniz?", QMessageBox.Yes | QMessageBox.No)
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

    def connection(self):

        global com
        global first_connect
        global connected
        global quit

        if quit and connected:
            com.disconnect()

        elif quit:
            return

        elif first_connect:
            port = self.combobox_ports.currentText()
            baud = self.combobox_bauds.currentText()
            com = Communication(port, baud, self)
            if com.connect():
                first_connect = False
                connected = True
                self.button_connection.setStyleSheet("background-color: red")
                self.button_connection.setText("KES")
                t1 = threading.Thread(target=com.getData)
                t1.start()

        else:
            isConnected = com.q
            if not isConnected:
                port = self.combobox_ports.currentText()
                baud = self.combobox_bauds.currentText()
                com = Communication(port, baud, self)
                if com.connect():
                    connected = True
                    self.button_connection.setStyleSheet("background-color: red")
                    self.button_connection.setText("KES")
                    t1 = threading.Thread(target=com.getData)
                    t1.start()

            else:
                com.disconnect()
                connected = False
                self.button_connection.setStyleSheet("background-color: green")
                self.button_connection.setText("BAĞLAN")


def main():
    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
