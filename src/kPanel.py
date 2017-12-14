#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :kPanel.py
 Author: FuGui
 Date: 2017/12/13-14:31
 Licence: 
 
'''
import sys

from PyQt5.QtCore import QPoint, QPointF, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QBrush


class KPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super(KPanel, self).__init__(*args, **kwargs)
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 600
        self.setMinimumSize(600, 600)

        self.initUI()
        # print(self.geometry())
        # print(self.geometry().x())

    pass
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.setLayout( QVBoxLayout(self))
        self.show()
        pass
    def paintEvent(self,QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.drawPanel(painter)


        pass
    def drawPanel(self, painter, size=19):
        # lenght = self.width if self.width < self.height else self.height
        lenght = self.geometry().width() if self.geometry().width() < self.geometry().height() else self.geometry().height()
        lenght = lenght if lenght <= 800 else 800
        padding = int(lenght * 0.05)
        interval = int(lenght * 0.9 // (size - 1))

        backgroundcolor=QColor(255, 160, 90)
        linecolor= QColor(70, 70, 70)
        # linecolor= QColor(0, 160, 230)
        # draw background
        painter.setBrush(backgroundcolor)
        painter.drawRect(0, 0, lenght, lenght)

        # draw lines
        painter.setPen(QPen(linecolor, 2))


        # print('lenght: ', lenght)
        # print('padding: ', padding)
        # print('interval: ', interval)

        for x in range(padding, (size)*interval+padding , interval):
            painter.drawLine(x, padding, x, (size-1)*interval+padding)

        for y in range(padding, (size)*interval+padding, interval):
            painter.drawLine(padding, y, (size-1)*interval+padding, y)

        # draw star
        painter.setBrush(linecolor)
        for i in [3, 9 ,15]:
            # print('i: ', i)
            for j in [3, 9, 15]:
                painter.drawEllipse(QPointF(padding+interval*i, padding+interval*j), interval*0.2, interval*0.2)
            
            # painter.drawEllipse(QPointF(padding+interval*3, padding+interval*10), interval*0.2, interval*0.2)
            # painter.drawEllipse(QPointF(padding+interval*3, padding+interval*16), interval*0.2, interval*0.2)


    pass

if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = KPanel()
    sys.exit(app.exec_())
    pass