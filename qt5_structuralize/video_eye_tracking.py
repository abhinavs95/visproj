import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import PyQt5.QtMultimedia as QM
import utility
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as np
import math
import random
import pandas

class eyeTrackingWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.view_width= 910 ##QGraphicsView resolution
        self.view_height= 300 ##QGraphcsView
        self.play_state = False
        self.gesture_dict = {0:'metaphoric',1:'beats',2:'deictics',3:'iconic'}
        self.ges_dict=None
        self.one = ''
        self.two = ''
        self.time = -1
        #####################       eye tracking        #####################

        self.layout = QtWidgets.QVBoxLayout(self)
        self.player = QM.QMediaPlayer()

        # self.qv = QVideoWidget()
        # self.scene = QGraphicsScene()
        # self.scene.setSceneRect(0, 0, self.view_width, self.view_height);
        # self.player.setVideoOutput(self.qv)
        # self.proxy = self.scene.addWidget(self.qv)
        # self.view = QGraphicsView(self.scene, self)

        self.videoItem = QGraphicsVideoItem()
        #self.videoItem.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.player.setVideoOutput(self.videoItem)
        self.scene.addItem(self.videoItem)

        self.label = QtWidgets.QLabel()
        self.label.setFixedWidth(200)
        self.label.setFixedHeight(self.view_height)
        self.scene.addWidget(self.label)

        self.view.setGeometry(0, 0, self.view_width, self.view_height)
        self.scene.setSceneRect(0, 0, self.view_width, self.view_height)
        self.videoItem.setSize(QtCore.QSizeF(self.view_width, self.view_height))
        #self.videoItem.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        self.videoItem.setPos(0, 0)
        self.layout.addWidget(self.view)

        self.createUI()
        self.view.show()


        # player.setInterval(self.eye_track_frame_rate)
        # timer.timeout.connect(self.draw_eye_tracking)

    def createUI(self):

        # video position slider
        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.valueChanged.connect(self.display_gesture)

        # play button
        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)

        self.openbutton = QtWidgets.QPushButton("Open video")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)

        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.player.setNotifyInterval(1000)
        self.player.positionChanged.connect(self.updateUI)
        #self.player.positionChanged.connect(self.printTime)
        self.player.durationChanged.connect(self.setRange)
        self.player.stateChanged.connect(self.setButtonCaption)
        self.setLayout(self.layout)

    def setButtonCaption(self,state):
        if self.player.state() == QM.QMediaPlayer.PlayingState:
            self.playbutton.setText("Pause")
        else:
            self.playbutton.setText("Play")

    def open_file(self):
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
        if not filename:
            return
        url = QtCore.QUrl.fromLocalFile(filename)
        content = QM.QMediaContent(url)
        #self.videoItem.setAspectRatioMode(1)
        self.player.setMedia(content)
        f = open('../../test_ges.txt').readlines()
        self.ges_dict = {}
        for i in f:
            t=i.strip().split()
            self.ges_dict[int(t[1])]=self.gesture_dict[int(t[0])]
        self.playbutton.setText("Play")

    def play_pause(self):
        #self.videoItem.setSize(QtCore.QSizeF(self.view_width, self.view_height))

        if self.player.state() == QM.QMediaPlayer.PlayingState:
            self.play_state = False
            self.player.pause()
        else:
            self.play_state = True
            self.player.play()

    def get_state(self):
    	return QM.QMediaPlayer.PlayingState

    def setPosition(self, position):
        self.positionSlider.setValue(position)
        self.player.setPosition(position)

    def setRange(self, duration):
        self.positionSlider.setRange(0, self.player.duration())

    def updateUI(self, position):
        self.positionSlider.setValue(position)
    
    def display_gesture(self):
        #print(self.positionSlider.value())
        if self.time != int(self.positionSlider.value()/1000):
            self.time = int(self.positionSlider.value()/1000)
            if self.time in self.ges_dict.keys():
                self.three = self.two
                self.two = self.one
                self.one = self.ges_dict[self.time]+' '+'<font size=3>'+str(self.time)+'</font><br><br>'
                self.label.setText("<h1><b><font size=8>"+self.one+"</font><font size=5>"+self.two+"</font><font size=3>"+self.three+"</font></b>")
                # label = QtWidgets.QLabel("<h1><b><font size=5>"+"Testing!"+"</font></b>")
                # self.scene.addWidget(label)#,1,0,QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = eyeTrackingWidget()
    w.show()
    sys.exit(app.exec_())
