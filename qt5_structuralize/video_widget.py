import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets, QtOpenGL
import PyQt5.QtMultimedia as QM
import utility
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
import numpy as np
import math
import random
import pandas
import vlc
import pyqtgraph

class videoWidget(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		QtWidgets.QWidget.__init__(self, *args, **kwargs)
		self.view_width= 710 
		self.view_height= 300
		# for rolling gesture view
		self.play_state = False
		self.gesture_dict = {0:'metaphoric',1:'beats',2:'deictics',3:'iconic'}
		self.ges_dict = {}
		self.one = ''
		self.two = ''
		self.time = -1
		self.noseData = None

		self.line = QtWidgets.QGraphicsLineItem()
		self.pen = QtGui.QPen()
		self.pen.setWidth(5)
		self.pen.setBrush(QtGui.QColor(0, 0, 255, 200))
		self.line.setPen(self.pen)

		# vlc widget
		# self.instance = vlc.Instance()
		# self.mediaplayer = self.instance.media_player_new()
		# self.mediaplayer.video_set_aspect_ratio('16:4')
		# self.isPaused = True

		self.view = QtWidgets.QGraphicsView()
		self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.view.setViewport(QtOpenGL.QGLWidget())
		self.view.setFixedSize(self.view_width,self.view_height)
		self.view.setGeometry(0,0,self.view_width,self.view_height)
		self.videoItem = QGraphicsVideoItem()

		# MUST setsize that is half the size of the GraphicsView
		# Most likey a bug in Qt's implementation on Mac OS X
		self.videoItem.setSize(QtCore.QSizeF(self.view_width/2,self.view_height/2))

		self.player = QM.QMediaPlayer()
		self.player.setVideoOutput(self.videoItem)

		self.scene = QtWidgets.QGraphicsScene()
		self.scene.addItem(self.videoItem)
		self.scene.addItem(self.line)

		self.view.setScene(self.scene)
		self.scene.setSceneRect(0, 0, self.view_width, self.view_height)
		self.videoItem.setPos(0,0)

		self.label = QtWidgets.QLabel()
		self.label.setFixedWidth(200)
		self.label.setFixedHeight(self.view_height)


		self.layout1 = QtWidgets.QGridLayout()
		self.layout1.addWidget(self.label,0,0)
		self.layout1.addWidget(self.view,0,1)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addLayout(self.layout1)

		#plot widget
		self.graph_widget = QtWidgets.QWidget()
        # Layout of Container Widget
		self.graph_layout = QtWidgets.QVBoxLayout()
		self.graph_widget.setLayout(self.graph_layout)
		self.layout.addWidget(self.graph_widget)

		self.createUI()
		self.view.show()

	def createUI(self):
		# vlc widget
		# self.vlcWidget = QtWidgets.QWidget(self)
		# self.vlcWidget.setGeometry(QtCore.QRect(0, 0, 910, 300))

		# self.vboxlayout = QtWidgets.QVBoxLayout()
		# self.vlcWidget.setLayout(self.vboxlayout)
		# self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
		# self.palette = self.videoframe.palette()
		# self.palette.setColor (QtGui.QPalette.Window,
		#                        QtGui.QColor(0,0,0))
		# self.videoframe.setPalette(self.palette)
		# self.videoframe.setAutoFillBackground(True)
		# #self.videoframe.resize(300,300)
		# self.vboxlayout.addWidget(self.videoframe)
		# self.layout.addWidget(self.vlcWidget)

		
		self.graph_view = pyqtgraph.PlotWidget(self)
		self.graph_view.setGeometry(QtCore.QRect(0,0,910,300))
		self.graph_view.setXRange(-100,100)
		self.graph_view.setYRange(0,68)
		self.graph_layout.addWidget(self.graph_view)

		self.hbuttonbox = QtWidgets.QHBoxLayout()



        # self.vboxlayout = QtWidgets.QVBoxLayout()
        # self.vboxlayout.addWidget(self.videoframe)
        # self.vboxlayout.addWidget(self.positionSlider)
        # self.vboxlayout.addLayout(self.hbuttonbox)

        # self.setLayout(self.vboxlayout)

        # self.timer = QtCore.QTimer(self)
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.updateUI)




		# video position slider
		self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
		self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
		                        "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
		self.positionSlider.sliderMoved.connect(self.setPosition)
		self.positionSlider.valueChanged.connect(self.display_gesture)

		# play button
		self.playbutton = QtWidgets.QPushButton("Play")
		self.hbuttonbox.addWidget(self.playbutton)
		self.playbutton.clicked.connect(self.play_pause)

		self.openbutton = QtWidgets.QPushButton("Open video")
		self.hbuttonbox.addWidget(self.openbutton)
		self.openbutton.clicked.connect(self.open_file)

		self.openbutton1 = QtWidgets.QPushButton("Open audio")
		self.hbuttonbox.addWidget(self.openbutton1)
		self.openbutton1.clicked.connect(self.open_audio)

		self.openbutton2 = QtWidgets.QPushButton("Open nose")
		self.hbuttonbox.addWidget(self.openbutton2)
		self.openbutton2.clicked.connect(self.open_nose)

		self.hbuttonbox.addStretch(1)
		self.layout.addWidget(self.positionSlider)#,3,0,1,-1)
		self.layout.addLayout(self.hbuttonbox)#,4,0,1,-1)

		self.player.setNotifyInterval(200)
		self.player.positionChanged.connect(self.updateUI)
		#self.player.positionChanged.connect(self.printTime)
		self.player.durationChanged.connect(self.setRange)
		self.player.stateChanged.connect(self.setButtonCaption)
		self.setLayout(self.layout)


	def open_nose(self):
		home = str(Path.home())
		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
		if not filename:
			return
		self.noseData = pandas.read_csv(filename).as_matrix()
		self.noseData[:,0] += 22
		self.noseData[:,1] -= 75
		self.noseData[:,2] += 22
		self.noseData[:,3] -= 75



	def open_audio(self):
		home = str(Path.home())
		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
		if not filename:
			return
		self.audio_data = pandas.read_csv(filename).as_matrix()
		self.audio_data = self.audio_data[:,0]
	# def OpenFile(self):
	#     """Open a media file in a MediaPlayer
	#     """
	#     home = str(Path.home())
	#     filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
	#     #print(filename)
	#         #filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", Path.home)
	#     if not filename:
	#         return
	#     # url = QtCore.QUrl.fromLocalFile(filename)
	#     # content = QM.QMediaContent(url)
	#     # #self.videoItem.setAspectRatioMode(1)
	#     # self.mediaplayer.set_agl(content)
	#     # create the media
	#     self.media = self.instance.media_new(str(filename))
	#     # # put the media in the media player
	#     self.mediaplayer.set_media(self.media)

	#     # # parse the metadata of the file
	#     self.media.parse()
	#     # # set the title of the track as window title
	#     self.setWindowTitle(self.media.get_meta(0))

	#     # # the media player has to be 'connected' to the QFrame
	#     # # (otherwise a video would be displayed in it's own window)
	#     # # this is platform specific!
	#     # if sys.platform == "linux2": # for Linux using the X Server
	#     #     self.mediaplayer.set_xwindow(self.videoframe.winId())
	#     # elif sys.platform == "win32": # for Windows
	#     #     self.mediaplayer.set_hwnd(self.videoframe.winId())
	#     # elif sys.platform == "darwin": # for MacOS
	#     self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
	#     #self.setRange()
	#     #self.mediaplayer.set_agl(self.videoframe.windId())
	#     #self.PlayPause()




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
	    for i in f:
	        t=i.strip().split()
	        self.ges_dict[int(t[1])]=self.gesture_dict[int(t[0])]
	    self.playbutton.setText("Play")

	def play_pause(self):
	    #self.videoItem.setSize(QtCore.QSizeF(self.view_width, self.view_height))
	    if self.player.state() == QM.QMediaPlayer.PlayingState:
	        self.play_state = False
	        self.player.pause()
	        # self.mediaplayer.pause()
	        # self.mediaplayer.set_position(self.positionSlider.value()/float(self.positionSlider.maximum()))
	    else:
	        self.play_state = True
	        #self.mediaplayer.set_position(self.positionSlider.value()/float(self.positionSlider.maximum()))
	        self.player.play()
	        #self.mediaplayer.play()

	def get_state(self):
		return QM.QMediaPlayer.PlayingState

	def setPosition(self, position):
	    self.positionSlider.setValue(position)
	    self.player.setPosition(position)
	    #self.mediaplayer.set_position(position / float(self.positionSlider.maximum()))

	def setRange(self, duration):
	    self.positionSlider.setRange(0, self.player.duration())

	def updateUI(self, position):
	    self.positionSlider.setValue(position)

	def display_gesture(self):
	    #print(self.positionSlider.value())

		indx = int(self.positionSlider.value()*30/1000)
		self.line.setLine(self.noseData[indx][0],self.noseData[indx][1],self.noseData[indx][2],self.noseData[indx][3])
		indx1 = int(self.positionSlider.value()/10)+100
		indx2 = np.arange(indx1-100,indx1+101)
		self.graph_view.clearPlots()
		self.graph_view.plot(np.arange(-100,101),self.audio_data[indx2], pen=pyqtgraph.mkPen(width=4,color='r'))
		self.graph_view.show()
		if self.time != int(self.positionSlider.value()/1000):
			self.time = int(self.positionSlider.value()/1000)
			if self.time in self.ges_dict.keys():
				self.three = self.two
				self.two = self.one
				self.one = self.ges_dict[self.time]+' '+'<br>'+str(self.time)+'<br><br>'
				self.label.setText("<h1><b><font size=8>"+self.one+"</font><font size=5>"+self.two+"</font><font size=3>"+self.three+"</font></b>")

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = videoWidget()
    w.show()
    sys.exit(app.exec_())

