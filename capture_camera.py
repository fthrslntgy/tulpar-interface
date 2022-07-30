# import the require packages.
import cv2
from time import strftime
from PySide2.QtGui import QImage
from PySide2.QtCore import QThread, Qt, Signal
import constants as cns


class CaptureCamera(QThread):

    ImageUpdated = Signal(QImage)

    def __init__(self, url, directory) -> None:

        super(CaptureCamera, self).__init__()
        self.url = url
        self.directory = directory
        self.__thread_active = True
        self.__thread_pause = False
        self.record_stat = False

    def run(self) -> None:

        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        self.record()
        if cap.isOpened():
            while self.__thread_active:
                if not self.__thread_pause:
                    ret, frame = cap.read()
                    if self.record_stat:
                        self.out.write(frame)
                    height, width, channels = frame.shape
                    bytes_per_line = width * channels
                    if ret:
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        qt_rgb_image_scaled = qt_rgb_image.scaled(400, 296, Qt.KeepAspectRatio)
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                    else:
                        break
        cap.release()
        self.unrecord()
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

    def record(self) -> None:
        self.out = cv2.VideoWriter(self.directory + strftime("/%H-%M-%S") + "_video.avi", cv2.VideoWriter_fourcc(*'DIVX'), 10, (400, 296))
        self.record_stat = True
    
    def unrecord(self) -> None:
        self.out.release()
        self.record_stat = False
