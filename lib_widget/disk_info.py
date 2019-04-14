# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/disk_info.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_disk_info(object):
    def setupUi(self, disk_info):
        disk_info.setObjectName("disk_info")
        disk_info.resize(785, 536)
        self.gridLayout_2 = QtWidgets.QGridLayout(disk_info)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.diskTable = QtWidgets.QTableWidget(disk_info)
        self.diskTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.diskTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.diskTable.setDragEnabled(True)
        self.diskTable.setAlternatingRowColors(True)
        self.diskTable.setObjectName("diskTable")
        self.diskTable.setColumnCount(8)
        self.diskTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.diskTable.setHorizontalHeaderItem(7, item)
        self.diskTable.horizontalHeader().setCascadingSectionResizes(True)
        self.diskTable.horizontalHeader().setStretchLastSection(True)
        self.diskTable.verticalHeader().setCascadingSectionResizes(True)
        self.diskTable.verticalHeader().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.diskTable, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(disk_info)
        QtCore.QMetaObject.connectSlotsByName(disk_info)

    def retranslateUi(self, disk_info):
        _translate = QtCore.QCoreApplication.translate
        disk_info.setWindowTitle(_translate("disk_info", "Form"))
        self.diskTable.setSortingEnabled(True)
        item = self.diskTable.horizontalHeaderItem(0)
        item.setText(_translate("disk_info", "device"))
        item = self.diskTable.horizontalHeaderItem(1)
        item.setText(_translate("disk_info", "mountpoint"))
        item = self.diskTable.horizontalHeaderItem(2)
        item.setText(_translate("disk_info", "fstype"))
        item = self.diskTable.horizontalHeaderItem(3)
        item.setText(_translate("disk_info", "opts"))
        item = self.diskTable.horizontalHeaderItem(4)
        item.setText(_translate("disk_info", "size"))
        item = self.diskTable.horizontalHeaderItem(5)
        item.setText(_translate("disk_info", "used"))
        item = self.diskTable.horizontalHeaderItem(6)
        item.setText(_translate("disk_info", "free"))
        item = self.diskTable.horizontalHeaderItem(7)
        item.setText(_translate("disk_info", "percent"))


