import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import utility
import numpy as np
import math
import pandas
#import pyqtgraph
import sip

class gestureWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        self.gesture_data = None
        self.gesture_pos = 0
        self.gesture_len = 0
        self.gesture_dict = {0:'metaphoric',1:'beats',2:'deictics',3:'iconic'}
        self.graph_width = 910
        self.graph_height = 200
        self.time = 0
        self.layout = QtWidgets.QVBoxLayout(self)
        self.createUI()



    def createUI(self):

        self.time = 0
        self.pause_signal = False
        # video position slider
        self.graph_widget = QtWidgets.QWidget()
        # Layout of Container Widget
        self.graph_layout = QtWidgets.QGridLayout()
        self.graph_widget.setLayout(self.graph_layout)

        self.scrollarea = QtWidgets.QScrollArea()
        self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollarea.setWidgetResizable(True)
        # self.scrollarea.setGeometry(10, 0, self.graph_width, self.graph_height * 3)
        self.scrollarea.setWidget(self.graph_widget)

        self.positionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.positionSlider.setStyleSheet("QSlider::groove:horizontal {background-color:grey;}"
                                "QSlider::handle:horizontal {background-color:black; height:8px; width: 8px;}")
        #self.positionSlider.valueChanged.connect(self.update_eeg_graph)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.openbutton = QtWidgets.QPushButton("Open gesture")
        # self.comboLabel = QtWidgets.QLabel("Select Channels:")
        # self.combobox = QtWidgets.QComboBox(self)
        # self.comboboxDelegate = utility.SubclassOfQStyledItemDelegate()
        # self.combobox.setItemDelegate(self.comboboxDelegate)
        # self.combobox.setSizeAdjustPolicy(0)
        self.hbuttonbox.addWidget(self.openbutton)
        # self.hbuttonbox.addWidget(self.comboLabel)
        # self.hbuttonbox.addWidget(self.combobox)
        self.openbutton.clicked.connect(self.open_file)

        self.hbuttonbox.addStretch(1)
        self.layout.addWidget(self.scrollarea)
        self.layout.addWidget(self.positionSlider)
        self.layout.addLayout(self.hbuttonbox)

        self.positionSlider.valueChanged.connect(self.setGestureType)
        self.setLayout(self.layout)



    def setGestureType(self):
        if self.gesture_pos == self.gesture_len:
            self.pause_signal = False
            return
        self.time = self.positionSlider.value()
        self.pause_signal = False
        if int(self.time/1000) == self.gesture_data[self.gesture_pos][1]:
            self.pause_signal = True
            label = QtWidgets.QLabel(self.gesture_dict[self.gesture_data[self.gesture_pos][0]])
            self.graph_layout.addWidget(label)
            self.gesture_pos = self.gesture_pos+1

    def open_file(self, filename=None):
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Gesture", home)
        if not filename:
            return
        self.gesture_data = open(filename).read().splitlines()
        for i in range(len(self.gesture_data)):
            self.gesture_data[i]=self.gesture_data[i].split(' ')
            self.gesture_data[i][0] = int(self.gesture_data[i][0])
            self.gesture_data[i][1] = int(int(self.gesture_data[i][1])/30)
        self.gesture_len = len(self.gesture_data)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = gestureWidget()
    w.show()
    sys.exit(app.exec_())
