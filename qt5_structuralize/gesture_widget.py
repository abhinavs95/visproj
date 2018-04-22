import sys
import os
from pathlib import Path
from PyQt5 import QtCore, Qt
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
        self.gesture_prev = -1
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
        # self.positionSlider.setMinimum(1)
        # self.positionSlider.setMaximum(9)
        # self.positionSlider.setTickInterval(1)
        # self.positionSlider.setSingleStep(1) # arrow-key step-size
        # self.positionSlider.setPageStep(1) # mouse-wheel/page-key step-size
        # self.positionSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)

        #self.positionSlider.valueChanged.connect(self.update_eeg_graph)

        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.openbutton = QtWidgets.QPushButton("Open gesture")
        self.hbuttonbox.addWidget(self.openbutton)
        self.openbutton.clicked.connect(self.open_file)
        
        self.prevbutton = QtWidgets.QPushButton("Prev")
        self.hbuttonbox.addWidget(self.prevbutton)
        self.prevbutton.clicked.connect(self.get_prev)

        self.nextbutton = QtWidgets.QPushButton("Next")
        self.hbuttonbox.addWidget(self.nextbutton)
        self.nextbutton.clicked.connect(self.get_next)
        # self.comboLabel = QtWidgets.QLabel("Select Channels:")
        # self.combobox = QtWidgets.QComboBox(self)
        # self.comboboxDelegate = utility.SubclassOfQStyledItemDelegate()
        # self.combobox.setItemDelegate(self.comboboxDelegate)
        # self.combobox.setSizeAdjustPolicy(0)
        # self.hbuttonbox.addWidget(self.comboLabel)
        # self.hbuttonbox.addWidget(self.combobox)

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
        #print(int(self.time/1000))
        self.pause_signal = False
        if int(self.time/1000) == self.gesture_data[self.gesture_pos,2]:
            self.pause_signal = True
            label = QtWidgets.QLabel("<h1><b><font size=5>"+str(self.gesture_data[self.gesture_pos,3])+"</font></b>")
            self.graph_layout.addWidget(label,self.gesture_pos+1,0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            label = QtWidgets.QLabel("<h1><b><font size=5>"+self.gesture_dict[self.gesture_data[self.gesture_pos][1]]+"</font></b>")
            self.graph_layout.addWidget(label,self.gesture_pos+1,1,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            label = QtWidgets.QLabel("<h1><b><font size=5>"+str(self.gesture_data[self.gesture_pos,4:])+"</font></b>")
            self.graph_layout.addWidget(label,self.gesture_pos+1,2,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            self.gesture_prev = self.gesture_pos
            self.gesture_pos = self.gesture_pos+1
        else:
            if int(self.time/1000) > self.gesture_data[self.gesture_pos,2]:
                self.pause_signal = True
                label = QtWidgets.QLabel("<h1><b><font size=5>"+str(self.gesture_data[self.gesture_pos,3])+"</font></b>")
                self.graph_layout.addWidget(label,self.gesture_pos+1,0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                label = QtWidgets.QLabel("<h1><b><font size=5>"+self.gesture_dict[self.gesture_data[self.gesture_pos][1]]+"</font></b>")
                self.graph_layout.addWidget(label,self.gesture_pos+1,1,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                label = QtWidgets.QLabel("<h1><b><font size=5>"+str(self.gesture_data[self.gesture_pos,4:])+"</font></b>")
                self.graph_layout.addWidget(label,self.gesture_pos+1,2,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
                self.gesture_prev = self.gesture_pos
                self.gesture_pos = self.gesture_pos+1


    def open_file(self, filename=None):
        home = str(Path.home())
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Gesture", home)
        if not filename:
            return
        self.gesture_data = pandas.read_csv(filename).as_matrix()
        self.gesture_data[:,2] = (self.gesture_data[:,2]/30).astype('int64')
        # for i in range(len(self.gesture_data)):
        #     self.gesture_data[i]=self.gesture_data[i].split(' ')
        #     self.gesture_data[i][0] = int(self.gesture_data[i][0])
        #     self.gesture_data[i][1] = int(int(self.gesture_data[i][1])/30)
        self.gesture_len = self.gesture_data.shape[0]
        label = QtWidgets.QLabel("<h1><b><u><font size=6>"+'Question'+"</font></u></b>")
        self.graph_layout.addWidget(label,0,0,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        label = QtWidgets.QLabel("<h1><b><u><font size=6>"+'Gesture'+"</font></u></b>")
        self.graph_layout.addWidget(label,0,1,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        label = QtWidgets.QLabel("<h1><b><u><font size=6>"+'Scores'+"</font></u></b>")
        self.graph_layout.addWidget(label,0,2,QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def get_next(self):
        try:
            self.gesture_prev += 1
            self.positionSlider.setValue(self.gesture_data[self.gesture_prev,2]*1000 - 100)
        except:
            self.gesture_prev -=1

    def get_prev(self):
        if self.gesture_prev == -1:
            self.positionSlider.setValue(0)
        else:
            self.positionSlider.setValue(self.gesture_data[self.gesture_prev,2]*1000 - 100) 
            self.gesture_prev -= 1       


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = gestureWidget()
    w.show()
    sys.exit(app.exec_())
