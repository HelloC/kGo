#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :GoEngine.py
 Author: FuGui
 Date: 2017/12/13-22:49
 Licence: 
 
'''
from enum import Enum

import numpy as np
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget

class WorkMode(Enum):
    SGF=1
    Fight=2
    Study=3


class GoEngine():
    def __init__(self, board=19):
        # stones = [[[] for i in range(board)] for i in range(board)]
        # x,y,color-w,b,e,status-visited or not, status-isLive(d)
        self.board = board
        self.stones = [[0 for i in range(board)] for i in range(board)]
        for i in range(board):
            for j in range(board):
                self.stones[i][j] = [i, j, 'empty', False, 'empty']
                pass
            pass
        self.stepsList = []
        self.deadstoneslist = []

        # mode: sgf,fight,study
        self.workMode = WorkMode.Study
        self.sgfFileList = None

        self.initAudio()

        pass

    def newGo(self):
        for t in self.stepsList:
            t[2] = 'empty'
        self.stepsList = []
        self.maudios['newGo'].play()
        pass

    def initAudio(self):
        self.maudios = {
            'move': QSound('resource\\sound\\move.wav'),
            'newGo': QSound('resource\\sound\\cleanboard.wav'),
            'clean': QSound('resource\\sound\\deadstonemore.wav'),

        }

    def stepPopLastOne(self):
        if self.stepsList:
            t = self.stepsList.pop()
            t[2] = 'empty'
            return t
        return None
        pass

    def initSGF(self, file=None):
        self.sgfFile=file
        self.workMode=WorkMode.SGF
        self.stepsList=[]
        pass

    def goStartStep(self):
        for stone in self.stepsList:
            stone[2] = 'empty'
        self.stepsList=[]
        self.maudios['clean'].play()
        pass
    def goEndStep(self):
        self.maudios['move'].play()
        pass
    def goNextStep(self):
        if self.workMode is WorkMode.SGF:
            index=len(self.stepsList)
            # print('self.sgfFile[index] ', self.sgfFile[index])
            self.move(self.sgfFile[index][0]+1, self.sgfFile[index][1]+1,self.sgfFile[index][2])
            self.maudios['move'].play()
        pass
    def goNextNodeStep(self):
        if self.workMode is WorkMode.SGF:
            index=len(self.stepsList)
            # print('goNextNodeStep index ', index)
            for i in range(index,8+index):
                # print('goNextNodeStep: ', self.sgfFile[i][0]+1 )
                # print('goNextNodeStep: ', self.sgfFile[i][1]+1 )
                # print('goNextNodeStep: ', self.sgfFile[i][2] )
                self.move(self.sgfFile[i][0]+1, self.sgfFile[i][1]+1,self.sgfFile[i][2])
            self.maudios['move'].play()
        pass
    def goPreStep(self):
        self.stepPopLastOne()
        steps= self.stepsList
        for t in self.stepsList:
            t[2] = 'empty'
        self.stepsList = []
        for t in steps:
            self.move(t[0]+1, t[1]+1, None)


        pass
    def goPreNodeStep(self):
        for i in range(8):
            self.stepPopLastOne()
            pass
        self.maudios['clean'].play()
        self.goPreStep()
        pass



    def move(self, x, y, color='empty', status=False):
        px = x-1
        py = y-1

        if self.stones[px][py][2] is 'black' or self.stones[px][py][2] is 'white':
            print('do move return False')
            return False
        if color is not None:
            self.stones[px][py][2] = color
        else:
            if not self.stepsList:
                self.stones[px][py][2]= 'black'
            else:
                self.stones[px][py][2] = 'white' if self.stepsList[-1][2] is 'black' else 'black'

        self.stones[px][py][3] = status

        self.stepsList.append(self.stones[px][py])

        ret = self.reFreshStone(self.stones[px][py])

        self.doClearStatus()
        if not ret:
            self.stepsList.pop()
            print('step not permit')

        self.maudios['move'].play()

        return ret
        pass
    def isHasStoneXY(self,x,y):
        px = x - 1
        py = y - 1
        if self.stones[px][py][2] is 'black' or self.stones[px][py][2] is 'white':
            # print('it has stones here')
            return True
        return False
        pass
    def getStepsLists(self):
        # print("getStepsLists: ",self.stepsList)
        return self.stepsList

    def doClearStatus(self):
        for t in self.stepsList:
            t[3]=False
        pass

    def reFreshStone(self, stone):
        deadstones= self.doCheckStoneAround(stone)
        self.doClearStatus()
        for st in deadstones:
            if st:
                self.collectDeadStoneList(st)
                self.doClearStatus()
                self.maudios['clean'].play()
        self.updateStepList()

        status = self.isStoneLive(stone)
        self.doClearStatus()
        if not status:
            self.collectDeadStoneList(stone)
            self.doClearStatus()
            self.updateStepList()
            return False

        return True
        pass
    def updateStepList(self):
        for st in self.deadstoneslist:
            st[4] = st[2]
            st[2]='empty'

        self.deadstoneslist=[]
        pass

    def doCheckStoneAround(self,stone):
        deadaround =[]
        around = self.getPointAroundHasDiffColor(stone)
        for st in around:
            if st :
                if not self.isStoneLive(st):
                    deadaround.append(st)
        return deadaround


    def isStoneLive(self, stone):
        # print('isStoneLive ', stone)
        stone[3] = True
        stone[4] = False
        around = self.getPointAround(stone)
        # print('around ', around)
        for st in around:
            if st :
                if st[2] is 'empty':
                    return True
                elif st[2] is stone[2] and not st[3]:
                    if self.isStoneLive(st):
                        return True

        return False
        pass
    def collectDeadStoneList(self,stone):
        # print('collectDeadStoneList start')
        self.deadstoneslist.append(stone)
        stone[3]=True
        around = self.getPointAroundHasSameColor(stone)
        # print('around ', around)
        for st in around:
            if st :
                if st[2] is stone[2] and not st[3]:
                    self.collectDeadStoneList(st)
        # print('collectDeadStoneList end')

    def getPointAround(self, stone):
        up = self.getUpStone(stone)
        down = self.getDownStone(stone)
        left = self.getLeftStone(stone)
        right = self.getRightStone(stone)

        return [up, down, left, right]
    def getPointAroundHasSameColor(self, stone):
        retlist = []
        up = self.getUpStone(stone)
        down = self.getDownStone(stone)
        left = self.getLeftStone(stone)
        right = self.getRightStone(stone)

        for st in [up, down, left, right]:
            if st and st[2] is stone[2]:
                retlist.append(st)

        return retlist

    def getPointAroundHasDiffColor(self, stone):
        retlist = []
        up = self.getUpStone(stone)
        down = self.getDownStone(stone)
        left = self.getLeftStone(stone)
        right = self.getRightStone(stone)

        for st in [up, down, left, right]:
            if st and st[2] is not stone[2] and st[2] is not 'empty':
                retlist.append(st)

        return retlist

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
        self.ge.move(1,1, 'black',True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

