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
        self.view_height= 400 ##QGraphcsView
        self.play_state = False
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
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)

        self.openbutton = QtWidgets.QPushButton("Open video")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)
        # self.openbutton2 = QtWidgets.QPushButton("Open EYE")
        # self.hbuttonbox.addWidget(self.openbutton2)
        # self.openbutton2.clicked.connect(self.open_eye)

        # self.comboLabel = QtWidgets.QLabel("Select objects:")
        # self.combobox = QtWidgets.QComboBox(self)
        # self.comboboxDelegate = utility.SubclassOfQStyledItemDelegate()
        # self.combobox.setItemDelegate(self.comboboxDelegate)
        # self.combobox.setSizeAdjustPolicy(0)
        # self.hbuttonbox.addWidget(self.comboLabel)
        # self.hbuttonbox.addWidget(self.combobox)


        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.player.setNotifyInterval(100)
        self.player.positionChanged.connect(self.updateUI)
        #self.player.positionChanged.connect(self.printTime)
        self.player.durationChanged.connect(self.setRange)
        self.player.stateChanged.connect(self.setButtonCaption)
        self.setLayout(self.layout)

    

    # def printTime(self):
    #     return
    #     #print(self.player.position())

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
        self.playbutton.setText("Play")

    # def open_eye(self):
    #     home = str(Path.home())
    #     filenames,_ = QtWidgets.QFileDialog.getOpenFileNames(self, "Open EYE", home)
    #     print("%s, %s" % (filenames, len(filenames)))
    #     if not filenames:
    #         return
    #     object_list=[]
    #     self.audience_eye_tracking_dic = {}
    #     self.eye_track_dic = {}
    #     for filename in filenames:
    #         object = os.path.split(filename)[-1].split('_')[0]
    #         self.create_eye_tracking_reference_dict(pandas.read_excel(str(filename)),object)
    #         object_list.append(object)
    #     self.addSelectArea(object_list)

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

    # def updateEyeTracking(self, position):
    #     if len(self.eye_track_dic.keys()) == 0:# or self.player.state() != 2:
    #         return
    #     self.draw_eye_tracking()

    # def addSelectArea(self, objects):
    #     self.player.pause()
    #     for k in self.elements.keys():
    #         self.removeElement(self.elements[k],k)
    #     self.elements={}
    #     self.model = QtGui.QStandardItemModel(len(objects) + 1, 1)  # 5 rows, 2 col
    #     firstItem = QtGui.QStandardItem("---- Select area(s) ----")
    #     firstItem.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
    #     firstItem.setSelectable(False)
    #     self.model.setItem(0, 0, firstItem)
    #     num = 0
    #     for obj in objects:
    #         num += 1
    #         item = QtGui.QStandardItem(obj)
    #         item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
    #         itemColor = QtGui.QColor(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    #         item.setBackground(itemColor)
    #         if num <= 2:
    #             item.setData(QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
    #             self.elements[item.text()] = {'dot': None, 'lines': [], 'color':itemColor}
    #         else:
    #             item.setData(QtCore.Qt.Unchecked,QtCore.Qt.CheckStateRole)
    #         self.model.setItem(num, 0, item)
    #     self.model.itemChanged.connect(self.update_objects)
    #     self.combobox.setModel(self.model)

    # def removeElement(self, element, name):
    #     for line in element['lines']:
    #         self.scene.removeItem(line)
    #         del line
    #     self.scene.removeItem(element['dot'])
    #     del element['dot']
    #     # del element['color']
    #     self.elements.pop(name)

    # def update_objects(self, item):
    #     if item.checkState() == 0:
    #         self.removeElement(self.elements[item.text()], item.text())
    #     else:
    #         self.elements[item.text()]={'dot':None,'lines':[], 'color':item.background().color()}

    # def draw_dot_line(self, v, obj):
    #     pos = v['pos']
    #     rad = v['rad']
    #     if self.elements[obj]['dot'] is not None:
    #         self.elements[obj]['dot'].setRect(QtCore.QRectF(0, 0, rad, rad))
    #     else:
    #         self.elements[obj]['dot'] = self.scene.addEllipse(QtCore.QRectF(0, 0, rad, rad),
    #                          QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(self.elements[obj]['color']))
    #     self.elements[obj]['dot'].setPos(QtCore.QPoint(pos[0] - rad / 2, pos[1] - rad / 2))
    #     j = 0
    #     for i in range(len(v['lines'])):
    #         j = i
    #         if i >= len(self.elements[obj]['lines']):
    #             self.elements[obj]['lines'].append(self.scene.addLine(QtCore.QLineF(v['lines'][i][0][0], v['lines'][i][0][1],
    #                                                         v['lines'][i][1][0], v['lines'][i][1][1]),
    #                                                  QtGui.QPen(self.elements[obj]['color'])))
    #         else:
    #             self.elements[obj]['lines'][i].setLine(QtCore.QLineF(v['lines'][i][0][0], v['lines'][i][0][1],
    #                                          v['lines'][i][1][0], v['lines'][i][1][1]))
    #     if len(self.elements[obj]['lines']) > j:
    #         for line in self.elements[obj]['lines'][j+1:-1]:
    #             self.scene.removeItem(line)
    #             del line

    # def resolution_transfer(self, x, y, duration):
    #     return [x / self.eye_tracking_width * self.view_width,\
    #            y / self.eye_tracking_height * self.view_height, \
    #            3 + duration / 20.0]

    # def create_eye_tracking_reference_dict(self, excel, object):
    #     self.audience_eye_tracking_dic[object] = {'pos': [], 'rad':0,'lines': []}
    #     self.eye_track_window = 1000 / self.eye_track_frame_rate
    #     self.eye_track_dic[object] = []
    #     last_one = int(excel['CURRENT_FIX_START'][521] / self.eye_track_window)
    #     head = 0
    #     for i in range(last_one):
    #         start_time = i * self.eye_track_window
    #         updated_flag = False
    #         while head < len(excel['CURRENT_FIX_START'].index):
    #             if excel['CURRENT_FIX_START'][head] > start_time:
    #                 break
    #             if excel['CURRENT_FIX_START'][head] <= start_time and start_time <= excel['CURRENT_FIX_END'][head]:
    #                 self.eye_track_dic[object].append(self.resolution_transfer(excel['CURRENT_FIX_X'][head], excel['CURRENT_FIX_Y'][head], excel['CURRENT_FIX_DURATION'][head]))
    #                 updated_flag = True
    #                 break
    #             head += 1
    #         if not updated_flag:
    #             if len(self.eye_track_dic[object]) > 0:
    #                 self.eye_track_dic[object].append(self.eye_track_dic[object][-1])
    #             else:
    #                 self.eye_track_dic[object].append([])
    #                 # print "no positions!"
    #     # print self.eye_track_dic

    # def draw_eye_tracking(self, clean_flag=False):
    #     media_time = self.player.position()
    #     for k in self.elements:
    #         v = self.audience_eye_tracking_dic[k]
    #         eye_tracking_window_index = int(media_time / self.eye_track_window)
    #         if eye_tracking_window_index >= len(self.eye_track_dic[k]) \
    #                 or len(self.eye_track_dic[k][eye_tracking_window_index]) < 3:
    #             continue
    #         v['pos'] = self.eye_track_dic[k][eye_tracking_window_index][0:2]
    #         v['rad'] = self.eye_track_dic[k][eye_tracking_window_index][2]
    #         v['lines'] = []
    #         if len(v['pos']) == 2:
    #             for line_num in range(int(self.trial_lapse / self.eye_track_window)):
    #                 if eye_tracking_window_index - line_num - 1 >= 0 and len(
    #                         self.eye_track_dic[k][eye_tracking_window_index - line_num - 1]) == 3:
    #                     v['lines'].append([self.eye_track_dic[k][eye_tracking_window_index - line_num - 1],
    #                                        self.eye_track_dic[k][eye_tracking_window_index - line_num]])
    #             self.draw_dot_line(v, k)

                #####################       eye tracking        #####################

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    w = eyeTrackingWidget()
    w.show()
    sys.exit(app.exec_())
