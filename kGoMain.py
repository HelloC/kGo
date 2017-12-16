#!/usr/bin/env python3
'''
 ProjectName: kGo
 FileName :kGoMain.py
 Author: FuGui
 Date: 2017/12/12-12:56
 Licence: 
 
'''

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src import kGoSGFparser
from src.InfoPanel import InfoPanel
from src.PicPanel import PicPanel
import src.kGoSGFparser
from src.ctrlPanel import CtrlPanel


class KgoWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(KgoWindow, self).__init__(*args, **kwargs)
        self.title = 'K-Go'
        self.left = 400
        self.top = 400
        self.width = 820
        self.height = 880
        # self.setMinimumSize(self.width, self.height)
        # self.setMaximumSize(self.width, self.height)


        self.initUI()
        self.center()
        self.show()
        pass

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('src\\resource\\image\\app.ico'))

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
        self.infopanel = InfoPanel(self)
        # self.ctrlpanel = CtrlPanel(self)

        self.topGroupBox = QGroupBox(self)

        picGroupBox = QGroupBox(self)
        mVlayout = QVBoxLayout()
        # mVlayout = QGridLayout()
        # mVlayout.addWidget(self.picpanel, 0,0, 1, 5)
        # mVlayout.addWidget(self.ctrlpanel, 1,2, 1,1)
        mVlayout.addWidget(self.picpanel)
        picGroupBox.setLayout(mVlayout)

        infogbox = QGroupBox(self)
        mVlayout = QVBoxLayout()
        mVlayout.addWidget(self.infopanel)
        mVlayout.addStretch(1)
        infogbox.setLayout(mVlayout)

        # mlayout = QHBoxLayout()
        # mlayout.addWidget(self.picpanel)
        # mlayout.addWidget(self.ctrlpanel)

        # self.setLayout(self.mlayout)
        mgridLayout = QGridLayout()
        mgridLayout.addWidget(picGroupBox, 0, 0)
        mgridLayout.addWidget(infogbox, 0, 1)
        # self.setLayout(mgridLayout)
        self.topGroupBox.setLayout(mgridLayout)


    def initMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        setMenu = mainMenu.addMenu('Setting')
        helpMenu = mainMenu.addMenu('Help')

        fileMenu.addAction(self.newMenuAction(text='Open', slot=self.doOpenFileAction))
        fileMenu.addAction(self.newMenuAction(text='Exit',icon=QIcon('exit24.png'),tip='Exit application',slot=self.close,shortcut='Ctrl+Q'))
        pass
    def initToolBars(self):

        self.mTBarFile = self.addToolBar('FileBar')
        FileBarList = [('Open', QIcon('src\\resource\\image\\open.png'), 'Open SGF File', self.doOpenFileAction),
                       ('Open', QIcon('src\\resource\\image\\page_save.png'), 'Save SGF File', self.doSaveFileAction),
                       ]
        for item in FileBarList:
            act = QAction(item[0], self)
            act.setIcon(item[1])
            act.setToolTip(item[2])
            act.triggered.connect(item[3])
            self.mTBarFile.addAction(act)

        self.mTbarBoard = self.addToolBar('BoardBar')
        BoardBarList = [('New',     QIcon('src\\resource\\image\\new.png'),     'Create A Board',   self.doNewAction),
                       ('start',    QIcon('src\\resource\\image\\start.png'),   'Go start step',    self.doStartAction),
                       ('PreTen',   QIcon('src\\resource\\image\\preten.png'),  'Pre Node step',     self.doPreNodeAction),
                       ('Pre',      QIcon('src\\resource\\image\\pre.png'),     'Pre step',         self.doPreAction),
                       ('next',     QIcon('src\\resource\\image\\next.png'),    'next step',        self.doNextAction),
                       ('nextTen',  QIcon('src\\resource\\image\\nextten.png'), 'next Node step',    self.doNextNodeAction),
                       ('end',      QIcon('src\\resource\\image\\end.png'),     'Go end step',      self.doEndAction)
                       ]

        for item in BoardBarList:
            act = QAction(item[0], self)
            act.setIcon(item[1])
            act.setToolTip(item[2])
            act.triggered.connect(item[3])
            self.mTbarBoard.addAction(act)
    pass

    def doNewAction(self):
        mbox = QMessageBox.question(self,
                       'K-Go',
                       "Do you want to new a Board ?",
                       QMessageBox.Yes | QMessageBox.Cancel,
                       QMessageBox.Cancel)

        if mbox == QMessageBox.Yes:
            self.picpanel.newPanel()

    def doStartAction(self):
        self.picpanel.goStonesEngine.goStartStep()
        self.picpanel.sigUpdate.emit()
        pass
    def doPreAction(self):
        self.picpanel.goStonesEngine.goPreStep()
        self.picpanel.sigUpdate.emit()
        pass
    def doPreNodeAction(self):
        self.picpanel.goStonesEngine.goPreNodeStep()
        self.picpanel.sigUpdate.emit()

    def doNextAction(self):
        self.picpanel.goStonesEngine.goNextStep()
        self.picpanel.sigUpdate.emit()
        pass
    def doNextNodeAction(self):
        self.picpanel.goStonesEngine.goNextNodeStep()
        self.picpanel.sigUpdate.emit()
        pass
    def doEndAction(self):
        self.picpanel.goStonesEngine.goEndStep()
        self.picpanel.sigUpdate.emit()
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

    def doOpenFileAction(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                          "Select A SGF File",
                                                          "SGF",
                                                          "SGF Files (*.sgf)")
        print('fileName1', fileName)
        print('filetype', filetype)
        # self.picpanel.goStonesEngine.initSGF(fileName)
        if fileName:
            kGoSGFparser.openFile(fileName)

    def doSaveFileAction(self):
        print('doSaveFileAction -->')
        pass
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kwin = KgoWindow()
    sys.exit(app.exec_())
    pass
