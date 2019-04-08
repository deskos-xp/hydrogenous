# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/battery_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_battery_widget(object):
    def setupUi(self, battery_widget):
        battery_widget.setObjectName("battery_widget")
        battery_widget.resize(400, 375)
        self.gridLayout_2 = QtWidgets.QGridLayout(battery_widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(battery_widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.time_left = QtWidgets.QLCDNumber(self.frame)
        self.time_left.setMinimumSize(QtCore.QSize(0, 300))
        self.time_left.setObjectName("time_left")
        self.gridLayout_3.addWidget(self.time_left, 0, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.plugged_in = QtWidgets.QLabel(self.frame)
        self.plugged_in.setMaximumSize(QtCore.QSize(50, 75))
        self.plugged_in.setObjectName("plugged_in")
        self.gridLayout_5.addWidget(self.plugged_in, 0, 0, 1, 1)
        self.battery_level = QtWidgets.QProgressBar(self.frame)
        self.battery_level.setProperty("value", 24)
        self.battery_level.setObjectName("battery_level")
        self.gridLayout_5.addWidget(self.battery_level, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(battery_widget)
        QtCore.QMetaObject.connectSlotsByName(battery_widget)

    def retranslateUi(self, battery_widget):
        _translate = QtCore.QCoreApplication.translate
        battery_widget.setWindowTitle(_translate("battery_widget", "battery_widget"))
        self.plugged_in.setText(_translate("battery_widget", "Plugged_IN"))


