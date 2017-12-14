#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :PicPanel.py
 Author: FuGui
 Date: 2017/12/13-23:26
 Licence: 
 
'''
import sys
from PyQt5.QtCore import QPoint, QPointF, QRect, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QBrush, QPixmap


class PicPanel(QWidget):
    def __init__(self,  *args, **kwargs):
        super(PicPanel, self).__init__(*args, **kwargs)
        self.boardWidth = 600
        self.boardHeight = 600

        self.resize(self.boardWidth, self.boardHeight)
        self.setMinimumSize(self.boardWidth, self.boardHeight)

        self.mboardsize = 19

        self.isBlack = True

        self.chosen_points = []
        self.initUI()
        self.show()
        pass

    def initUI(self):
        # self.resize()
        self.initGoBoardSize()

        self.initGoImages()

        # mlayout.addWidget(self.labelBoard)
        # self.setLayout(mlayout)
        pass
    def initGoBoardSize(self):
        mlen = self.geometry().width() if self.geometry().width() < self.geometry().height() else self.geometry().height()
        self.lenght = mlen if mlen <= 800 else 800
        # print('mboardsize ', self.mboardsize)
        self.interval = int(self.lenght * 0.9 // (self.mboardsize - 1))
        # self.interval = 30
        self.padding = self.interval
        pass
    def initGoImages(self):
        self.bdPixmap = QPixmap('src\\resource\\image\\board.png')
        self.blPixmap = QPixmap('src\\resource\\image\\black.png')
        self.wtPixmap = QPixmap('src\\resource\\image\\white.png')

        self.transToQuadrate(self.bdPixmap)
        self.transToQuadrate(self.blPixmap)
        self.transToQuadrate(self.wtPixmap)

        # print('bdPixmap', self.bdPixmap)
        # print(self.bdPixmap.size().width())

        radio = self.boardWidth / self.bdPixmap.size().width() * 0.8

        # width = int(self.blPixmap.size().width() * radio)
        # height = int(self.blPixmap.size().height() * radio)
        # print(width, " ", height)

        self.boardPixmap = self.bdPixmap.scaled(self.boardWidth, self.boardHeight, Qt.KeepAspectRatio)
        # self.blackPixmap = self.blPixmap.scaled(width, height, Qt.KeepAspectRatio)
        # self.whitePixmap = self.wtPixmap.scaled(width, height, Qt.KeepAspectRatio)
        self.reCalculateGoImage()

        pass
    def reCalculateGoImage(self):
        radio = self.interval*0.9
        self.blackPixmap = self.blPixmap.scaled(radio, radio, Qt.KeepAspectRatio)
        self.whitePixmap = self.wtPixmap.scaled(radio, radio, Qt.KeepAspectRatio)
        pass

    def transToQuadrate(self, pixmap):
        if (pixmap.size().width() > pixmap.size().height()):
            pixmap.scaled(pixmap.size().height(), pixmap.size().height())
        else:
            pixmap.scaled(pixmap.size().width(), pixmap.size().width())
            pass
        pass

    def paintEvent(self, QPaintEvent):

        self.initGoBoardSize()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.drawBoard(painter)
        self.drawPanelLines(painter)
        self.reCalculateGoImage()
        self.drawPoints(painter)

    def drawBoard(self, painter):
        painter.drawPixmap(self.rect(), self.boardPixmap)
        pass

    def drawPanelLines(self, painter):
        # lenght = self.width if self.width < self.height else self.height

        linecolor = QColor(70, 70, 70)

        # draw lines
        painter.setPen(QPen(linecolor, 2))

        # print('lenght: ', lenght)
        # print('padding: ', padding)
        # print('interval: ', interval)

        for x in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(x, self.padding, x, (self.mboardsize - 1) * self.interval + self.padding)

        for y in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(self.padding, y, (self.mboardsize - 1) * self.interval + self.padding, y)

        # draw star
        painter.setBrush(linecolor)
        for i in [3, 9, 15]:
            # print('i: ', i)
            for j in [3, 9, 15]:
                painter.drawEllipse(QPointF(self.padding + self.interval * i, self.padding + self.interval * j),
                                    self.interval * 0.2,
                                    self.interval * 0.2)

            # painter.drawEllipse(QPointF(padding+interval*3, padding+interval*10), interval*0.2, interval*0.2)
            # painter.drawEllipse(QPointF(padding+interval*3, padding+interval*16), interval*0.2, interval*0.2)
            pass
        pass

    def drawPoints(self, painter):
        # painter.setPen(QPen())
        for tpoint in self.chosen_points:
            # painter.drawPoint(pos)
            # print(tpoint)
            # print(tpoint[0])
            # print(tpoint[1])
            # print(tpoint[0].x() * self.interval)
            # print(tpoint[0].y() * self.interval)

            if tpoint[1] is 'b':
                pmap = self.blackPixmap

            else:
                pmap = self.whitePixmap

                pass
            painter.drawPixmap(tpoint[0].x() * self.interval - self.blackPixmap.size().width() / 2,
                               tpoint[0].y() * self.interval - self.blackPixmap.size().height() / 2,
                               pmap)
            pass

        pass

    def mouseReleaseEvent(self, cursor_event):
        # print(cursor_event.pos())
        p = self.calculatePoint(cursor_event.pos())
        if p is not None:
            if self.isBlack is True:
                self.chosen_points.append((p,'b'))
            else:
                self.chosen_points.append((p,'w'))
                pass
            self.isBlack = not self.isBlack
            pass
            # self.chosen_points.append(self.mapFromGlobal(QtGui.QCursor.pos()))
            self.update()
        pass

    def calculatePoint(self, pos):
        x = pos.x()
        y = pos.y()
        # print('x:', x)
        # print('y:', y)

        px = self.calPointOne(x)
        py = self.calPointOne(y)

        # print('px:', px)
        # print('py:', py)
        if px is not None and py is not None:
            return QPoint(px, py)
        else:
            return None

        pass

    def calPointOne(self, p):
        m = p // self.interval
        n = p % self.interval
        # print('m:', m)
        # print('n:', n)

        if m <= 0 or m >= 19:
            return None

        if (n < self.interval * 0.5):
            ret = m
        elif (n > self.interval * 0.6):
            ret = (m + 1)
            pass
        else:
            print('re press')
            ret = None
            pass
        return ret

    pass


if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = PicPanel()
    sys.exit(app.exec_())
    pass
