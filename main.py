import os
import serial.tools.list_ports
import socket
import threading
import csv
import time
from time import sleep, strftime
from ftplib import FTP
from pathlib import Path

import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PySide2.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView, QMessageBox, QFileDialog
from PySide2.QtCore import QFile, QRect
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPalette, QColor, Qt, QPixmap, QImage
from PySide2.QtUiTools import loadUiType

from communication import Communication
from telemetry_table import TelemetryTable
from graphs import Graphs
from telecommand import Telecommand
from capture_camera import CaptureCamera
from map import Map
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

        self.session_directory = output_dir + strftime("/%d%m%Y_%H-%M-%S")
        os.makedirs(self.session_directory)
        with open(self.session_directory + cns.TELEMETRY_FILE_NAME, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(cns.TABLE_TITLE)

        # Main window options
        self.image = None
        self.setWindowIcon(QIcon("images/logo.ico"))
        self.setWindowTitle(cns.MAIN_TITLE)
        self.setFixedSize(cns.MAIN_WIDTH, cns.MAIN_HEIGHT)
        # self.setWindowOpacity(cns.MAIN_OPACITY)

        # Palette options
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(135, 105, 255))
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

        # Telemetry table component
        self.table_telemetry = TelemetryTable(self)
        self.table_telemetry.setStyleSheet("background-color: white")
        self.table_telemetry.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_telemetry.setGeometry(QRect(cns.TABLE_X, cns.TABLE_Y, cns.TABLE_WIDTH, cns.TABLE_HEIGHT))

        # Port, baud and connection components
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])
        for element in cns.MAIN_BAUDS:
            self.combobox_bauds.addItem(element)
        self.combobox_ports.setStyleSheet("color: black;")
        self.combobox_bauds.setStyleSheet("color: black;")
        self.button_refresh.setIcon(QIcon("images/refresh.png"))
        self.button_refresh.clicked.connect(self.refreshPorts)

        self.telecommand = Telecommand(self)
        self.button_connection.setStyleSheet("background-color: green")
        self.button_connection.clicked.connect(self.connection)
        self.button_connection_tele.clicked.connect(self.teleConnection)

        # Status and telecommand components
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_timer.setAlignment(Qt.AlignCenter)
        self.label_timer.setStyleSheet("background-color: black; color: red; font-size: 14px;font-weight: bold;")

        self.button_send_command.setStyleSheet("color: black;")
        self.button_servo_open.setStyleSheet("color: black;")
        self.button_servo_close.setStyleSheet("color: black;")
        self.button_caliber.setStyleSheet("color: black;")
        self.combobox_command.setStyleSheet("color: black;")

        for element in cns.SAT_STATUS_VARS:
            self.combobox_command.addItem(element)
        self.button_send_command.clicked.connect(lambda: self.telecommand.sendTelecommand(self.combobox_command.currentText()))
        self.button_servo_open.clicked.connect(self.telecommand.sendServoOpen)
        self.button_servo_close.clicked.connect(self.telecommand.sendServoClose)

        # Video send components
        self.button_select_video.clicked.connect(self.uploadVideo)
        self.button_send_video.clicked.connect(self.sendVideo)
        self.label_video_status.setAlignment(Qt.AlignCenter)
        self.label_video_status.setStyleSheet("background-color: black; font-size: 8pt; font-weight: bold; color: white")
        self.label_video_status.setText("Aktarım Durumu: -")
        self.lineedit_select_video.setStyleSheet("background-color: white; color: black;")
        self.button_select_video.setStyleSheet("color: black;")
        self.button_send_video.setStyleSheet("background-color: green; color: black;")

        ## Alarm components
        # self.button_alarm1.setIcon(QIcon("images/alarm_ok.png"))
        self.button_alarm1.setStyleSheet("background-color: green;")
        # self.button_alarm2.setIcon(QIcon("images/alarm_warning.png"))
        self.button_alarm2.setStyleSheet("background-color: red;")
        self.button_alarm1.setEnabled(False)
        self.button_alarm2.setEnabled(False)

        # Logo component
        pixmap_tulpar = QPixmap('images/logo_tulpar.png')
        self.label_logo_tulpar.setPixmap(pixmap_tulpar)
        pixmap_etu = QPixmap('images/logo_etu.png')
        self.label_logo_etu.setPixmap(pixmap_etu)

        # Gyro (model) compontents
        filename = cns.STL_FILE_NAME
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(filename)

        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame_model)
        self.vl.addWidget(self.vtkWidget)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.transform = vtk.vtkTransform()
        self.transformFilter = vtk.vtkTransformPolyDataFilter()
        self.transformFilter.SetTransform(self.transform)
        self.transformFilter.SetInputConnection(self.reader.GetOutputPort())
        self.transformFilter.Update()
        self.mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(self.transformFilter.GetOutput())
        else:
            self.mapper.SetInputConnection(self.transformFilter.GetOutputPort())
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.SetScale(0.0107, 0.0107, 0.0107)
        self.actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.ren.AddActor(self.actor)
        self.ren.SetBackground(0.496, 0.832, 0.996)
        self.ren.ResetCamera()
        self.frame_model.setLineWidth(0.6)
        self.frame_model.setLayout(self.vl)
        self.iren.Initialize()
        self.iren.Start()
        self.frame_model.setStyleSheet("border:1px solid #000000; background-color:#7FD5FF")

        self.label_gyro.setAlignment(Qt.AlignCenter)
        self.label_gyro.setStyleSheet("background-color: darkred; font-size: 8pt; font-weight: bold; color: white")

        # Map components
        self.map = Map(self)
        self.updateLatLon(cns.DEFAULT_COORDINATE_X, cns.DEFAULT_COORDINATE_Y, cns.DEFAULT_COORDINATE_X + 0.01, cns.DEFAULT_COORDINATE_Y + 0.01)
        self.map.update(self.pl_lat, self.pl_lon, self.car_lat, self.car_lon)

        self.label_height_diff.setAlignment(Qt.AlignCenter)
        self.label_height_diff.setStyleSheet("background-color: darkred; font-size: 10pt; font-weight: bold; color: white")

        # Camera component
        self.label_camera_text.setStyleSheet("background-color: darkred; font-size: 10pt; font-weight: bold; color: white")
        self.label_camera_text.setAlignment(Qt.AlignCenter)
        self.label_camera_text.setText("REALTIME VIDEO CONNECTION: NOT CONNECTED")
        self.camera_started = False
        self.camera_paused = False
        self.camera_recorded = False
        self.button_camera_start.setStyleSheet("background-color: green")
        self.button_camera_pause.setEnabled(False)
        self.button_camera_pause.setStyleSheet("background-color: None")
        self.button_camera_record.setEnabled(False)
        self.button_camera_record.setStyleSheet("background-color: None")

        self.camurl = cns.CAMERA_URL
        self.button_camera_start.clicked.connect(self.cameraStart)
        self.button_camera_pause.clicked.connect(self.cameraPause)
        self.button_camera_record.clicked.connect(self.cameraRecord)

        # Graph components
        self.graphs = Graphs(self)
        
        # Update buttons
        self.updateButtons()

    def updateButtons(self):

        global connected, tele_connected

        if connected:
            self.button_connection.setStyleSheet("background-color: red")
            self.button_connection.setText(cns.MAIN_DISCONNECT)
            self.label_status.setStyleSheet("background-color: green; font-size: 12pt; font-weight: bold;")
            self.label_status.setText("CONNECTED")
            self.button_connection_tele.setEnabled(True)

            if tele_connected:
                self.button_connection_tele.setStyleSheet("background-color: red")
                self.combobox_command.setEnabled(True)
                self.button_send_command.setEnabled(True)
                self.button_servo_open.setEnabled(True)
                self.button_servo_close.setEnabled(True)
                self.button_caliber.setEnabled(True)

            else:
                self.button_connection_tele.setStyleSheet("background-color: green")
                self.combobox_command.setEnabled(False)
                self.button_send_command.setEnabled(False)
                self.button_servo_open.setEnabled(False)
                self.button_servo_close.setEnabled(False)
                self.button_caliber.setEnabled(False)

        else:
            self.button_connection.setStyleSheet("background-color: green")
            self.button_connection.setText(cns.MAIN_CONNECT)
            self.label_status.setStyleSheet("background-color: red; font-size: 12pt; font-weight: bold;")
            self.label_status.setText("UNCONNECTED")
            self.label_timer.setText("UPTIME 00 : 00")

            self.button_connection_tele.setEnabled(False)
            self.button_connection_tele.setStyleSheet("background-color: None")
            self.combobox_command.setEnabled(False)
            self.button_send_command.setEnabled(False)
            self.button_servo_open.setEnabled(False)
            self.button_servo_close.setEnabled(False)
            self.button_caliber.setEnabled(False)

    def refreshPorts(self):

        self.combobox_ports.clear()
        ports = serial.tools.list_ports.comports()
        for element in ports:
            self.combobox_ports.addItem(str(element).split()[0])
        self.map.update(self.pl_lat, self.pl_lon, self.car_lat, self.car_lon)

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
        tFtp = threading.Thread(target=self.fileTransferFTP, args=[file_name])
        tFtp.start()
    
    def fileTransferFTP(self, file_name):

        try:
            session = FTP(cns.FTP_IP, cns.FTP_USERNAME, cns.FTP_PASSWORD, timeout=cns.FTP_TIMEOUT)
        except socket.timeout as e: 
            print("File transfer error! " + str(e))
            sleep(1)
            self.fileTransferFTP(file_name)
        else:  
            file = open(file_name, 'rb')
            session.storbinary(cns.FTP_STORED_FILE_NAME, file)
            file.close()
            session.quit()
            print("File sent succesfully!")

    def updateLatLon(self, pl_lat, pl_lon, car_lat, car_lon):

        self.pl_lat = pl_lat
        self.pl_lon = pl_lon
        self.car_lat = car_lat
        self.car_lon = car_lon
    
    def ShowCamera(self, frame, control):
        
        if control is False:
            self.cameraStart()
            empty_image = QImage()
            self.label_camera.setPixmap(QPixmap.fromImage(empty_image))
        else:
            self.label_camera.setPixmap(QPixmap.fromImage(frame))
        
    def cameraStart(self):

        if not self.camera_started:
            self.CaptureCamera = CaptureCamera(self.camurl, self.session_directory)
            self.CaptureCamera.ImageUpdated.connect(lambda image, control: self.ShowCamera(image, control))
            self.CaptureCamera.start()
            self.camera_started = True
            self.button_camera_start.setText("STOP")
            self.button_camera_start.setStyleSheet("background-color: red")
            self.button_camera_pause.setEnabled(True)
            self.button_camera_pause.setText("PAUSE")
            self.button_camera_pause.setStyleSheet("background-color: red")
            self.button_camera_record.setEnabled(True)
            self.button_camera_record.setText("RECORD")
            self.button_camera_record.setStyleSheet("background-color: green")
            self.label_camera_text.setText("REALTIME VIDEO CONNECTION: CONNECTED")

        else:
            self.CaptureCamera.stop()
            self.camera_started = False
            self.camera_paused = False
            self.camera_recorded = False
            self.button_camera_start.setText("START")
            self.button_camera_start.setStyleSheet("background-color: green")
            self.button_camera_pause.setEnabled(False)
            self.button_camera_pause.setText("PAUSE")
            self.button_camera_pause.setStyleSheet("background-color: None")
            self.button_camera_record.setEnabled(False)
            self.button_camera_record.setText("RECORD")
            self.button_camera_record.setStyleSheet("background-color: None")
            self.label_camera_text.setText("REALTIME VIDEO CONNECTION: NOT CONNECTED")

    def cameraPause(self):

        if not self.camera_paused:
            self.camera_paused = True
            self.CaptureCamera.pause()
            self.button_camera_pause.setText("UNPAUSE")
            self.button_camera_pause.setStyleSheet("background-color: green")

        else:
            self.camera_paused = False
            self.CaptureCamera.unpause()
            self.button_camera_pause.setText("PAUSE")
            self.button_camera_pause.setStyleSheet("background-color: red")

    def cameraRecord(self):

        if not self.camera_recorded:
            self.camera_recorded = True
            self.CaptureCamera.record()
            self.button_camera_record.setText("UNRECORD")
            self.button_camera_record.setStyleSheet("background-color: red")

        else:
            self.camera_recorded = False
            self.CaptureCamera.unrecord()
            self.button_camera_record.setText("RECORD")
            self.button_camera_record.setStyleSheet("background-color: green")

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

        if status == 1:
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

        global com, first_connect, connected, tele_connected, suit

        if quit and connected:
            if tele_connected:
                self.teleConnection()
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
                    connected = True
                    t1 = threading.Thread(target=com.getData)
                    t1.start()
                    t2 = threading.Thread(target=self.timer)
                    t2.start()

            else:
                if tele_connected:
                    self.teleConnection()
                com.disconnect()
                connected = False

        self.updateButtons()

    def teleConnection(self):

        global tele_connected

        if tele_connected:
            self.telecommand.disconnect()
            tele_connected = False

        else:
            port = self.combobox_ports.currentText()
            baud = self.combobox_bauds.currentText()
            self.telecommand.connect(port, baud)
            tele_connected = True

        self.updateButtons()

    def closeEvent(self, event):

        global quit
        close = QMessageBox.question(self, cns.MAIN_EXIT_TITLE, cns.MAIN_EXIT_MESSAGE, QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            quit = True
            self.vtkWidget.Finalize()
            event.accept()
            self.connection()
        else:
            quit = False
            event.ignore()


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()
