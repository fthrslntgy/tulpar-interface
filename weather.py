import pandas as pd
import numpy as np


class Weather:

    def __init__(self):

        sheet1 = pd.read_excel('weather.xlsx', sheet_name=0)
        sheet2 = pd.read_excel('weather.xlsx', sheet_name=1)
        self.weather_array = self.excel_to_matrix(sheet1)
        self.current_weather_array = self.excel_to_matrix(sheet2)
        self.windows = self.get_windows(self.weather_array)

    def excel_to_matrix(self, sheet):
        len = sheet.__len__()
        columns = sheet.columns
        weather_array = np.zeros((len,4))
        sayac = 0
        for column in columns:
            for i in range(0,len):
                weather_array[i,sayac] = sheet[column][i]
            sayac = sayac+1

        return weather_array

    def get_windows(self, weather_array):

        windows = []

        row, col = weather_array.shape
    
        for i in range(0, row-6):
            arr_window = weather_array[i:i+7,:]
            windows.append(arr_window)
        
        return windows

    def get_window_properties(self, window):
        arr_mean = np.mean(window, axis=0)
        arr_var = np.var(window, axis=0)
        window_var = np.zeros(window.shape)
        row, col = window.shape
        for i in range(0,row):
            window_var[i,:] = window[i, :] - arr_mean
        return arr_mean, window_var

    def predict(self, temp, humidity, forecast):

        self.current_weather_array[6,0] = temp
        self.current_weather_array[6,2] = humidity
        self.current_weather_array[6,3] = forecast

        distances = []
        for window in self.windows:
            distances.append(np.linalg.norm(window - self.current_weather_array))

        chosen_window = distances.index(min(distances))
        chosen_window_mean, chosen_window_var = self.get_window_properties(self.windows[chosen_window])
        current_window_mean, current_window_var = self.get_window_properties(self.current_weather_array)
        var_mean = (np.mean(chosen_window_var, axis=0) + np.mean(current_window_var, axis=0))/2.0
        predicted_weather_condition = self.windows[chosen_window][6] + var_mean
        return predicted_weather_condition








