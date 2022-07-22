# This Python file uses the following encoding: utf-8
import os
import io
import serial.tools.list_ports
import threading
import csv
import time
import folium
from time import strftime
from ftplib import FTP
from pathlib import Path

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PySide2.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView, QMessageBox, QFileDialog
from PySide2.QtCore import QFile, QRect
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt, QPixmap, QImage
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtUiTools import loadUiType
from PySide2 import QtCore

from communication import Communication
from telemetry_table import TelemetryTable
from graphs import Graphs
from telecommand import Telecommand
from capture_camera import CaptureCamera
# from model import Model
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

        # Global variables about connection status
        global com, first_connect, connected, tele_connected, quit
        first_connect = True
        connected = False
        tele_connected = False
        quit = False

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

        # Port, baud and connection components
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])
        for element in cns.MAIN_BAUDS:
            self.combobox_bauds.addItem(element)
        self.button_refresh.setIcon(QIcon("images/refresh.png"))
        self.button_refresh.clicked.connect(self.refreshPorts)

        self.telecommand = Telecommand(self)
        self.button_connection.setStyleSheet("background-color: green")
        self.button_connection.clicked.connect(self.connection)
        self.button_connection_tele.clicked.connect(self.tele_connection)

        # Status and telecommand components
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_timer.setAlignment(Qt.AlignCenter)
        self.label_timer.setStyleSheet("background-color: black; color: red; font-size: 14px;font-weight: bold;")

        for element in cns.SAT_STATUS_VARS:
            self.combobox_command.addItem(element)
        self.button_send_command.clicked.connect(lambda: self.telecommand.send_telecommand(self.combobox_command.currentText()))
        self.button_servo_open.clicked.connect(self.telecommand.send_servo_open)
        self.button_servo_close.clicked.connect(self.telecommand.send_servo_close)
        self.button_engine_run.clicked.connect(lambda: self.telecommand.send_engine_run(self.spinbox_value.value()))
        self.button_engine_stop.clicked.connect(self.telecommand.send_engine_stop)

        # Video send components
        self.button_select_video.clicked.connect(self.uploadVideo)
        self.button_send_video.clicked.connect(self.sendVideo)
        self.label_video_status.setAlignment(Qt.AlignCenter)
        self.label_video_status.setStyleSheet("background-color: black; font-size: 8pt; font-weight: bold; color: white")
        self.label_video_status.setText("Aktarım Durumu: -")

        # Logo component
        self.label_logo.setStyleSheet("background: url(images/logo.jpg)")

        # Gyro (model) compontents
        filename = "model.stl"
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(filename)

        self.vl = QVBoxLayout()
        self.frame_model.setLayout(self.vl)
        self.frame_model.setLineWidth(0.6)
        self.frame_model.setStyleSheet("border:1px solid #000000; background-color:#7FD5FF")
        self.coneMapper2 = vtk.vtkPolyDataMapper()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame_model)
        self.vl.addWidget(self.vtkWidget)

        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.ren = vtk.vtkRenderer()
        self.transform = vtk.vtkTransform()
        self.transform.RotateX(-90)
        self.transform.RotateY(0)
        self.transform.RotateZ(0)
        self.transformFilter = vtk.vtkTransformPolyDataFilter()
        self.transformFilter.SetTransform(self.transform)
        self.transformFilter.SetInputConnection(self.reader.GetOutputPort())
        self.transformFilter.Update()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.coneMapper2.SetInput(self.transformFilter.GetOutput())
        else:
            self.coneMapper2.SetInputConnection(self.transformFilter.GetOutputPort())

        self.actor2 = vtk.vtkActor()
        self.actor2.SetMapper(self.coneMapper2)
        self.actor2.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.actor2.SetScale(0.5, 0.5, 0.5)
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.ren.AddActor(self.actor2)
        self.ren.SetBackground(0.496, 0.832, 0.996)
        self.iren.Initialize()
        self.iren.Start()

        self.label_gyro.setAlignment(Qt.AlignCenter)
        self.label_gyro.setStyleSheet("background-color: darkred; font-size: 8pt; font-weight: bold; color: white")

        # Map components
        self.vm = QVBoxLayout()
        coordinates = (39.9211819,32.7983108)
        self.m = folium.Map(tiles='Stamen Terrain', zoom_start=14, location=coordinates)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        self.vm.addWidget(self.webView)
        self.frame_map.setLayout(self.vm)
        self.updateMap(39.9211819,32.7983108)

        self.label_height_diff.setAlignment(Qt.AlignCenter)
        self.label_height_diff.setStyleSheet("background-color: darkred; font-size: 10pt; font-weight: bold; color: white")

        # Graph components
        self.graphs = Graphs(self)

        # Camera component
        self.camurl = "rtsp://10.5.39.149:8554/mjpeg/1"
        self.CaptureCamera = CaptureCamera(self.camurl)
        self.CaptureCamera.ImageUpdated.connect(lambda image: self.ShowCamera(image))
        self.CaptureCamera.start()

        # Telemetry table component
        self.table_telemetry = TelemetryTable(self)
        self.table_telemetry.setStyleSheet("background-color: white")
        self.table_telemetry.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_telemetry.setGeometry(QRect(cns.TABLE_X, cns.TABLE_Y, cns.TABLE_WIDTH, cns.TABLE_HEIGHT))

        # Update buttons
        self.update_buttons()

    def update_buttons(self):

        global connected, tele_connected

        if connected:
            self.button_connection.setStyleSheet("background-color: red")
            self.button_connection.setText(cns.MAIN_DISCONNECT)
            self.label_status.setStyleSheet("background-color: green; font-size: 12pt; font-weight: bold;")
            self.label_status.setText("CONNECTED")
            self.button_select_video.setEnabled(True)
            self.button_connection_tele.setEnabled(True)
            self.button_send_video.setEnabled(True)

            if tele_connected:
                self.button_connection_tele.setStyleSheet("background-color: red")
                self.spinbox_value.setEnabled(True)
                self.combobox_command.setEnabled(True)
                self.button_send_command.setEnabled(True)
                self.button_servo_open.setEnabled(True)
                self.button_servo_close.setEnabled(True)
                self.button_engine_run.setEnabled(True)
                self.button_engine_stop.setEnabled(True)

            else:
                self.button_connection_tele.setStyleSheet("background-color: green")
                self.spinbox_value.setEnabled(False)
                self.combobox_command.setEnabled(False)
                self.button_send_command.setEnabled(False)
                self.button_servo_open.setEnabled(False)
                self.button_servo_close.setEnabled(False)
                self.button_engine_run.setEnabled(False)
                self.button_engine_stop.setEnabled(False)

        else:
            self.button_connection.setStyleSheet("background-color: green")
            self.button_connection.setText(cns.MAIN_CONNECT)
            self.label_status.setStyleSheet("background-color: red; font-size: 12pt; font-weight: bold;")
            self.label_status.setText("UNCONNECTED")
            self.label_timer.setText("UPTIME 00 : 00")
            self.button_select_video.setEnabled(False)
            self.button_send_video.setEnabled(False)

            self.button_connection_tele.setEnabled(False)
            self.button_connection_tele.setStyleSheet("background-color: None")
            self.spinbox_value.setEnabled(False)
            self.combobox_command.setEnabled(False)
            self.button_send_command.setEnabled(False)
            self.button_servo_open.setEnabled(False)
            self.button_servo_close.setEnabled(False)
            self.button_engine_run.setEnabled(False)
            self.button_engine_stop.setEnabled(False)

    def refreshPorts(self):

        self.combobox_ports.clear()
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])

    def timer(self):

        global connected
        for min in range(0, 60):
            if not connected:
                break
            for sec in range(0, 60):
                if not connected:
                    break
                self.label_timer.setText("UPTIME {:02d} : {:02d}".format(min, sec))
                time.sleep(1)

    def uploadVideo(self):

        fileName, _ = QFileDialog.getOpenFileName(self, "Gönderilecek Video Dosyasını Seçiniz", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if fileName != '':
            self.lineedit_select_video.setText(fileName)

    def sendVideo(self):

        file_name = self.lineedit_select_video.text()
        session = FTP('IP', 'USERNAME', 'PASS') # CHANGE!
        file = open(file_name, 'rb')
        session.storbinary('STOR file.mp4', file)
        file.close()
        session.quit()

    def updateMap(self, lat, lon):

        folium.Marker([lat, lon]).add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def ShowCamera(self, frame: QImage) -> None:
        self.label_camera.setPixmap(QPixmap.fromImage(frame))

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

    def setVideoStatus(self, status):

        if status == 0:
            self.label_video_status.setText("Aktarım Durumu: Evet")
        else:
            self.label_video_status.setText("Aktarım Durumu: Hayır")

    def setPRY(self, pitch, roll, yaw):

        text = "PITCH: " + str(pitch) + " ROLL: " + str(roll) + " YAW: " + str(yaw)
        self.label_gyro.setText(text)

    def setHeightDiff(self, height_diff):

        text = "Yükseklik Farkı: " + str(height_diff)
        self.label_height_diff.setText(text)

    def connection(self):

        global com, first_connect, connected, tele_connected, quit

        if quit and connected:
            if tele_connected:
                self.tele_connection()
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
                t1 = threading.Thread(target=com.getData)
                t1.start()
                t2 = threading.Thread(target=self.timer)
                t2.start()

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
                    t1 = threading.Thread(target=com.getData)
                    t1.start()
                    t2 = threading.Thread(target=self.timer)
                    t2.start()

            else:
                if tele_connected:
                    self.tele_connection()
                com.disconnect()
                connected = False

        self.update_buttons()

    def tele_connection(self):

        global tele_connected

        if tele_connected:
            self.telecommand.disconnect()
            tele_connected = False

        else:
            port = self.combobox_ports.currentText()
            baud = self.combobox_bauds.currentText()
            self.telecommand.connect(port, baud)
            tele_connected = True

        self.update_buttons()

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

    def load_ui(self):

        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / cns.UI_FILE)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


def main():

    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()


if __name__ == "__main__":

    main()
