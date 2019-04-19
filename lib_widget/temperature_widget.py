# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/temperature_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_temperature(object):
    def setupUi(self, temperature):
        temperature.setObjectName("temperature")
        temperature.resize(560, 110)
        temperature.setMinimumSize(QtCore.QSize(560, 110))
        self.gridLayout_2 = QtWidgets.QGridLayout(temperature)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(temperature)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.high = QtWidgets.QLCDNumber(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.high.sizePolicy().hasHeightForWidth())
        self.high.setSizePolicy(sizePolicy)
        self.high.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.high.setLineWidth(0)
        self.high.setMidLineWidth(0)
        self.high.setSmallDecimalPoint(True)
        self.high.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.high.setObjectName("high")
        self.gridLayout_5.addWidget(self.high, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 1, 3, 1, 1)
        self.frame_3 = QtWidgets.QFrame(temperature)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.current = QtWidgets.QLCDNumber(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current.sizePolicy().hasHeightForWidth())
        self.current.setSizePolicy(sizePolicy)
        self.current.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.current.setLineWidth(0)
        self.current.setMidLineWidth(0)
        self.current.setSmallDecimalPoint(True)
        self.current.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.current.setObjectName("current")
        self.gridLayout_3.addWidget(self.current, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 2, 1, 1)
        self.frame_2 = QtWidgets.QFrame(temperature)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.critical = QtWidgets.QLCDNumber(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.critical.sizePolicy().hasHeightForWidth())
        self.critical.setSizePolicy(sizePolicy)
        self.critical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.critical.setLineWidth(0)
        self.critical.setMidLineWidth(0)
        self.critical.setSmallDecimalPoint(True)
        self.critical.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.critical.setObjectName("critical")
        self.gridLayout_7.addWidget(self.critical, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 4, 1, 1)
        self.frame_4 = QtWidgets.QFrame(temperature)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label = QtWidgets.QLineEdit(self.frame_4)
        self.label.setDragEnabled(True)
        self.label.setReadOnly(True)
        self.label.setObjectName("label")
        self.gridLayout_9.addWidget(self.label, 1, 0, 1, 1)
        self.hardware = QtWidgets.QLineEdit(self.frame_4)
        self.hardware.setDragEnabled(True)
        self.hardware.setReadOnly(True)
        self.hardware.setObjectName("hardware")
        self.gridLayout_9.addWidget(self.hardware, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(temperature)
        QtCore.QMetaObject.connectSlotsByName(temperature)

    def retranslateUi(self, temperature):
        _translate = QtCore.QCoreApplication.translate
        temperature.setWindowTitle(_translate("temperature", "Form"))
        self.label_3.setText(_translate("temperature", "High"))
        self.label_2.setText(_translate("temperature", "Current"))
        self.label_4.setText(_translate("temperature", "Critical"))


