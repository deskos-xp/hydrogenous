# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/gateways_info.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gateway_info(object):
    def setupUi(self, gateway_info):
        gateway_info.setObjectName("gateway_info")
        gateway_info.resize(532, 336)
        self.gridLayout_2 = QtWidgets.QGridLayout(gateway_info)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gateways = QtWidgets.QGroupBox(gateway_info)
        self.gateways.setObjectName("gateways")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gateways)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_3 = QtWidgets.QFrame(self.gateways)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_3)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 250))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(True)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget.verticalHeader().setMinimumSectionSize(32)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.gateways, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(gateway_info)
        QtCore.QMetaObject.connectSlotsByName(gateway_info)

    def retranslateUi(self, gateway_info):
        _translate = QtCore.QCoreApplication.translate
        gateway_info.setWindowTitle(_translate("gateway_info", "Form"))
        self.gateways.setTitle(_translate("gateway_info", "Gateways"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("gateway_info", "family"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("gateway_info", "address"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("gateway_info", "interface"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("gateway_info", "default"))


