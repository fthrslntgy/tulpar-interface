from PySide2.QtWidgets import QAbstractItemView, QTableWidget
from PySide2.QtGui import QFont


class TelemetryTable(QTableWidget):

    title = ("<TAKIM NO>",
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

    def __init__(self, parent=None):
        super(TelemetryTable, self).__init__(1, 24, parent)
        self.setFont(QFont("Times New Roman", 11, QFont.Normal, italic=False))
        style = "::section {""background-color: white; font-size: 8pt; }"
        self.horizontalHeader().setStyleSheet(style)
        self.setHorizontalHeaderLabels(self.title)
        self.verticalHeader().hide()

        self.setSelectionMode(QAbstractItemView.NoSelection)
        for i in range(0, 24):
            self.setColumnWidth(i, 150)
