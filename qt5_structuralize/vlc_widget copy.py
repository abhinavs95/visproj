__author__ = "Hector Yong Hyun Cho"
__version__ = "0.0.1"
# comment


import sys
from pathlib import Path
import vlc
from PyQt5 import QtGui, QtCore, QtWidgets
import PyQt5.QtMultimedia as QM

class VLCPlayerWidget(QtWidgets.QWidget):
    def __init__(self):
        super(VLCPlayerWidget, self).__init__()
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False


    def createUI(self):

        self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setToolTip("Position")
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        #self.positionSlider.setMaximum(1000)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        # self.playbutton = QtWidgets.QPushButton("Play")
        # self.hbuttonbox.addWidget(self.playbutton)
        # self.playbutton.clicked.connect(self.PlayPause)

        # self.stopbutton = QtWidgets.QPushButton("Stop")
        # self.hbuttonbox.addWidget(self.stopbutton)
        # self.stopbutton.clicked.connect(self.Stop)

        self.openbutton = QtWidgets.QPushButton("Open audio")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.OpenFile)


        self.hbuttonbox.addStretch(1)
        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeSlider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeSlider)
        self.volumeSlider.sliderMoved.connect(self.setVolume)


        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionSlider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.setLayout(self.vboxlayout)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)


    def OpenFile(self):
        """Open a media file in a MediaPlayer
        """
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", home)
        #print(filename)
            #filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", Path.home)
        if not filename:
            return
        # url = QtCore.QUrl.fromLocalFile(filename)
        # content = QM.QMediaContent(url)
        # #self.videoItem.setAspectRatioMode(1)
        # self.mediaplayer.set_agl(content)
        # create the media
        self.media = self.instance.media_new(str(filename))
        # # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # # parse the metadata of the file
        self.media.parse()
        # # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # # the media player has to be 'connected' to the QFrame
        # # (otherwise a video would be displayed in it's own window)
        # # this is platform specific!
        # if sys.platform == "linux2": # for Linux using the X Server
        #     self.mediaplayer.set_xwindow(self.videoframe.winId())
        # elif sys.platform == "win32": # for Windows
        #     self.mediaplayer.set_hwnd(self.videoframe.winId())
        # elif sys.platform == "darwin": # for MacOS
        self.mediaplayer.set_nsobject(int(self.videoframe.winId()))
        #self.mediaplayer.set_agl(self.videoframe.windId())
        #self.PlayPause()


    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            #self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        #self.playbutton.setText("Play")

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / float(self.positionSlider.maximum()))
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionSlider.setValue(self.mediaplayer.get_position() * self.positionSlider.maximum())

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

    def getPosition(self):
        return self.mediaplayer.get_position()

    def setRange(self, duration):
        self.positionSlider.setRange(0, self.player.duration())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = VLCPlayerWidget()
    player.show()
    player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
