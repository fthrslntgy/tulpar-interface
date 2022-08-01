import folium
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QUrl
import constants as cns


class Map(QVBoxLayout):

    def __init__(self, widget, parent=None):

        super(self.__class__, self).__init__(parent)
        self.widget = widget
        self.webView = QWebEngineView()
        self.addWidget(self.webView)
        self.widget.frame_map.setLayout(self)
        

    def update(self, pl_lat, pl_lon, car_lat, car_lon):

        coordinates = ((pl_lat+car_lat)/2,(pl_lon+car_lon)/2)
        m = folium.Map(tiles='Stamen Terrain', zoom_start=8, location=coordinates)
        folium.Marker([pl_lat, pl_lon], icon=folium.Icon(color='red')).add_to(m)
        folium.Marker([car_lat, car_lon], icon=folium.Icon(color='blue')).add_to(m)
        m.save(outfile= "map.html")     
        self.webView.load(QUrl.fromLocalFile("/map.html"))
        