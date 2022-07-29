import serial
import serial.tools.list_ports
from time import sleep
import struct
import constants as cns
import csv
from weather import Weather


class Communication:

    def __init__(self, port, baud, widget):

        self.baudrate = baud
        self.portName = port
        self.widget = widget
        self.q = False
        self.ser = serial.Serial()
        self.weather = Weather()

        self.last_pitch = 0
        self.last_roll = 0
        self.last_yaw = 0

    def connect(self):

        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
            print("Connected : ", self.portName)
            self.q = True
            return True

        except serial.serialutil.SerialException:
            print("Can't open : ", self.portName)
            return False

    def disconnect(self):

        if self.ser.isOpen():
            self.ser.close()
            print("Disconnected : ", self.portName)
            self.q = False

    def getData(self):

        line = []
        last = b'\x00'
        lastlast = b'\x00'

        while self.q:
            try:
                byte = self.ser.read()
                if byte == cns.HEADER_BYTE_2 and len(line) == 0:
                    1 == 1

                elif byte == cns.HEADER_BYTE_1 and last == cns.HEADER_BYTE_2 and len(line) == 0:
                    line.append(last)
                    line.append(byte)

                elif byte and last == cns.FINISH_BYTE_1 and lastlast == cns.FINISH_BYTE_2 and len(line) == cns.TELEMETRY_LEN-1:
                    line.append(byte)
                    self.pckParser(line)
                    line = []
                    sleep(cns.TELEMETRY_PERIOD)

                elif byte and len(line) != 0:
                    line.append(byte)

                if len(line) >= cns.TELEMETRY_LEN:
                    line = []

                lastlast = last
                last = byte

            except BaseException as be:
                print("Serial exception, read at: ", self.portName)
                print("Exception: ", be)

    def pckParser(self, line):

        # header = line[0] + line[1]
        length = line[2]
        length = int.from_bytes(length, "little", signed=False)

        takim_no = line[3] + line[4]
        takim_no = int.from_bytes(takim_no, "little", signed=False)
        takim_no = takim_no * 8

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
        # humidity = humidity[85]+lihumidityne[86]+humidity[87]+humidity[88]
        # [humidity] = struct.unpack("f", humidity)
        # finish = line[89:91]
        # crc = line[91]

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
        row.append(float("{:.2f}".format(longitude_pl)))
        row.append(float("{:.2f}".format(altitude_pl)))
        row.append(float("{:.2f}".format(latitude_car)))
        row.append(float("{:.2f}".format(longitude_car)))
        row.append(float("{:.2f}".format(altitude_car)))
        row.append(status)
        row.append(float("{:.2f}".format(yaw)))
        row.append(float("{:.2f}".format(roll)))
        row.append(float("{:.2f}".format(pitch)))
        row.append(return_number)
        row.append(video_status)
        row.append(weather_forecast)

        print(row)
        # update csv
        with open(self.widget.session_directory + cns.TELEMETRY_FILE_NAME, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(row)
            
        # update telemetry table
        self.widget.addRow(row)

        # update graphs
        self.widget.graphs.update_pl(latitude_pl, longitude_pl, altitude_pl)
        self.widget.graphs.update_car(latitude_car, longitude_car, altitude_car)
        self.widget.graphs.update_pl_hei(pressure_pl, height_pl, pressure_car, height_car)
        self.widget.graphs.update_sp_tmp_v(speed, tempe, b_voltage)

        # update status, pitch-roll-yaw, height diff and video status
        self.widget.setStatus(status)
        self.widget.transform.RotateX(pitch - self.last_pitch)
        self.widget.transform.RotateY(roll - self.last_roll)
        self.widget.transform.RotateZ(yaw - self.last_yaw)
        self.widget.vtkWidget.update()
        self.widget.setPRY(float("{:.2f}".format(pitch)), float("{:.2f}".format(roll)), float("{:.2f}".format(yaw)))
        self.last_pitch = pitch
        self.last_roll = roll
        self.last_yaw = yaw

        # self.widget.updateMap(float("{:.4f}".format(latitude_pl)), float("{:.4f}".format(longitude_pl)))
        self.widget.setHeightDiff(float("{:.2f}".format(height_diff)))
        self.widget.setVideoStatus(status)

        # update weather
        predict = self.weather.predict(float("{:.2f}".format(tempe)), 0, weather_forecast) # max temp, min temp, nem, yağış miktarı
        self.widget.setWeatherPredict(predict)
