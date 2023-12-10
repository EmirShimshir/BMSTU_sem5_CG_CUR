from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from win import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, engine):
        super().__init__()
        self.setupUi(self)
        self.init_connections()

        self.engine = engine

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Up:
            self.engine.camera.press_up()
        elif event.key() == Qt.Key_Down:
            self.engine.camera.press_down()
        elif event.key() == Qt.Key_Left:
            self.engine.camera.press_left()
        elif event.key() == Qt.Key_Right:
            self.engine.camera.press_right()
        elif event.key() == Qt.Key_W:
            self.engine.camera.press_w()
        elif event.key() == Qt.Key_S:
            self.engine.camera.press_s()
        elif event.key() == Qt.Key_A:
            self.engine.camera.press_a()
        elif event.key() == Qt.Key_D:
            self.engine.camera.press_d()

    def init_connections(self):
        self.stopButton.clicked.connect(self.stop)
        self.startButton.clicked.connect(self.start)

    def stop(self):
        self.speed.setDisabled(False)
        self.acceleration.setDisabled(False)
        self.density.setDisabled(False)
        self.fong.setDisabled(False)
        self.guro.setDisabled(False)
        self.triangle.setDisabled(False)
        self.engine.clear_models()

    def start(self):
        self.engine.clear_models()
        self.speed.setDisabled(True)
        self.acceleration.setDisabled(True)
        self.density.setDisabled(True)
        self.fong.setDisabled(True)
        self.guro.setDisabled(True)
        self.triangle.setDisabled(True)
        v = self.speed.value()
        g = self.acceleration.value()
        ro = self.density.value()
        self.engine.add_models(v, g, ro)
        guro = self.guro.isChecked()
        tri = self.triangle.isChecked()
        self.engine.drawer(guro, tri)



