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

from sgfmill import sgf, sgf_moves, ascii_boards
from src import kGoSGFparser
from src.InfoPanel import InfoPanel
from src.PicPanel import PicPanel
import src.kGoSGFparser
from src.ctrlPanel import CtrlPanel


class KgoWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(KgoWindow, self).__init__(*args, **kwargs)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.title = 'K-Go'
        self.left = 400
        self.top = 400
        self.width = 820
        self.height = 880
        # self.setMinimumSize(self.width, self.height)
        # self.setMaximumSize(self.width, self.height)
        self.sgflist=[]


        self.initUI()
        self.center()
        self.show()
        pass

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('resource\\image\\app.ico'))

        # self.initMenu()
        self.initStatusBar()
        # self.initToolBars()
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
        self.initCustToolBar()
        self.picpanel = PicPanel(self)
        self.picpanel.sigRepaint.connect(self.doResponsePicPanelRepaint)
        # self.picpanel.goStonesEngine.sigStepsNum.connect(self.doResponsePicPanelRepaint)

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
        mgridLayout.addWidget(self.custToolBar, 0,0, 1,2)
        mgridLayout.addWidget(picGroupBox, 1, 0, 1,2)
        mgridLayout.addWidget(infogbox, 0, 2, 2,1)
        # self.setLayout(mgridLayout)
        self.topGroupBox.setLayout(mgridLayout)

    def initCustToolBar(self):
        self.custToolBar=QGroupBox()
        hlayout = QHBoxLayout()
        hlayout.addStretch(1)
        fileBarList = [(QIcon('resource\\toolbar\\open.png'),       self.doOpenFileAction),
                       (QIcon('resource\\toolbar\\page_save.png'),  self.doSaveFileAction),
                       (QIcon('resource\\toolbar\\new.png'),        self.doNewAction),
                       (QIcon('resource\\toolbar\\start.png'),      self.doStartAction),
                       (QIcon('resource\\toolbar\\prenode.png'),    self.doPreNodeAction),
                       (QIcon('resource\\toolbar\\pre.png'),        self.doPreAction),
                       (QIcon('resource\\toolbar\\next.png'),       self.doNextAction),
                       (QIcon('resource\\toolbar\\nextnode.png'),   self.doNextNodeAction),
                       (QIcon('resource\\toolbar\\end.png'),        self.doEndAction),
                       (QIcon('resource\\image\\info.png'),         self.doShowInfoAction),
                       ]

        for item in fileBarList:
            b = QPushButton(icon=item[0],parent =self)
            b.clicked.connect(item[1])
            b.setMaximumSize(b.minimumSizeHint())
            hlayout.addWidget(b)
            hlayout.setSpacing(1)

        btnSetting=QPushButton(icon=QIcon('resource\\image\\setting.png'), parent=self)

        mNumMenu= QMenu()
        mshowtGroup = QActionGroup(self)
        mshowtGroup.setExclusive(True)

        mShowNum=QAction('show ALl num', mshowtGroup)
        mShowNum.setCheckable(True)
        mLastNum=QAction('show Last num', mshowtGroup)
        mLastNum.setCheckable(True)

        mShowTriangle=QAction('show Triangle',mshowtGroup)
        mShowTriangle.setCheckable(True)
        mShowTriangle.setChecked(True)

        mNumMenu.addAction(mShowNum)
        mNumMenu.addAction(mLastNum)
        mNumMenu.addAction(mShowTriangle)
        # mNumMenu
        btnSetting.setMenu(mNumMenu)

        # btnSet.clicked.connect(self.doSettingAction)
        hlayout.addWidget(btnSetting)

        hlayout.addStretch(1)
        self.custToolBar.setLayout(hlayout)

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
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Current Step: 0')

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
        # print('fileName1', fileName)
        # print('filetype', filetype)
        # self.picpanel.goStonesEngine.initSGF(fileName)
        if fileName:
            stones=self.doLoadSGFfile(fileName, None)
            if stones:
                self.picpanel.goStonesEngine.initSGF(stones)

            pass

        # kGoSGFparser.openFile(fileName)

    def doLoadSGFfile(self, pathname, move_number=None):
        stones=[]
        print('pathname ',pathname)
        f = open(pathname, "rb")
        sgf_src = f.read()
        f.close()
        # print('sgfsrc', sgf_src)

        try:
            sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
        except ValueError:
            raise Exception("bad sgf file")

        try:
            board, plays = sgf_moves.get_setup_and_moves(sgf_game)
        except ValueError as e:
            raise Exception(str(e))
        if move_number is not None:
            move_number = max(0, move_number - 1)
            plays = plays[:move_number]

        for colour, move in plays:
            if move is None:
                continue
            # print('move ', move)
            if colour is 'w':
                stones.append([move[0], move[1], 'white'])
            elif colour is 'b':
                stones.append([move[0], move[1], 'black'])
            else:
                print('color error')
            # row, col = move
            # print("stones:",row,' ',col, ' ', colour)

        return stones

        # print('board ', board)
        # print(ascii_boards.render_board(board))
        print()
        pass

    def doSaveFileAction(self):
        print('doSaveFileAction -->')
        pass
    def doShowInfoAction(self):

        pass

    def doSettingAction(self):
        pass

    def doResponsePicPanelRepaint(self, index):
        self.statusBar.showMessage('Current Step: '+ str(index))
        self.infopanel.updateStepIndex(index)
        # print(index)
        pass
    pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    kwin = KgoWindow()
    sys.exit(app.exec_())
    pass
