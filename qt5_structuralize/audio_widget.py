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

class audioWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.view_width= 910 ##QGraphicsView resolution
        self.view_height= 100 ##QGraphcsView
        self.play_state = False
        #####################       eye tracking        #####################

        self.layout = QtWidgets.QVBoxLayout(self)
        self.player = QM.QMediaPlayer()

        self.videoItem = QGraphicsVideoItem()
        #self.videoItem.setAspectRatioMode(QtCore.Qt.KeepAspectRatio)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.player.setVideoOutput(self.videoItem)
        self.scene.addItem(self.videoItem)

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
        #self.positionSlider.valueChanged.connect(self.setPosition)

        # play button
        self.hbuttonbox = QtWidgets.QHBoxLayout()
        # self.playbutton = QtWidgets.QPushButton("Play")
        # self.hbuttonbox.addWidget(self.playbutton)
        # self.playbutton.clicked.connect(self.play_pause)

        self.openbutton = QtWidgets.QPushButton("Open audio")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)


        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.player.setNotifyInterval(100)
        self.player.positionChanged.connect(self.updateUI)
        #self.player.positionChanged.connect(self.printTime)
        self.player.durationChanged.connect(self.setRange)
        #self.player.stateChanged.connect(self.setButtonCaption)
        self.setLayout(self.layout)

    

    # def printTime(self):
    #     return
    #     #print(self.player.position())

    # def setButtonCaption(self,state):
    #     if self.player.state() == QM.QMediaPlayer.PlayingState:
    #         self.playbutton.setText("Pause")
    #     else:
    #         self.playbutton.setText("Play")

    def open_file(self):
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
        if not filename:
            return
        url = QtCore.QUrl.fromLocalFile(filename)
        content = QM.QMediaContent(url)
        #self.videoItem.setAspectRatioMode(1)
        self.player.setMedia(content)
        #self.playbutton.setText("Play")

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = audioWidget()
    w.show()
    sys.exit(app.exec_())
