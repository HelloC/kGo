#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :PicPanel.py
 Author: FuGui
 Date: 2017/12/13-23:26
 Licence: 
 
'''
import sys
from PyQt5.QtCore import QPointF, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen,  QPixmap

from src.GoEngine import GoEngine





class PicPanel(QWidget):
    sigUpdate = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PicPanel, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.boardWidth = 800
        self.boardHeight = 800

        self.resize(self.boardWidth, self.boardHeight)
        self.setMinimumSize(self.boardWidth, self.boardHeight)

        self.mboardsize = 19
        self.mousePos=[10,10]

        self._goStonesEngine = GoEngine()

        self.initUI()
        self.initSinalHandler()

        self.show()
        pass


    def initUI(self):
        self.initGoBoardSize()
        self.initGoImages()
        pass

    def initGoBoardSize(self):
        mlen = self.geometry().width() if self.geometry().width() < self.geometry().height() else self.geometry().height()
        # self.lenght = mlen if mlen <= 800 else 800
        self.lenght = mlen
        self.interval = int(self.lenght * 0.9 // (self.mboardsize - 1))
        self.padding = self.interval
        pass

    def initGoImages(self):
        self.bdPixmap = QPixmap('src\\resource\\image\\board.png')
        self.blPixmap = QPixmap('src\\resource\\image\\black.png')
        self.wtPixmap = QPixmap('src\\resource\\image\\white.png')
        self.posPixmap = QPixmap('src\\resource\\image\\pos.png')
        self.lastStepPixmap = QPixmap('src\\resource\\image\\square.gif')

        self.transToQuadrate(self.bdPixmap)
        self.transToQuadrate(self.blPixmap)
        self.transToQuadrate(self.wtPixmap)

        radio = self.boardWidth / self.bdPixmap.size().width() * 0.8
        self.boardPixmap = self.bdPixmap.scaled(self.boardWidth, self.boardHeight, Qt.KeepAspectRatio)
        self.reCalculateGoImage()
        pass
    def initSinalHandler(self):
        self.sigUpdate.connect(self.sigUpdateHandler)

    def newPanel(self):
        self.goStonesEngine.newGo()
        self.update()

    def stepBackLastOne(self):
        if self.goStonesEngine.stepPopLastOne():
            self.update()
            return True
        False

    @property
    def goStonesEngine(self):
        return self._goStonesEngine
    @goStonesEngine.setter
    def goStonesEngine(self,val):
        self._goStonesEngine=val


    def reCalculateGoImage(self):
        radio = self.interval * 0.9
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

    def sigUpdateHandler(self):
        self.update()

    def paintEvent(self, QPaintEvent):

        self.initGoBoardSize()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.drawBoard(painter)
        self.drawPanelLines(painter)
        self.drawPoints(painter)
        self.drawMousePos(painter)

    def drawBoard(self, painter):
        painter.drawPixmap(self.rect(), self.boardPixmap)
        pass

    def drawPanelLines(self, painter):
        linecolor = QColor(70, 70, 70)
        # draw lines
        painter.setPen(QPen(linecolor, 2))

        for x in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(x, self.padding, x, (self.mboardsize - 1) * self.interval + self.padding)

        for y in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(self.padding, y, (self.mboardsize - 1) * self.interval + self.padding, y)

        # draw star
        painter.setBrush(linecolor)
        for i in [3, 9, 15]:
            for j in [3, 9, 15]:
                painter.drawEllipse(QPointF(self.padding + self.interval * i, self.padding + self.interval * j),
                                    self.interval * 0.2,
                                    self.interval * 0.2)

            pass
        pass

    def drawMousePos(self, painter):
        painter.drawPixmap((self.mousePos[0]) * self.interval - self.posPixmap.size().width() / 2,
                           (self.mousePos[1]) * self.interval - self.posPixmap.size().height() / 2,
                               self.posPixmap)

    def drawPoints(self, painter):
        for tpoint in self.goStonesEngine.getStepsLists():

            if tpoint[2] is 'black':
                painter.drawPixmap((tpoint[0] + 1) * self.interval - self.blackPixmap.size().width() / 2,
                                   (tpoint[1] + 1) * self.interval - self.blackPixmap.size().height() / 2,
                                   self.blackPixmap)
            elif tpoint[2] is 'white':
                painter.drawPixmap((tpoint[0] + 1) * self.interval - self.blackPixmap.size().width() / 2,
                                   (tpoint[1] + 1) * self.interval - self.blackPixmap.size().height() / 2,
                                   self.whitePixmap)
            else:
                pass
            pass
        tpointlist=self.goStonesEngine.getStepsLists()
        if tpointlist:
            tpoint = tpointlist[-1]
            painter.drawPixmap((tpoint[0] + 1) * self.interval - self.lastStepPixmap.size().width() / 2,
                                (tpoint[1] + 1) * self.interval - self.lastStepPixmap.size().height() / 2,
                                self.lastStepPixmap)
        pass

    def mouseReleaseEvent(self, cursor_event):
        px, py = self.xyTorowcol(cursor_event.pos())

        if px > 0 and py > 0:
            if self.goStonesEngine.move(px, py, None, False) is True:
                self.update()
            else:
                mMBox=QMessageBox()
                mMBox.setIcon(QIcon('src\\resource\\image\\unhappy.png'))
                mMBox.information(self,
                                        "K-Go",
                                        "Warnning: Step Forbidden",
                                        QMessageBox.Ok)
            pass

        pass

    def mouseMoveEvent(self,cursor_event):
        px, py = self.xyTorowcol(cursor_event.pos())
        if px > 0 and py > 0:
            self.mousePos[0] = px
            self.mousePos[1] = py
            self.update()

        pass

    def xyTorowcol(self, pos):
        x = pos.x()
        y = pos.y()

        px = self.calPointOne(x)
        py = self.calPointOne(y)

        if px is not None and py is not None:
            if px <=0:
                px = 0
            elif px >= 19:
                px = 19;
            if py <= 0:
                py=0
            elif py >=19:
                py=19
            return px, py
        else:
            return -1, -1

        pass

    def calPointOne(self, p):
        m = p // self.interval
        n = p % self.interval

        if (n < self.interval * 0.5):
            ret = m
        elif (n > self.interval * 0.6):
            ret = (m + 1)
            pass
        else:
            # print('re press')
            ret = None
            pass
        return ret
        pass

    pass


if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = PicPanel()
    sys.exit(app.exec_())
    pass
