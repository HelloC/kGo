#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :kGoMain.py
 Author: FuGui
 Date: 2017/12/12-12:56
 Licence: 
 
'''
import PyQt5

import sys

from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.PicPanel import PicPanel
from src.ctrlPanel import CtrlPanel
from src.kPanel import KPanel


class KgoWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(KgoWindow, self).__init__(*args, **kwargs)
        self.title = 'K-Go'
        self.left = 400
        self.top = 400
        self.width = 880
        self.height = 900
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)


        self.initUI()
        self.center()
        self.show()
        pass

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initMenu()
        self.initStatusBar()
        self.initToolBars()
        self.initWinLayout()

        self.setCentralWidget(self.topGroupBox)

        pass
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        pass


    def initWinLayout(self):
        # self.wpanel = KPanel(self)
        self.picpanel = PicPanel(self)
        # self.ctrlpanel = CtrlPanel(self)

        self.topGroupBox = QGroupBox(self)

        mlayout = QVBoxLayout()
        mlayout.addWidget(self.picpanel)



        self.topGroupBox.setLayout(mlayout)
        # self.setLayout(self.mlayout)



    def initMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        setMenu = mainMenu.addMenu('Setting')
        helpMenu = mainMenu.addMenu('Help')

        fileMenu.addAction(self.newMenuAction(text='Open',slot=self.openFile))
        fileMenu.addAction(self.newMenuAction(text='Exit',icon=QIcon('exit24.png'),tip='Exit application',slot=self.close,shortcut='Ctrl+Q'))
        pass
    def initToolBars(self):
        self.toolbar = self.addToolBar('toolbar')
        startAction = QAction( 'start', self)
        exitAction = QAction( 'Exit', self)
        exitAction = QAction( 'Exit', self)

        startAction.setStatusTip('start a new')

        exitAction.triggered.connect(qApp.quit)

        self.toolbar.addAction(startAction)
        self.toolbar.addAction(exitAction)

    pass

    def initStatusBar(self):
        statusBar = self.statusBar()
        statusBar.showMessage('Message in statusbar.')

        pass

    def newMenuAction(self, text="newaction", icon=None, tip=None, slot=None, shortcut=None):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        return action

        pass

    def openFile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "/Users/Kelisiya/Desktop",
                                                          "All Files (*);;Text Files (*.txt)")
        print(fileName1, filetype)

    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kwin = KgoWindow()
    sys.exit(app.exec_())
    pass
