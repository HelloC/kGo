import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt


class App(QWidget):

    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200

        self.list1=[[1,2],['a','b']]
        self.list2=[]
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('btn', self)
        button.setToolTip('This s an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)
        button.setMaximumSize(50,50)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        print('list1 ', self.list1)
        item = self.list1.pop()
        print('item ', item)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())