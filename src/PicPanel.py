#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :PicPanel.py
 Author: FuGui
 Date: 2017/12/13-23:26
 Licence: 
 
'''
import sys
from enum import Enum

from PyQt5.QtCore import QPointF, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen,  QPixmap

from src.GoEngine import GoEngine


class PicPanel(QWidget):
    mSignalTriggleRepaint = pyqtSignal()
    mSignalUpdateCurStepNum= pyqtSignal(int)

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
        self.mShowStonesIndex='ShowTriangle'

        self._goStonesEngine = GoEngine()

        self.initUI()
        self.initSignals()

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
        self.bdPixmap = QPixmap('resource\\boards\\board.png')
        self.blPixmap = QPixmap('resource\\stones\\black.png')
        self.wtPixmap = QPixmap('resource\\stones\\white.png')
        self.lastStepPixmap = QPixmap('resource\\image\\triangle.gif')
        self.stepFobidPixmap = QPixmap('resource\\image\\unhappy.png')

        self.transToQuadrate(self.bdPixmap)
        self.transToQuadrate(self.blPixmap)
        self.transToQuadrate(self.wtPixmap)

        radio = self.boardWidth / self.bdPixmap.size().width() * 0.8
        self.boardPixmap = self.bdPixmap.scaled(self.boardWidth, self.boardHeight, Qt.KeepAspectRatio)
        self.reCalculateGoImage()

        pass
    def initSignals(self):
        self.mSignalTriggleRepaint.connect(self.sigUpdateHandler)




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
        self.posPixmapbl= self.blPixmap.scaled(radio/2, radio/2, Qt.KeepAspectRatio)
        self.posPixmapwh= self.whitePixmap.scaled(radio/2, radio/2, Qt.KeepAspectRatio)
        pass

    def transToQuadrate(self, pixmap):
        if (pixmap.size().width() > pixmap.size().height()):
            pixmap.scaled(pixmap.size().height(), pixmap.size().height())
        else:
            pixmap.scaled(pixmap.size().width(), pixmap.size().width())
            pass
        pass

    def sigUpdateHandler(self):
        self.mSignalUpdateCurStepNum.emit(len(self.goStonesEngine.getStepsLists()))
        self.update()

    def paintEvent(self, QPaintEvent):

        self.initGoBoardSize()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.drawBoard(painter)
        self.drawPanelLines(painter)
        self.drawNum(painter)
        self.drawPoints(painter)
        self.drawMousePos(painter)

        pass

    def drawBoard(self, painter):
        painter.drawPixmap(self.rect(), self.boardPixmap)
        pass

    def drawPanelLines(self, painter):
        linecolor = QColor(70, 70, 70)
        # draw lines
        painter.setPen(QPen(linecolor, 1))

        for x in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(x, self.padding, x, (self.mboardsize - 1) * self.interval + self.padding)

        for y in range(self.padding, (self.mboardsize) * self.interval + self.padding, self.interval):
            painter.drawLine(self.padding, y, (self.mboardsize - 1) * self.interval + self.padding, y)

        # draw star
        painter.setBrush(linecolor)
        for i in [3, 9, 15]:
            for j in [3, 9, 15]:
                painter.drawEllipse(QPointF(self.padding + self.interval * i, self.padding + self.interval * j),
                                    self.interval * 0.15,
                                    self.interval * 0.15)

            pass
        pass
    def drawNum(self, painter):
        color = QColor(30, 30, 240)
        painter.setPen(QPen(color, 2))
        for i in range(19):
                painter.drawText(self.padding+self.interval*i-2, self.padding*0.9, str(i+1))
                painter.drawText(self.padding+self.interval*i-2, self.padding*(1.3)+self.interval*18, str(i+1))
        for i in range(19):
                painter.drawText(self.padding*0.7, self.padding+self.interval*i+3, chr(i+65))
                painter.drawText(self.padding*(1.2)+self.interval*18, self.padding+self.interval*i+3, chr(i+65))

        pass

    def drawMousePos(self, painter):
        color = QColor(30, 240, 30)
        painter.setPen(QPen(color, 1))
        painter.setOpacity(0.5)
        painter.drawLine(self.padding+(self.mousePos[0]-1)* self.interval, self.padding,
                         self.padding + (self.mousePos[0] - 1) * self.interval,
                         self.padding+(self.mboardsize-1)* self.interval)
        painter.drawLine(self.padding , self.padding+(self.mousePos[1]-1)* self.interval,
                         self.padding + (self.mboardsize - 1) * self.interval,
                         self.padding + (self.mousePos[1] - 1) * self.interval)
        if self.goStonesEngine.isHasStoneXY(self.mousePos[0], self.mousePos[1]) is True:
            painter.setOpacity(1)
            painter.drawPixmap((self.mousePos[0]) * self.interval - self.posPixmapwh.size().width() / 2,
                               (self.mousePos[1]) * self.interval - self.posPixmapwh.size().height() / 2,
                               self.stepFobidPixmap)
        else:
            tpointlist = self.goStonesEngine.getStepsLists()

            if tpointlist and tpointlist[-1][2]  is 'black':
                painter.drawPixmap((self.mousePos[0]) * self.interval - self.posPixmapwh.size().width() / 2,
                                       (self.mousePos[1]) * self.interval - self.posPixmapwh.size().height() / 2,
                                           self.posPixmapwh)
            else:
                painter.drawPixmap((self.mousePos[0]) * self.interval - self.posPixmapwh.size().width() / 2,
                                       (self.mousePos[1]) * self.interval - self.posPixmapwh.size().height() / 2,
                                           self.posPixmapbl)
                pass
            pass





    def drawPoints(self, painter):
        painter.setPen(QPen(QColor(230, 30, 30), 5))

        for tpoint in self.goStonesEngine.getStepsLists():
            if tpoint[2] is 'empty':
                continue

            if tpoint[2] is 'black':
                painter.drawPixmap((tpoint[0] + 1) * self.interval - self.blackPixmap.size().width() / 2,
                                   (tpoint[1] + 1) * self.interval - self.blackPixmap.size().height() / 2,
                                   self.blackPixmap)
            elif tpoint[2] is 'white':
                painter.drawPixmap((tpoint[0] + 1) * self.interval - self.blackPixmap.size().width() / 2,
                                   (tpoint[1] + 1) * self.interval - self.blackPixmap.size().height() / 2,
                                   self.whitePixmap)
            # print(self.mShowStonesIndex)
            # print(id(self.mShowStonesIndex))
            # print(id('ShowAllIndex'))
            if self.ShowStonesIndex == 'ShowAllIndex':
                painter.drawText((tpoint[0] + 1) * self.interval-3,
                                 (tpoint[1] + 1) * self.interval+3,
                                 str(self.goStonesEngine.getStepsLists().index(tpoint)+1))
                pass

        tpointlist=self.goStonesEngine.getStepsLists()
        if tpointlist:
            tpoint=tpointlist[-1]
            painter.drawPixmap((tpoint[0] + 1) * self.interval - self.lastStepPixmap.size().width() / 2,
                                (tpoint[1] + 1) * self.interval - self.lastStepPixmap.size().height() / 2,
                                self.lastStepPixmap)
            if self.mShowStonesIndex == 'ShowLastIndex':
                painter.drawText((tpoint[0] + 1) * self.interval - 3,
                                 (tpoint[1] + 1) * self.interval + 3,
                                 str(self.goStonesEngine.getStepsLists().index(tpoint)+1))


        pass

    def mouseReleaseEvent(self, cursor_event):
        px, py = self.xyTorowcol(cursor_event.pos())

        if px > 0 and py > 0:
            if self.goStonesEngine.move(px, py, None, False) is True:
                self.mSignalUpdateCurStepNum.emit(len(self.goStonesEngine.getStepsLists()))
                self.update()
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

    @property
    def ShowStonesIndex(self):
        return self.mShowStonesIndex
    @ShowStonesIndex.setter
    def ShowStonesIndex(self, text):
        self.mShowStonesIndex=text
    pass




if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = PicPanel()
    sys.exit(app.exec_())
    pass
