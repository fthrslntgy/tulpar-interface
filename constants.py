UI_FILE = "form.ui"
NUM_OF_VARS = 24
TELEMETRY_LEN = 88
TELEMETRY_PERIOD = 1
SAT_STATUS_VARS = ("1. Beklemede", "2. Yükselme", "3. Model uydu iniş ", "4. Ayrılma",
               "5. Görev yükü iniş 6", "6. Askıda kalma", "7. Görev yükü iniş 4", "8. Kurtarma")

TELEMETRY_FILE_NAME = "/Telemetry.csv"
VIDEO_FILE_NAME = "/Video.avi"
STL_FILE_NAME = "model.stl"

DEFAULT_COORDINATE_X = 39.9211819
DEFAULT_COORDINATE_Y = 32.7983108
CAMERA_URL = "rtsp://10.5.39.149:8554/mjpeg/1"
FTP_IP = '10.5.39.143'
FTP_USERNAME = 'esp'
FTP_PASSWORD = 'esp'
FTP_STORED_FILE_NAME = 'STOR file.mp4'

MAIN_TITLE = "TULPAR Model Uydu Takımı"
MAIN_WIDTH = 1286
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
GRAPH_CARRIER_TITLE = "Taşıyıcı"
GRAPH_PR_HEI_TITLE = "Basınç ve Yükseklik"
GRAPH_SP_TMP_V_TITLE = "Hız, Sıcaklık ve Gerilim"
GRAPH_X_MAX = 20
GRAPH_PADDING = 0

TABLE_X = 10
TABLE_Y = 650
TABLE_WIDTH = 1261
TABLE_HEIGHT = 192
TABLE_COLUMN_WIDTH = 150
TABLE_FONT = "Times New Roman"
TABLE_FONT_SIZE = 11
TABLE_TITLE = ("<TAKIM NO>", "<PAKET NUMARASI>", "<GONDERME SAATI>", "<PAYLOAD BASINC>", "<TASIYICI BASINC>", "<PAYLOAD YUKSEKLIK>", "<TASIYICI YUKSEKLIK>", "<YUKSEKLIK FARKI>",
               "<İNİŞ HIZI>", "<SICAKLIK>", "<PIL GERILIMI>", "<PAYLOAD GPS LATITUDE>", "<PAYLOAD GPS LONGITUDE>", "<PAYLOAD GPS ALTITUDE>", "<TASIYICI GPS LATITUDE>",
               "<TASIYICI GPS LONGITUDE>", "<TASIYICI GPS ALTITUDE>", "<UYDU STATÜSÜ>", "<YAW>", "<ROLL>", "<PITCH>", "<DÖNÜŞ SAYISI>", "<VİDEO AKTARIM BİLGİSİ>", "<HAVA DURUMU>")
