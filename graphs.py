import pyqtgraph as pg
import numpy as np
import constants as cns

class Graphs:

    def __init__(self, widget):

        self.widget = widget

        # Payload latitude, longitude and altitude graph
        pl_view = pg.GraphicsView(self.widget.graph_pl)
        pl_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        pl_layout = pg.GraphicsLayout()
        pl_view.setCentralItem(pl_layout)
        pl_graph = pl_layout.addPlot(title=cns.GRAPH_PAYLOAD_TITLE)
        pl_graph.addLegend()
        pl_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        pl_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        self.pl_lat_plot = pl_graph.plot(pen='y', name="Latitude (m)")
        self.pl_lon_plot = pl_graph.plot(pen='r', name="Longitude (m)")
        self.pl_alt_plot = pl_graph.plot(pen='b', name="Altitude (m)")
        self.pl_lat_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.pl_lon_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.pl_alt_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Carrier latitude, longitude and altitude graph
        car_view = pg.GraphicsView(self.widget.graph_car)
        car_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        car_layout = pg.GraphicsLayout()
        car_view.setCentralItem(car_layout)
        car_graph = car_layout.addPlot(title=cns.GRAPH_CARRIER_TITLE)
        car_graph.addLegend()
        car_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        car_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        self.car_lat_plot = car_graph.plot(pen='y', name="Latitude (m)")
        self.car_lon_plot = car_graph.plot(pen='r', name="Longitude (m)")
        self.car_alt_plot = car_graph.plot(pen='b', name="Altitude (m)")
        self.car_lat_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.car_lon_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.car_alt_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

    def update_pl(self, lat, lon, alt):

        print(self.pl_lat_data)
        self.pl_lat_data[:-1] = self.pl_lat_data[1:]
        self.pl_lon_data[:-1] = self.pl_lon_data[1:]
        self.pl_alt_data[:-1] = self.pl_alt_data[1:]
        self.pl_lat_data[-1] = lat
        self.pl_lon_data[-1] = lon
        self.pl_alt_data[-1] = alt

        self.pl_lat_plot.setData(self.pl_lat_data)
        self.pl_lon_plot.setData(self.pl_lon_data)
        self.pl_alt_plot.setData(self.pl_alt_data)

    def update_car(self, lat, lon, alt):

        self.car_lat_data[:-1] = self.car_lat_data[1:]
        self.car_lon_data[:-1] = self.car_lon_data[1:]
        self.car_alt_data[:-1] = self.car_alt_data[1:]
        self.car_lat_data[-1] = lat
        self.car_lon_data[-1] = lon
        self.car_alt_data[-1] = alt

        self.car_lat_plot.setData(self.car_lat_data)
        self.car_lon_plot.setData(self.car_lon_data)
        self.car_alt_plot.setData(self.car_alt_data)


