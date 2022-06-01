# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import struct
import serial.tools.list_ports


from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt
from PySide2.QtUiTools import loadUiType

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "form.ui"))


class Widget(Base, Form):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.image = None
        self.setWindowIcon(QIcon("logo.ico"))
        self.setWindowTitle("TULPAR Model Uydu Takımı")

        dark_palette = QPalette();
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

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
