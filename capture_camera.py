# import the require packages.
import cv2
from PySide2.QtGui import QImage
from PySide2.QtCore import QThread, Qt, Signal


class CaptureCamera(QThread):

    ImageUpdated = Signal(QImage)

    def __init__(self, url) -> None:

        super(CaptureCamera, self).__init__()
        self.url = url
        self.__thread_active = True
        self.__thread_pause = False

    def run(self) -> None:

        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        if cap.isOpened():
            while self.__thread_active:
                if not self.__thread_pause:
                    ret, frame = cap.read()
                    height, width, channels = frame.shape
                    bytes_per_line = width * channels
                    if ret:
                        cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        qt_rgb_image_scaled = qt_rgb_image.scaled(800, 600, Qt.KeepAspectRatio)
                        self.ImageUpdated.emit(qt_rgb_image_scaled)
                    else:
                        break
        cap.release()
        self.quit()

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False
