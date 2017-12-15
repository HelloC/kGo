#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :ctrlPanel.py
 Author: FuGui
 Date: 2017/12/13-21:18
 Licence: 
 
'''
import sys

from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton, QGridLayout, QApplication, QHBoxLayout


class CtrlPanel(QWidget):
    def __init__(self,*args, **kwargs):
        super(CtrlPanel, self).__init__(*args, **kwargs)

        self.initUI()
        self.resize(480, 320)
        self.show()
        pass
    def initUI(self):
        # self.setGeometry(100,100, 320, 600)
        # self.initVSLayout()
        # self.initbtnLayout()

        mlayout = QVBoxLayout(self)

        mlayout.addStretch(1)

        # layout.setStretch()
        # mlayout.addWidget(self.vsGroupBox)
        #

        layout = QHBoxLayout()
        stBtn = QPushButton('Start')
        preBtn = QPushButton('Pre')
        nextBtn = QPushButton('Next')
        endBtn = QPushButton('End')

        btnlist = {'start': stBtn, 'pre': preBtn, 'next': nextBtn, 'end': endBtn}
        for btn in btnlist:
            btnlist[btn].setMaximumSize(50,30)
            # btnlist[btn].setSizePolicy()
            layout.addWidget(btnlist[btn])
        # mlayout.addWidget(stBtn)
        layout.setSpacing(1)



        # mlayout.addWidget(self.btnGroupBox)
        mlayout.addLayout(layout)

        self.setLayout(mlayout)
        pass

    def initVSLayout(self):

        self.vsGroupBox = QGroupBox()
        layout = QHBoxLayout()
        stBtn =QPushButton('Start')
        preBtn=QPushButton('Pre')
        nextBtn=QPushButton('Next')
        endBtn = QPushButton('End')

        btnlist={'start':stBtn, 'pre':preBtn, 'next':nextBtn, 'end':endBtn }
        for btn in btnlist:
            # btnlist[btn].setMaximumSize(40,30)
            layout.addWidget(btnlist[btn])

        layout.setContentsMargins(QMargins(1,1,1,1))
        self.vsGroupBox.setLayout(layout)



if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = CtrlPanel()
    sys.exit(app.exec_())
    pass