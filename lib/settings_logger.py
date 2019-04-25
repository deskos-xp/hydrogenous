#! /usr/bin/env python3

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore,QtWidgets
import os
class settings_logger(QtCore.QObject):
    #settings tab controls for logger settings
    def __init__(me,self):
        super(me.__class__,me).__init__()
        me.parent=self
        me.checkBoxes(self)
        me.comboBoxes(self)
        me.buttons(self)
        me.lineEdits(self)
        #set this in etc/hydrogenous.json as "loggerFormat":"MySQL"
        me.settingsModeChange()
        
    def checkBoxes(me,self):
        self.useLogger.toggled.connect(lambda: me.enable_disable(self))

    def comboBoxes(me,self):
        self.loggerSQLFormat.currentIndexChanged.connect(me.settingsModeChange)

    def buttons(me,self):
        if 'logger_obj' in self.main.keys():
            self.connect.clicked.connect(self.main['logger_obj'].setConnector)
            self.sqlite3Browse.clicked.connect(me.getSaveFileName)
    
    @QtCore.pyqtSlot(bool)
    def getSaveFileName(me,clicked):
        if me.parent.dbName.text() == '' or not os.path.exists(me.parent.dbName.text()):
            default_dir=os.environ['HOME']
        else:
            default_dir=me.parent.dbName.text()
        print(clicked)
        fname=QtWidgets.QFileDialog.getSaveFileName(me.parent,caption='Save SQLite3 DB',directory=default_dir,filter='SQLite3 DB (*.db)')
        if fname != ('',''):
            me.parent.dbName.setText(fname[0])
            me.saveInternal()

    def lineEdits(me,self):
        #print('le setup')
        self.dbName.textChanged.connect(me.saveInternal)
        self.dbTable.textChanged.connect(me.saveInternal)
        self.serverUser.textChanged.connect(me.saveInternal)
        self.serverAddress.textChanged.connect(me.saveInternal)
        self.serverPort.valueChanged.connect(me.saveInternal)

    @pyqtSlot()
    def saveInternal(me):
        self=me.parent
        print('settings changing...')
        self.main['format']=self.loggerSQLFormat.currentText()
        self.main['dbName']=self.dbName.text()
        self.main['dbTable']=self.dbTable.text()
        if self.loggerSQLFormat.currentText() == 'MySQL':
            self.main['serverUser']=self.serverUser.text()
            self.main['serverAddress']=self.serverAddress.text()
            self.main['serverPort']=self.serverPort.value()
        self.main['controls'].saveSettings(self)
    
    @pyqtSlot()
    def settingsModeChange(me):
        self=me.parent
        self.main['format']=self.loggerSQLFormat.currentText()
        if self.main['format'] == 'MySQL':
            self.sqlite3Browse.setEnabled(False)
            self.serverAddress.setEnabled(True)
            self.serverUser.setEnabled(True)
            self.serverPassword.setEnabled(True)
            self.serverPort.setEnabled(True)
            for ichar in '|-*/<>=,~!^();.':
                if ichar in self.dbName.text():
                    self.statusBar().showMessage('Invalid DB Name "{}"'.format(self.dbName.text()))
                    self.dbName.setText('hydrogenous')
                if ichar in self.dbTable.text():
                    self.statusBar().showMessage('Invalid DB Table "{}"'.format(self.dbTable.text()))
                    self.dbName.setText('logs')
        elif self.main['format'] == 'SQLite3':
            self.sqlite3Browse.setEnabled(True)
            self.serverAddress.setEnabled(False)
            self.serverUser.setEnabled(False)
            self.serverPassword.setEnabled(False)
            self.serverPort.setEnabled(False)
        me.saveInternal()
        print('settings changing',self.main['format'])
    def enable_disable(me,self):
        self.main['useLogger']=self.useLogger.isChecked()
        self.main['controls'].saveSettings(self)
        self.logger_handler()
