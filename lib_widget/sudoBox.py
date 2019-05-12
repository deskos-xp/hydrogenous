# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/sudoBox.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_sudoBox(object):
    def setupUi(self, sudoBox):
        sudoBox.setObjectName("sudoBox")
        sudoBox.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(sudoBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.message = QtWidgets.QLabel(sudoBox)
        self.message.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 0, 0, 1, 1)
        self.passwd = QtWidgets.QLineEdit(sudoBox)
        self.passwd.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.passwd.setDragEnabled(True)
        self.passwd.setObjectName("passwd")
        self.gridLayout.addWidget(self.passwd, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(sudoBox)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(sudoBox)
        self.buttonBox.accepted.connect(sudoBox.accept)
        self.buttonBox.rejected.connect(sudoBox.reject)
        QtCore.QMetaObject.connectSlotsByName(sudoBox)

    def retranslateUi(self, sudoBox):
        _translate = QtCore.QCoreApplication.translate
        sudoBox.setWindowTitle(_translate("sudoBox", "Dialog"))
        self.message.setText(_translate("sudoBox", "You need administration rights to do this. You have {} attempts left."))


