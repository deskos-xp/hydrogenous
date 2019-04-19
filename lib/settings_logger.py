#! /usr/bin/env python3


class settings_logger:
    #settings tab controls for logger settings
    def __init__(me,self):
        me.checkBoxes(self)
        me.comboBoxes(self)
        #set this in etc/hydrogenous.json as "loggerFormat":"MySQL"
        me.settingsModeChange(self,'MySQL')
    def checkBoxes(me,self):
        self.useLogger.toggled.connect(lambda: me.enable_disable(self))

    def comboBoxes(me,self):
        self.loggerSQLFormat.currentIndexChanged.connect(lambda: me.settingsModeChange(self,self.loggerSQLFormat.currentText()))

    def settingsModeChange(me,self,formatName):
        if formatName == 'MySQL':
            self.sqlite3Browse.setEnabled(False)
            self.serverAddress.setEnabled(False)
            self.serverUser.setEnabled(False)

        if formatName == 'SQLite3':
            self.sqlite3Browse.setEnabled(True)
            self.serverAddress.setEnabled(False)
            self.serverUser.setEnabled(False)

    def enable_disable(me,self):
        self.main['useLogger']=self.useLogger.isChecked()
        self.main['controls'].saveSettings(self)
        self.logger_handler()
