import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
#import pyqtgraph as pg
import numpy as np
import math
import video_eye_tracking
import gesture_widget
import audio_widget
# pyqtgraph.examples.run()
# comment



try:
    _fromUtf8 = str
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def __init__(self):
        self.time = 0
        #self.eeg = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setGeometry(0, 0, 2560, 1600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.video_widget = video_eye_tracking.eyeTrackingWidget(self.centralWidget)
        self.video_widget.setGeometry(QtCore.QRect(5, 5, 954, 500))
        self.video_widget.setObjectName(_fromUtf8("eyeTrackingWidget"))

        self.gestureWidget = gesture_widget.gestureWidget(self.centralWidget)
        self.gestureWidget.setGeometry(QtCore.QRect(5, 500, 954, 200))
        self.gestureWidget.setObjectName(_fromUtf8("graphicsView"))

        # self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.centralWidget)
        # self.slider.setGeometry(QtCore.QRect(20,500,500,60))

        self.audioWidget = audio_widget.audioWidget(self.centralWidget)
        self.audioWidget.setGeometry(QtCore.QRect(5, 700, 954, 200))
        self.audioWidget.setObjectName(_fromUtf8("graphicsView"))

        self.video_widget.positionSlider.rangeChanged.connect(self.syncEggRange)
        self.video_widget.positionSlider.valueChanged.connect(self.SyncScroll)
        self.gestureWidget.positionSlider.valueChanged.connect(self.SyncScroll2)
        self.gestureWidget.positionSlider.sliderMoved.connect(self.updateScroll)
        self.audioWidget.positionSlider.valueChanged.connect(self.SyncScroll3)
        self.audioWidget.positionSlider.sliderMoved.connect(self.updateScroll)
        if self.gestureWidget.pause_signal == True:
        	video_eye_tracking.eyeTrackingWidget(self.video_widget)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def syncEggRange(self):
    	self.gestureWidget.positionSlider.setRange(0, self.video_widget.positionSlider.maximum())
    	self.audioWidget.positionSlider.setRange(0, self.video_widget.positionSlider.maximum())

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

    def SyncScroll(self,position):
    	self.audioWidget.positionSlider.setValue(position)
    	self.gestureWidget.positionSlider.setValue(position)
    	if self.gestureWidget.pause_signal == True:
    		self.video_widget.play_pause()
    		self.audioWidget.play_pause()

    def SyncScroll2(self,position):
    	self.audioWidget.positionSlider.setValue(position)
    	self.audioWidget.player.setPosition(position)
    	self.video_widget.positionSlider.setValue(position)
    	self.video_widget.player.setPosition(position)

    def updateScroll(self,position):
        self.video_widget.play_pause()
        self.audioWidget.play_pause()
        self.video_widget.positionSlider.setValue(position)
        self.video_widget.player.setPosition(position)

    def SyncScroll3(self,position):
    	if self.video_widget.play_state != self.audioWidget.play_state:
    		self.audioWidget.play_pause()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.resize(2560, 1600)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #ui.drawCurve(eeg)
    # ui.cal_content()
    # t = QtCore.QTimer()
    # t.timeout.connect(ui.updateData)
    # t.start(100)
    sys.exit(app.exec_())
