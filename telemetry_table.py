from PySide2.QtWidgets import QAbstractItemView, QTableWidget
from PySide2.QtGui import QFont
import constants as cns

class TelemetryTable(QTableWidget):

    title = cns.TABLE_TITLE

    def __init__(self, parent=None):
        super(TelemetryTable, self).__init__(1, cns.NUM_OF_VARS, parent)
        self.setFont(QFont(cns.TABLE_FONT, cns.TABLE_FONT_SIZE, QFont.Normal, italic=False))
        style = "::section {""background-color: white; font-size: 8pt; }"
        self.horizontalHeader().setStyleSheet(style)
        self.setHorizontalHeaderLabels(self.title)
        self.verticalHeader().hide()

        self.setSelectionMode(QAbstractItemView.NoSelection)
        for i in range(0, cns.NUM_OF_VARS):
            self.setColumnWidth(i, cns.TABLE_COLUMN_WIDTH)
