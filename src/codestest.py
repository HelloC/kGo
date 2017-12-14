import sys

from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 200
        self.top = 200
        self.width = 600
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        mlayout = QHBoxLayout(self)

        # Create widget
        self.labelImageboard = QLabel()
        self.labelImageblack = QLabel()
        self.labelImagewhite = QLabel()

        self.pixmapboard = QPixmap('board.png')
        self.pixmapblack = QPixmap('black.png')
        self.pixmapwhite = QPixmap('white.png')


        self.pixmapBd = self.pixmapboard.scaled(600, 600, Qt.KeepAspectRatio)
        pixmapBl = self.pixmapblack.scaled(64, 64, Qt.KeepAspectRatio)
        pixmapWt = self.pixmapwhite.scaled(256, 256, Qt.KeepAspectRatio)

        #
        # self.labelImageblack.setPixmap(pixmapBl)
        # self.labelImagewhite.setPixmap(pixmapWt)

        # labelImage.setAlignment(Qt.AlignCenter)
        # self.labelImageblack.resize(0.3 * self.labelImageblack.pixmap().size())
        # self.labelImageblack.resize(1.5 * self.labelImagewhite.pixmap().size())

        # mlayout.addWidget(self.labelImageblack)
        # mlayout.addWidget(self.labelImagewhite)

        # self.setLayout(mlayout)

        # self.resize(pixmap.width(), pixmap.height())

        self.labelImageboard.setPixmap(self.pixmapBd)

        self.show()
        pass
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self.pixmapBd)
        line = QLineF(10.0, 80.0, 90.0, 20.0)
        painter.drawLine(line)
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
