UI_FILE = "form.ui"
NUM_OF_VARS = 24
TELEMETRY_LEN = 88
TELEMETRY_PERIOD = 1

HEADER_BYTE_1 = b'\xab'
HEADER_BYTE_2 = b'\xcd'
FINISH_BYTE_1 = b'\xdc'
FINISH_BYTE_2 = b'\xba'

GRAPH_WIDTH = 361
GRAPH_HEIGHT = 241
GRAPH_PAYLOAD_TITLE = "Görev Yükü"
GRAPH_CARRIER_TITLE = "Taşıyıcı"
GRAPH_X_MAX = 20
GRAPH_PADDING = 0

MAIN_TITLE = "TULPAR Model Uydu Takımı"
MAIN_WIDTH = 1083
MAIN_HEIGHT = 621
MAIN_OPACITY = 0.95
MAIN_BAUDS = ["2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200"]
MAIN_EXIT_TITLE = "CIKIS"
MAIN_EXIT_MESSAGE = "Cikmak istediginizden emin misiniz?"
MAIN_CONNECT = "BAGLAN"
MAIN_DISCONNECT = "KES"


TABLE_X = 10
TABLE_Y = 420
TABLE_WIDTH = 1061
TABLE_HEIGHT = 192
TABLE_COLUMN_WIDTH = 150
TABLE_FONT = "Times New Roman"
TABLE_FONT_SIZE = 11
TABLE_TITLE = ("<TAKIM NO>",
             "<PAKET NUMARASI>",
             "<GONDERME SAATI>",
             "<PAYLOAD BASINC>",
             "<TASIYICI BASINC>",
             "<PAYLOAD YUKSEKLIK>",
             "<TASIYICI YUKSEKLIK>",
             "<YUKSEKLIK FARKI>",
             "<İNİŞ HIZI>",
             "<SICAKLIK>",
             "<PIL GERILIMI>",
             "<PAYLOAD GPS LATITUDE>",
             "<PAYLOAD GPS LONGITUDE>",
             "<PAYLOAD GPS ALTITUDE>",
             "<TASIYICI GPS LATITUDE>",
             "<TASIYICI GPS LONGITUDE>",
             "<TASIYICI GPS ALTITUDE>",
             "<UYDU STATÜSÜ>",
             "<YAW>",
             "<ROLL>",
             "<PITCH>",
             "<DÖNÜŞ SAYISI>",
             "<VİDEO AKTARIM BİLGİSİ>",
             "<HAVA DURUMU>")