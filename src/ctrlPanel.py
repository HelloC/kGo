#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :ctrlPanel.py
 Author: FuGui
 Date: 2017/12/13-21:18
 Licence: 
 
'''
import sys
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QPushButton, QGridLayout, QApplication


class CtrlPanel(QWidget):
    def __init__(self,*args, **kwargs):
        super(CtrlPanel, self).__init__(*args, **kwargs)

        self.initUI()
        self.show()
        pass
    def initUI(self):
        # self.setGeometry(100,100, 320, 600)
        self.initVSLayout()
        self.initbtnLayout()

        mlayout = QVBoxLayout(self)

        mlayout.addStretch(1)

        # layout.setStretch()
        mlayout.addWidget(self.vsGroupBox)

        mlayout.addWidget(self.btnGroupBox)

        self.setLayout(mlayout)
        pass

    def initVSLayout(self):

        self.vsGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.addWidget(QPushButton('1'), 0, 0)
        layout.addWidget(QPushButton('2'), 0, 1)
        layout.addWidget(QPushButton('3'), 1, 0)
        layout.addWidget(QPushButton('4'), 1, 1)

        self.vsGroupBox.setLayout(layout)

    def initbtnLayout(self):

        self.btnGroupBox = QGroupBox()

        layout = QGridLayout()
        layout.addWidget(QPushButton('1'), 0, 0)
        layout.addWidget(QPushButton('2'), 0, 1)
        layout.addWidget(QPushButton('3'), 0, 2)
        layout.addWidget(QPushButton('4'), 1, 0)
        layout.addWidget(QPushButton('5'), 1, 1)
        layout.addWidget(QPushButton('6'), 1, 2)
        layout.addWidget(QPushButton('7'), 2, 0)
        layout.addWidget(QPushButton('8'), 2, 1)
        layout.addWidget(QPushButton('9'), 2, 2)

        self.btnGroupBox.setLayout(layout)
    pass

if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = CtrlPanel()
    sys.exit(app.exec_())
    pass