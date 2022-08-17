import pyqtgraph as pg
import numpy as np
import constants as cns


class Graphs:

    def __init__(self, widget):

        self.widget = widget

        # Payload latitude, longitude
        pl_view = pg.GraphicsView(self.widget.graph_pl)
        pl_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        pl_layout = pg.GraphicsLayout()
        pl_view.setCentralItem(pl_layout)
        pl_graph = pl_layout.addPlot(title=cns.GRAPH_PAYLOAD_TITLE)
        pl_graph.addLegend()
        pl_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        pl_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        pl_graph.vb.setLimits(yMin=0)
        self.pl_lat_plot = pl_graph.plot(pen='y', name="Latitude (m)")
        self.pl_lon_plot = pl_graph.plot(pen='r', name="Longitude (m)")
        self.pl_lat_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.pl_lon_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Carrier latitude, longitude
        car_view = pg.GraphicsView(self.widget.graph_car)
        car_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        car_layout = pg.GraphicsLayout()
        car_view.setCentralItem(car_layout)
        car_graph = car_layout.addPlot(title=cns.GRAPH_CARRIER_TITLE)
        car_graph.addLegend()
        car_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        car_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        car_graph.vb.setLimits(yMin=0)
        self.car_lat_plot = car_graph.plot(pen='y', name="Latitude (m)")
        self.car_lon_plot = car_graph.plot(pen='r', name="Longitude (m)")
        self.car_lat_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.car_lon_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Speed, tempature and voltage graph
        sp_tmp_v_view = pg.GraphicsView(self.widget.graph_sp_tmp_v)
        sp_tmp_v_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        sp_tmp_v_layout = pg.GraphicsLayout()
        sp_tmp_v_view.setCentralItem(sp_tmp_v_layout)
        sp_tmp_v_graph = sp_tmp_v_layout.addPlot(title=cns.GRAPH_SP_TMP_V_TITLE)
        sp_tmp_v_graph.addLegend()
        sp_tmp_v_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        sp_tmp_v_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        sp_tmp_v_graph.vb.setLimits(yMin=0)
        self.sp_plot = sp_tmp_v_graph.plot(pen='y', name="Hız (m/s)")
        self.tmp_plot = sp_tmp_v_graph.plot(pen='r', name="Sıcaklık (C)")
        self.v_plot = sp_tmp_v_graph.plot(pen='b', name="Gerilim (V)")
        self.sp_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.tmp_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.v_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Pressure graph
        pressure_view = pg.GraphicsView(self.widget.graph_pressure)
        pressure_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        pressure_layout = pg.GraphicsLayout()
        pressure_view.setCentralItem(pressure_layout)
        pr_hei_graph = pressure_layout.addPlot(title=cns.GRAPH_PRESSURE_TITLE)
        pr_hei_graph.addLegend()
        pr_hei_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        pr_hei_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        pr_hei_graph.vb.setLimits(yMin=0)
        self.pl_pr_plot = pr_hei_graph.plot(pen='g', name="Görev Yükü Basınç (Pa)")
        self.car_pr_plot = pr_hei_graph.plot(pen='b', name="Taşıyıcı Basınç (Pa)")
        self.pl_pr_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.car_pr_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Height graph
        height_view = pg.GraphicsView(self.widget.graph_height)
        height_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        height_layout = pg.GraphicsLayout()
        height_view.setCentralItem(height_layout)
        height_graph = height_layout.addPlot(title=cns.GRAPH_HEIGHT_TITLE)
        height_graph.addLegend()
        height_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        height_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        height_graph.vb.setLimits(yMin=0)
        self.pl_hei_plot = height_graph.plot(pen='g', name="Görev Yükü Yükseklik (m)")
        self.car_hei_plot = height_graph.plot(pen='b', name="Taşıyıcı Yükseklik (m)")
        self.pl_hei_data = np.linspace(0, 0, cns.GRAPH_X_MAX)
        self.car_hei_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

        # Altitude graph
        altitude_view = pg.GraphicsView(self.widget.graph_altitude)
        altitude_view.resize(cns.GRAPH_WIDTH, cns.GRAPH_HEIGHT)
        altitude_layout = pg.GraphicsLayout()
        altitude_view.setCentralItem(altitude_layout)
        altitude_graph = altitude_layout.addPlot(title=cns.GRAPH_ALTITUDE_TITLE)
        altitude_graph.addLegend()
        altitude_graph.setXRange(0, cns.GRAPH_X_MAX, padding=cns.GRAPH_PADDING)
        altitude_graph.vb.setLimits(xMin=0, xMax=cns.GRAPH_X_MAX)
        altitude_graph.vb.setLimits(yMin=0)
        self.pl_alt_plot = altitude_graph.plot(pen='g', name="Görev Yükü Altitude (m)")
        self.car_alt_plot = altitude_graph.plot(pen='b', name="Taşıyıcı Altitude (m)")
        self.pl_alt_data = np.linspace(0, 0, cns.GRAPH_X_MAX)  
        self.car_alt_data = np.linspace(0, 0, cns.GRAPH_X_MAX)

    def update_pl(self, lat, lon):

        self.pl_lat_data[:-1] = self.pl_lat_data[1:]
        self.pl_lon_data[:-1] = self.pl_lon_data[1:]
        self.pl_lat_data[-1] = lat
        self.pl_lon_data[-1] = lon

        self.pl_lat_plot.setData(self.pl_lat_data)
        self.pl_lon_plot.setData(self.pl_lon_data)

    def update_car(self, lat, lon):

        self.car_lat_data[:-1] = self.car_lat_data[1:]
        self.car_lon_data[:-1] = self.car_lon_data[1:]
        self.car_lat_data[-1] = lat
        self.car_lon_data[-1] = lon

        self.car_lat_plot.setData(self.car_lat_data)
        self.car_lon_plot.setData(self.car_lon_data)
    
    def update_sp_tmp_v(self, sp, tmp, v):

        self.sp_data[:-1] = self.sp_data[1:]
        self.tmp_data[:-1] = self.tmp_data[1:]
        self.v_data[:-1] = self.v_data[1:]
        self.sp_data[-1] = sp
        self.tmp_data[-1] = tmp
        self.v_data[-1] = v

        self.sp_plot.setData(self.sp_data)
        self.tmp_plot.setData(self.tmp_data)
        self.v_plot.setData(self.v_data)

    def update_pressure(self, pl_pr, car_pl):

        self.pl_pr_data[:-1] = self.pl_pr_data[1:]
        self.car_pr_data[:-1] = self.car_pr_data[1:]
        self.pl_pr_data[-1] = pl_pr
        self.car_pr_data[-1] = car_pl

        self.pl_pr_plot.setData(self.pl_pr_data)
        self.car_pr_plot.setData(self.car_pr_data)

    def update_height(self, pl_hei, car_hei):

        self.pl_hei_data[:-1] = self.pl_hei_data[1:]
        self.car_hei_data[:-1] = self.car_hei_data[1:]
        self.pl_hei_data[-1] = pl_hei
        self.car_hei_data[-1] = car_hei

        self.pl_hei_plot.setData(self.pl_pr_data)
        self.car_hei_plot.setData(self.car_pr_data)
    
    def update_altitude(self, pl_alt, car_alt):

        self.pl_alt_data[:-1] = self.pl_alt_data[1:]
        self.car_alt_data[:-1] = self.car_alt_data[1:]
        self.pl_alt_data[-1] = pl_alt
        self.car_alt_data[-1] = car_alt

        self.pl_alt_plot.setData(self.pl_alt_data)
        self.car_alt_plot.setData(self.car_alt_data)

