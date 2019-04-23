#! /usr/bin/env python3

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore,QtWidgets
class settings_logger(QtCore.QObject):
    #settings tab controls for logger settings
    def __init__(me,self):
        me.parent=self
        me.checkBoxes(self)
        me.comboBoxes(self)
        me.buttons(self)
        me.lineEdits(self)
        #set this in etc/hydrogenous.json as "loggerFormat":"MySQL"
        me.settingsModeChange(self,'MySQL')
        
    def checkBoxes(me,self):
        self.useLogger.toggled.connect(lambda: me.enable_disable(self))

    def comboBoxes(me,self):
        self.loggerSQLFormat.currentIndexChanged.connect(lambda: me.settingsModeChange(self,self.loggerSQLFormat.currentText()))

    def buttons(me,self):
        if 'logger_obj' in self.main.keys():
            self.connect.clicked.connect(self.main['logger_obj'].setConnector)

    def lineEdits(me,self):
        #print('le setup')
        self.dbName.textChanged.connect(lambda x: me.saveInternal(self,x))
        self.dbTable.textChanged.connect(lambda x: me.saveInternal(self, x))
        self.serverUser.textChanged.connect(lambda x: me.saveInternal(self,x))
        self.serverAddress.textChanged.connect(lambda x:me.saveInternal(self,x))
        self.serverPort.valueChanged.connect(lambda: me.saveInternal(self,x))

    #@pyqtSlot()
    def saveInternal(me,self,val):
        print('settings changing...')
        self.main['dbName']=self.dbName.text()
        self.main['dbTable']=self.dbTable.text()
        self.main['serverUser']=self.serverUser.text()
        self.main['serverAddress']=self.serverAddress.text()
        self.main['serverPort']=self.serverPort.value()
        self.main['controls'].saveSettings(self)

    def settingsModeChange(me,self,formatName):
        if formatName == 'MySQL':
            self.sqlite3Browse.setEnabled(False)
            self.serverAddress.setEnabled(True)
            self.serverUser.setEnabled(True)
            self.serverPassword.setEnabled(True)
            self.serverPort.setEnabled(True)
        elif formatName == 'SQLite3':
            self.sqlite3Browse.setEnabled(True)
            self.serverAddress.setEnabled(False)
            self.serverUser.setEnabled(False)
            self.serverPassword.setEnabled(False)
            self.serverPort.setEnabled(False)

    def enable_disable(me,self):
        self.main['useLogger']=self.useLogger.isChecked()
        self.main['controls'].saveSettings(self)
        self.logger_handler()
