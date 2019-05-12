# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/renice.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_renice(object):
    def setupUi(self, renice):
        renice.setObjectName("renice")
        renice.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(renice)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pid = QtWidgets.QSpinBox(renice)
        self.pid.setMinimum(1)
        self.pid.setMaximum(999999999)
        self.pid.setObjectName("pid")
        self.gridLayout.addWidget(self.pid, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(renice)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(renice)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.nice = QtWidgets.QSpinBox(renice)
        self.nice.setMinimum(-19)
        self.nice.setMaximum(20)
        self.nice.setObjectName("nice")
        self.gridLayout.addWidget(self.nice, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.renice_button = QtWidgets.QPushButton(renice)
        self.renice_button.setObjectName("renice_button")
        self.gridLayout_2.addWidget(self.renice_button, 2, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(renice)
        self.name.setDragEnabled(True)
        self.name.setReadOnly(True)
        self.name.setObjectName("name")
        self.gridLayout_2.addWidget(self.name, 0, 0, 1, 1)

        self.retranslateUi(renice)
        QtCore.QMetaObject.connectSlotsByName(renice)

    def retranslateUi(self, renice):
        _translate = QtCore.QCoreApplication.translate
        renice.setWindowTitle(_translate("renice", "Form"))
        self.pid.setToolTip(_translate("renice", "Process ID"))
        self.label.setText(_translate("renice", "PID"))
        self.label_2.setText(_translate("renice", "Nice"))
        self.nice.setToolTip(_translate("renice", "Set the Nice/Priority Value"))
        self.renice_button.setToolTip(_translate("renice", "Renice!"))
        self.renice_button.setText(_translate("renice", "Re-Nice"))


