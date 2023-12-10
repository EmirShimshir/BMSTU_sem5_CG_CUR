from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage, QPainter, QColor


class RenderWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        self.width = width
        self.height = height

        self.setGeometry(20, 20, self.width, self.height)
        self.image = QImage(width, height, QImage.Format_RGB32)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image.scaled(self.width, self.height))
        painter.end()

    def set_pixel(self, x, y, r, g, b):
        self.image.setPixel(int(x), int(y), QColor(int(r), int(g), int(b)).rgb())

    def fill(self, rgb):
        self.image.fill(rgb)


