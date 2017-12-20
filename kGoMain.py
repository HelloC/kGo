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
from src.InfoPanel import InfoPanel
from src.PicPanel import PicPanel
import src.kGoSGFparser
from src.SettingPanel import SettingPanel
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

        self.initWinLayout()

        self.mSettingPanel=None

        self.setCentralWidget(self.topGroupBox)

        pass
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        pass


    def initWinLayout(self):
        self.picpanel = PicPanel(self)
        self.picpanel.mSignalUpdateCurStepNum.connect(self.doUpdateStepNumSlot)

        self.infopanel = InfoPanel(self)
        self.initCustToolBar()

        self.topGroupBox = QGroupBox(self)

        picGroupBox = QGroupBox(self)
        mVlayout = QVBoxLayout()
        mVlayout.addWidget(self.picpanel)
        picGroupBox.setLayout(mVlayout)

        infogbox = QGroupBox(self)
        mVlayout = QVBoxLayout()
        mVlayout.addWidget(self.infopanel)
        mVlayout.addStretch(1)
        infogbox.setLayout(mVlayout)

        mgridLayout = QGridLayout()
        mgridLayout.addWidget(self.custToolBar, 0,0, 1,2)
        mgridLayout.addWidget(picGroupBox, 1, 0, 1,2)
        mgridLayout.addWidget(infogbox, 0, 2, 2,1)

        self.topGroupBox.setLayout(mgridLayout)


    def initCustToolBar(self):
        self.custToolBar=QGroupBox()
        hlayout = QHBoxLayout()
        hlayout.addStretch(3)
        fileBarList = [(QIcon('resource\\toolbar\\open.png'),       self.doOpenFileAction),
                       (QIcon('resource\\toolbar\\page_save.png'),  self.doSaveFileAction),
                       (QIcon('resource\\toolbar\\new.png'),        self.doNewAction),
                       (QIcon('resource\\toolbar\\start.png'),      self.doStartAction),
                       (QIcon('resource\\toolbar\\prenode.png'),    self.doPreNodeAction),
                       (QIcon('resource\\toolbar\\pre.png'),        self.doPreAction),
                       (QIcon('resource\\toolbar\\next.png'),       self.doNextAction),
                       (QIcon('resource\\toolbar\\nextnode.png'),   self.doNextNodeAction),
                       (QIcon('resource\\toolbar\\end.png'),        self.doEndAction),
                       (QIcon('resource\\image\\setting.png'),       self.doSettingAction),
                       (QIcon('resource\\image\\info.png'),         self.doShowInfoAction),
                       ]

        for item in fileBarList:
            b = QPushButton(icon=item[0],parent =self)
            b.clicked.connect(item[1])
            b.setMaximumSize(b.minimumSizeHint())
            hlayout.addWidget(b)
            hlayout.setSpacing(1)

        hlayout.addStretch(1)

        # add a slide to show step progress
        self.mCurNumLabel = QLabel(self)
        self.mCurNumLabel.setText('0')
        self.picpanel.mSignalUpdateCurStepNum.connect(self.mCurNumLabel.setNum)

        self.mMaxNumLabel = QLabel(self)
        self.mMaxNumLabel.setText('361')

        self.mIndexSlider = QSlider(Qt.Horizontal,self)
        self.mIndexSlider.setMaximum(361)
        self.mIndexSlider.setMinimum(0)
        self.mIndexSlider.setValue(0)
        self.picpanel.mSignalUpdateCurStepNum.connect(self.mIndexSlider.setValue)


        hlayout.addWidget(self.mCurNumLabel)
        hlayout.addWidget(self.mIndexSlider)


        # self.mlcd.setMaximumWidth(20)


        hlayout.addWidget(self.mMaxNumLabel)

        hlayout.addStretch(2)

        self.custToolBar.setLayout(hlayout)

        pass

    def doNewAction(self):
        mbox = QMessageBox.question(self,
                       'K-Go',
                       "Do you want to new a Board ?",
                       QMessageBox.Yes | QMessageBox.Cancel,
                       QMessageBox.Cancel)

        if mbox == QMessageBox.Yes:
            self.mIndexSlider.setMaximum(361)
            self.mMaxNumLabel.setText('361')
            self.picpanel.newPanel()

    def doStartAction(self):
        self.picpanel.goStonesEngine.goStartStep()
        self.picpanel.mSignalTriggleRepaint.emit()
        pass
    def doPreAction(self):
        self.picpanel.goStonesEngine.goPreStep()
        self.picpanel.mSignalTriggleRepaint.emit()
        pass
    def doPreNodeAction(self):
        self.picpanel.goStonesEngine.goPreNodeStep()
        self.picpanel.mSignalTriggleRepaint.emit()

    def doNextAction(self):
        self.picpanel.goStonesEngine.goNextStep()
        self.picpanel.mSignalTriggleRepaint.emit()
        pass
    def doNextNodeAction(self):
        self.picpanel.goStonesEngine.goNextNodeStep()
        self.picpanel.mSignalTriggleRepaint.emit()
        pass
    def doEndAction(self):
        self.picpanel.goStonesEngine.goEndStep()
        self.picpanel.mSignalTriggleRepaint.emit()
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
            stonesList=self.doLoadSGFfile(fileName, None)
            if stonesList:
                self.mIndexSlider.setMaximum(len(stonesList))
                self.mMaxNumLabel.setText(str(len(stonesList)))
                self.picpanel.goStonesEngine.initSGF(stonesList)

            pass

        # kGoSGFparser.openFile(fileName)

    def doLoadSGFfile(self, pathname, move_number=None):
        stones=[]
        # print('pathname ',pathname)
        f = open(pathname, "rb")
        sgf_src = f.read()
        f.close()
        # print('sgfsrc', sgf_src)

        try:
            sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
            text=[]
            if sgf_game.get_gamename() is None :
                text.append(sgf_game.get_player_name('b') + ' VS '+sgf_game.get_player_name('w')+'\n')
            else:
                text.append((str(sgf_game.get_gamename())) + '\n')
            text.append('Winner:   '+str(sgf_game.get_winner())+'\n')
            text.append('size:     '+str(sgf_game.get_size())+'\n')
            text.append('komi:     ' +str(sgf_game.get_komi()) +'\n')
            text.append('handicap: ' +str(sgf_game.get_handicap()) +'\n')
            text.append('TotalTime:'+(str(sgf_game.get_times()/3600) if sgf_game.get_times() is not None else '0')+'\n')
            text.append('overtime: '+str(sgf_game.get_overtime())+'\n')
            text.append(str(sgf_game.get_common())+'\n')

            self.infopanel.mTextEditor.setText(''.join(text))
            self.infopanel.black.Name=sgf_game.get_player_name('b')
            self.infopanel.white.Name=sgf_game.get_player_name('w')

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
        pass

    def doSaveFileAction(self):
        print('doSaveFileAction -->')
        pass
    def doShowInfoAction(self):
        print('doShowInfoAction')
        info='''a(large) group of stones 一条（大）龙
            alive活（棋）
            aji味
            areas实地
            atari打吃
            Baduk围棋
            Black黑棋
            board棋盘
            bowl棋盒
            capture提子
            capturingraces 对杀
            compensationpoints 贴目
            connection连接
            corner角
            dame单官
            dan（业余/职业）（）段
            danpro 职业（）段
            dead死（棋）
            divinemove 胜负手
            edge边
            eye眼
            falseeyes 假眼
            fiveby five 五五
            forcingmoves 劫财
            fuseki布局
            Go围棋
            gote后手
            gridsize 棋盘尺寸（9X9，13X13，19X19）
            handicap泛指包括让子和贴目等形式在内的指导棋
            hane扳
            hayago快棋
            higheye 高目
            highkakari 高挂
            Igo围棋
            influence-orientedapproach 注重外势
            jigo和棋
            joseki定石/定式
            jungsuk定石/定式
            kakari挂
            kifu棋谱
            ko劫
            kofights 打劫
            komi贴目
            korigatachi愚形
            kosumi小尖
            kyu级
            ladder征子
            largehigh eye 超高目
            liberties气
            lightness薄
            lowkakari 低挂
            miai见合
            monkeyjump 伸腿
            move一招棋、一手棋
            moyo模样
            myoushu妙手
            nakade点杀
            net枷吃
            nidanbane 连扳
            originof heaven 天元
            outsidethe eye 目外
            outsidethe large eye 超目外
            pass停一手
            rank级别、段位
            resignation投子认负
            rule-sets（中国/日本/韩国）规则
            score点目
            seki双活
            sente先手
            separation分离/分断
            shape棋形
            side边
            smalleye 小目
            snapback倒扑
            starpoint 星位
            stone棋子
            tengen天元
            territorialapproach 注重实地
            territories实地
            tesuji手筋
            thickness厚实
            threeby three 三三
            tsumego诘棋/死活题
            Weiqi围棋
            White白棋
            yose官子
            yosu miru 试应手'''

        pass

    def doSettingAction(self):
        print('doSettingAction')
        # self.mSettingPanel.show()
        if self.mSettingPanel is None:
            self.mSettingPanel = SettingPanel()
            self.mSettingPanel.mIndexCombobox.currentTextChanged.connect(self.domShowStonesIndexSlot)
        else:
            self.mSettingPanel.show()


        pass
    def domShowStonesIndexSlot(self, text):
        self.picpanel.ShowStonesIndex=text
        self.picpanel.mSignalTriggleRepaint.emit()
        pass

    def doUpdateStepNumSlot(self, index):
        self.mIndexSlider.setValue(index)
        # print(index)
        pass
    pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    kwin = KgoWindow()
    sys.exit(app.exec_())
    pass
