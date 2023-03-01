UI_FILE = "form.ui"
NUM_OF_VARS = 24
TELEMETRY_LEN = 74
TELEMETRY_PERIOD = 1

TELE_COMMANDS = ("0. Telekomut yok", "1. Görev Yükü Ayrılma", "2. Görev Yükü Kilitlenme", "3. Uçuşa Hazır" ,"4. Model Uydu İniş" ,"5. Ayrılma", "6. Görev Yükü İniş", "7. Kurtarma","8.Sensör kalibre etme")
## old name : SAT_STATUS_VARS

SATELLITE_STATUS =("0. Uçuşa hazır","1. Yükselme","2. Model uydu iniş","3. Ayrılma","4. Görev yükü iniş","5. Kurtarma")

TELEMETRY_FILE_NAME = "/telemetry.csv"
VIDEO_FILE_NAME = "video.avi"
STL_FILE_NAME = "model.stl"

DEFAULT_COORDINATE_X = 39.9211819
DEFAULT_COORDINATE_Y = 32.7983108
CAMERA_URL = "rtsp://192.168.0.154:8554/mjpeg/1"
FTP_IP = '192.168.0.144'
FTP_TIMEOUT = 5
FTP_USERNAME = 'esp'
FTP_PASSWORD = 'esp'
FTP_STORED_FILE_NAME = 'STOR file.mp4'

MAIN_TITLE = "TULPAR Model Uydu Takımı"
MAIN_WIDTH = 1656
MAIN_HEIGHT = 859
MAIN_OPACITY = 0.95
MAIN_BAUDS = ["2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200"]
MAIN_EXIT_TITLE = "CIKIS"
MAIN_EXIT_MESSAGE = "Cikmak istediginizden emin misiniz?"
MAIN_CONNECT = "BAGLAN"
MAIN_DISCONNECT = "KES"

HEADER_BYTE_1 = b'\xab'
HEADER_BYTE_2 = b'\xcd'
FINISH_BYTE_1 = b'\xdc'
FINISH_BYTE_2 = b'\xba'

GRAPH_WIDTH = 361
GRAPH_HEIGHT = 261
GRAPH_PAYLOAD_TITLE = "Görev Yükü"
GRAPH_CARRIER_TITLE = "PRY"
GRAPH_SP_TMP_V_TITLE = "Hız, Sıcaklık ve Gerilim"
GRAPH_PRESSURE_TITLE = "Basınç"
GRAPH_HEIGHT_TITLE = "Yükseklik"
GRAPH_ALTITUDE_TITLE = "Altitude"
GRAPH_X_MAX = 30
GRAPH_PADDING = 0

ARAS_ERROR = ("0. !(12 <= Uydu iniş hız <=14)", "1. !(6<= Görev Yükü iniş hızı <=8)", 
"2. Taşıyıcı basınç verisi alınamaması", "3. Görev Yükü konum verisinin alınamaması", "4. Ayrılmanın gerçekleşmemesi")

TABLE_X = 10
TABLE_Y = 650
TABLE_WIDTH = 1631
TABLE_HEIGHT = 192
TABLE_COLUMN_WIDTH = 150
TABLE_FONT = "Times New Roman"
TABLE_FONT_SIZE = 11
TABLE_TITLE = ("<TAKIM NO>", "<PAKET NUMARASI>", "<GONDERME SAATI>", "<PAYLOAD BASINC>", "<TASIYICI BASINC>", "<PAYLOAD YUKSEKLIK>", "<TASIYICI YUKSEKLIK>", "<YUKSEKLIK FARKI>",
               "<INIS HIZI>", "<SICAKLIK>", "<PIL GERILIMI>", "<PAYLOAD GPS LATITUDE>", "<PAYLOAD GPS LONGITUDE>", "<PAYLOAD GPS ALTITUDE>",
               "<UYDU STATUSU>", "<YAW>", "<ROLL>", "<PITCH>")
