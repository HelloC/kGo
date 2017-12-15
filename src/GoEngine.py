#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :GoEngine.py
 Author: FuGui
 Date: 2017/12/13-22:49
 Licence: 
 
'''
import numpy as np
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget


class GoEngine():
    def __init__(self, board=19):
        # stones = [[[] for i in range(board)] for i in range(board)]
        # x,y,color-w,b,e,status-visited or not
        self.board = board
        self.stones = [[0 for i in range(board)] for i in range(board)]
        for i in range(board):
            for j in range(board):
                self.stones[i][j] = [i, j, 'e', False]
                pass
            pass
        self.stepsList = []
        self.deadstones = []
        # print(self.stones)

        pass

    def newGo(self):
        for t in self.stepsList:
            t[2] = 'e'
        self.stepsList = []
        pass
    def stepPopLastOne(self):
        if self.stepsList:
            t = self.stepsList.pop()
            t[2] = 'e'
        pass


    def move(self, x, y, color='e', status=False):

        # print("move ",x, ' ', y, " ", color, ' ', status)
        px = x-1
        py = y-1
        if self.stones[px][py][2] is 'b' or self.stones[px][py][2] is 'w':
            print('do move return False')
            return False

        self.stones[px][py][2] = color
        self.stones[px][py][3] = status

        # print('move stone:', self.stones[px][py])

        # print('do self.stepsList.append')
        self.stepsList.append(self.stones[px][py])

        # print('do reFreshStone')
        ret = self.reFreshStone(self.stones[px][py])

        self.doClearStatus()
        # print('do move end ret=',ret)

        return ret
        pass
    def getStepsLists(self):
        # print("getStepsLists: ",self.stepsList)
        return self.stepsList

    def doClearStatus(self):
        for t in self.stepsList:
            t[3]=False
        pass

    def reFreshStone(self, stone):
        # self.findFiberty(stone)
        # if self.doStonesUpdate(stone):
        if not self.isHasDeadStonesAround(stone):
            if self.isStoneDead(stone):
                return False
        return True

        pass
    def isStoneDead(self, stone):
        print('doStonesUpdate itself')
        isLivestone = self.doDeadStoneCheck(stone)
        self.doClearStatus()
        print('isLivestone ', isLivestone)

        if not isLivestone:
            self.deadstones.append(stone)
            self.doDeadStonesCollect(stone)
        return isLivestone

    def isHasDeadStonesAround(self, stone):
        left = self.getLeftStone(stone)
        right = self.getRightStone(stone)
        up = self.getUpStone(stone)
        down = self.getDownStone(stone)

        if left and left[2] is not 'e' and left[2] is not stone[2]:
            isLivestone=self.doDeadStoneCheck(left)
            self.doClearStatus()
            if not isLivestone:
                self.deadstones.append(left)
                self.doDeadStonesCollect(left)

        if right and right[2] is not 'e' and  right[2] is not stone[2]:
            isLivestone=self.doDeadStoneCheck(right)
            self.doClearStatus()
            if not isLivestone:
                self.deadstones.append(right)
                self.doDeadStonesCollect(right)

        if up and up[2] is not 'e' and  up[2] is not stone[2]:
            isLivestone=self.doDeadStoneCheck(up)
            self.doClearStatus()
            if not isLivestone:
                self.deadstones.append(up)
                self.doDeadStonesCollect(up)

        if down and down[2] is not 'e' and  down[2] is not stone[2]:
            isLivestone=self.doDeadStoneCheck(down)
            self.doClearStatus()
            if not isLivestone:
                self.deadstones.append(down)
                self.doDeadStonesCollect(down)
                pass
            pass
        if self.deadstones is None:
            return False

        for item in self.deadstones:
            item[2] = 'e'

        self.deadstones = []
        return True
        pass






    def doDeadStonesCollect(self,stone):
        stone[3] = True
        left = self.getLeftStone(stone)
        if left and left[2] is stone[2] and not left[3]:
            left[3]=True
            self.deadstones.append(left)
            self.doDeadStonesCollect(left)

        right = self.getRightStone(stone)
        if right and right[2] is stone[2] and not right[3]:
            right[3]=True
            self.deadstones.append(right)
            self.doDeadStonesCollect(right)

        up = self.getUpStone(stone)
        if up and up[2] is stone[2] and not up[3]:
            up[3]=True
            self.deadstones.append(up)
            self.doDeadStonesCollect(up)
        down = self.getDownStone(stone)
        if down and down[2] is stone[2] and not down[3]:
            down[3]=True
            self.deadstones.append(down)
            self.doDeadStonesCollect(down)

        pass

    def doDeadStoneCheck(self, stone):
        stone[3]=True

        left = self.getLeftStone(stone)
        if left and left[2] is 'e':
            return True
        right = self.getRightStone(stone)
        if right and right[2] is 'e':
            return True
        up = self.getUpStone(stone)
        if up and up[2] is 'e':
            return True
        down = self.getDownStone(stone)
        if down and down[2] is 'e':
            return True

        if left and left[2] is stone[2] and not left[3]:
            return self.doDeadStoneCheck(left)


        if right and right[2] is stone[2] and not right[3]:
            return self.doDeadStoneCheck(right)

        if up and up[2] is stone[2] and not up[3]:
            return self.doDeadStoneCheck(up)

        if down and down[2] is stone[2] and not down[3]:
            return self.doDeadStoneCheck(down)

        return False
        pass

    def getLeftStone(self, stone):
        # print('getLeftStone: ', stone)
        x = stone[0] - 1
        y = stone[1]
        if x >= 0 and x < self.board:
            return self.stones[x][y]
        else:
            return None
        pass

    def getRightStone(self, stone):
        x = stone[0] + 1
        y = stone[1]
        if x >= 0 and x < self.board:
            return self.stones[x][y]
        else:
            return None
        pass

    def getUpStone(self, stone):
        x = stone[0]
        y = stone[1] - 1
        if y >= 0 and y < self.board:
            return self.stones[x][y]
        else:
            return None
        pass

    def getDownStone(self, stone):
        x = stone[0]
        y = stone[1] + 1
        if y >= 0 and y < self.board:
            return self.stones[x][y]
        else:
            return None
        pass

    pass


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.ge = GoEngine()

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        self.ge.move(1,1, 'b',True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

