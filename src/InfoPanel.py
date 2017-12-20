#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :InfoPanel.py
 Author: FuGui
 Date: 2017/12/16-22:21
 Licence: 
 
'''
# !/usr/bin/env python3
from PyQt5.QtGui import QIcon, QPixmap, QTextBlock, QStaticText

'''
 ProjectName: kGo
 FileName :ctrlPanel.py
 Author: FuGui
 Date: 2017/12/13-21:18
 Licence: 

'''
import sys

from PyQt5.QtCore import QMargins, Qt
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton, QGridLayout, QApplication, QHBoxLayout, \
    QLabel, QTextEdit, QPlainTextEdit


class PersonView(QWidget):

    def __init__(self, *args, **kwargs):
        super(PersonView, self).__init__(*args, **kwargs)
        self.initUI()
        # self.setGeometry(100,100,480,320)

        self.show()
        pass

    def initUI(self):
        mlayout = QGridLayout(self)

        self.blackpmap = QPixmap('resource\\image\\black.gif')
        self.whitepmap = QPixmap('resource\\image\\white.gif')

        self.personstone = QLabel(self)
        self.personstone.setPixmap(self.blackpmap)

        nameLab = QLabel('Name:', self)
        self.name = QLabel('XXXX', self)
        levelLab = QLabel('Level:', self)
        self.level = QLabel('9D', self)




        mlayout.addWidget(self.personstone, 0, 0, 1, 1, Qt.AlignLeft)

        mlayout.addWidget(nameLab, 1, 0, Qt.AlignLeft)
        mlayout.addWidget(self.name, 1, 1, Qt.AlignLeft)

        mlayout.addWidget(levelLab, 2, 0, Qt.AlignLeft)
        mlayout.addWidget(self.level, 2, 1, Qt.AlignLeft)



        mlayout.setSpacing(2)
        mlayout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(mlayout)


    @property
    def Name(self):
        return self.name.text
    @Name.setter
    def Name(self,name):
        self.name.setText(name)
    @property
    def Level(self):
        return self.level.text
    @Level.setter
    def Level(self,name):
        self.level.setText(name)

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
        toplayout = QVBoxLayout(self)
        groupBox = QGroupBox(self)

        mlayout = QGridLayout(self)


        self.black = PersonView(self)
        self.black.Name = 'black'

        self.white = PersonView(self)
        self.white.setPersonStone('white')
        self.white.Name='white'
        self.white.Level='10D'

        mlayout.addWidget(self.black, 0, 0 ,1,1)
        mlayout.addWidget(self.white, 0,1, 1,1)


        groupBox.setLayout(mlayout)
        toplayout.addWidget(groupBox)

        self.mTextEditor = QTextEdit()
        self.mTextEditor.setDisabled(True)
        # self.mTextEditor.setText('VSsdfsdfffffffffffffffffsdfffffffffffffffffffffffffffffffffffffffffffffff')
        self.mTextEditor.setText('infomation')
        toplayout.addWidget(self.mTextEditor)

        self.setLayout(toplayout)
        pass
    def updateStepIndex(self,  index):
        pass



if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = InfoPanel()
    sys.exit(app.exec_())
    pass
