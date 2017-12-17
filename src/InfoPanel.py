#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :InfoPanel.py
 Author: FuGui
 Date: 2017/12/16-22:21
 Licence: 
 
'''
# !/usr/bin/env python3
from PyQt5.QtGui import QIcon, QPixmap

'''
 ProjectName: kGo
 FileName :ctrlPanel.py
 Author: FuGui
 Date: 2017/12/13-21:18
 Licence: 

'''
import sys

from PyQt5.QtCore import QMargins, Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton, QGridLayout, QApplication, QHBoxLayout, QLabel


class PersonView(QWidget):
    def __init__(self, *args, **kwargs):
        super(PersonView, self).__init__(*args, **kwargs)
        self.initUI()
        # self.setGeometry(100,100,480,320)
        self.show()
        pass

    def initUI(self):
        mlayout = QGridLayout(self)

        self.blackpmap=QPixmap('resource\\image\\black.gif')
        self.whitepmap=QPixmap('resource\\image\\white.gif')

        self.personstone = QLabel(self)
        # person.setScaledContents(True)
        self.personstone.setPixmap(self.blackpmap)

        # self.portrait = QLabel(self)
        # # portrait.setScaledContents(True)
        # # self.portrait.setPixmap(self.blackpmap)

        nameLab = QLabel('Name:',self)
        self.name = QLabel('XXXX', self)
        levelLab = QLabel('Level:', self)
        self.level = QLabel('9D',self)

        mlayout.addWidget(self.personstone, 0,0, 1,1, Qt.AlignLeft)
        # mlayout.addWidget(self.portrait, 0,1)

        mlayout.addWidget(nameLab, 1,0, Qt.AlignLeft)
        mlayout.addWidget(self.name, 1,1, Qt.AlignHCenter)

        mlayout.addWidget(levelLab, 2,0, Qt.AlignLeft)
        mlayout.addWidget(self.level, 2,1, Qt.AlignHCenter)
        mlayout.setSpacing(2)
        mlayout.setContentsMargins(20,20,20,20)
        self.setLayout(mlayout)
    def setPersonStone(self, stone=None):
        if not stone:
            return False
        if stone is 'black':
            self.personstone.setPixmap(self.blackpmap)
        elif stone is 'white':
            self.personstone.setPixmap(self.whitepmap)
        else:
            return False
        return True
        pass
    pass

class InfoPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super(InfoPanel, self).__init__(*args, **kwargs)

        self.initUI()
        # self.resize(480, 320)
        self.show()
        pass

    def initUI(self):
        # self.setGeometry(100,100, 320, 600)
        # self.initVSLayout()
        # self.initbtnLayout()
        toplayout = QHBoxLayout(self)
        groupBox = QGroupBox(self)

        mlayout = QHBoxLayout(self)
        self.black = PersonView(self)
        self.white = PersonView(self)
        self.white.setPersonStone('white')
        mlayout.addWidget(self.black)
        mlayout.addWidget(self.white)

        groupBox.setLayout(mlayout)
        toplayout.addWidget(groupBox)
        self.setLayout(toplayout)
        pass

  


if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = InfoPanel()
    sys.exit(app.exec_())
    pass
