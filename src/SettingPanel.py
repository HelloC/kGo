#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :SettingPanel.py
 Author: FuGui
 Date: 2017/12/19-16:38
 Licence: 
 
'''
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QMenu, QActionGroup, QAction, QComboBox, \
    QHBoxLayout


class SettingPanel(QWidget):
    mSignalShowIndex=pyqtSignal(str)
    def __init__(self,*args, **kwargs):
        super(SettingPanel, self).__init__(*args, **kwargs)
        self.title='k-Go Setting'
        # self.setGeometry(200,200, 480,320)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        # Create widget
        topLayout=QHBoxLayout()
        label = QLabel('StonesIndex',self)
        self.initShowIndex()

        topLayout.addWidget(label)
        topLayout.addWidget(self.mIndexCombobox)
        topLayout.addStretch(1)
        self.setLayout(topLayout)

        self.show()
        pass
    def initShowIndex(self):
        # self.btnSetting = QPushButton(icon=QIcon('resource\\image\\setting.png'), parent=self)
        self.mIndexCombobox = QComboBox(self)
        self.mIndexCombobox.addItem("ShowLastIndex")
        self.mIndexCombobox.addItem("ShowAllIndex")
        self.mIndexCombobox.addItem("ShowTriangle")
        self.mIndexCombobox.setCurrentText('ShowTriangle')
        # self.mIndexCombobox.currentTextChanged.connect(self.mSignalShowIndex)
        pass
    def doIndexBoxSlot(self, text):
        print('textL: ', text)
        pass
    pass
if __name__ == '__main__':
    print(__file__ + __name__)
    app = QApplication(sys.argv)
    kwin = SettingPanel()
    sys.exit(app.exec_())
    pass