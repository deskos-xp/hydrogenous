#! /usr/bin/env python3

import sqlite3,pymysql
from PyQt5 import QtCore
import time,os,platform
class logger(QtCore.QThread):
    sig=QtCore.pyqtSignal()

    def __init__(me,self,name):

        me.dbName="hydrogenousLogs_{}".format(platform.uname().node)
        me.tableName=time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime())

        me.name=name
        #self is parent
        me.parent=self
        QtCore.QThread.__init__(me,self)
        me.timer=QtCore.QTimer()
        me.timer.timeout.connect(lambda: me.logData(self))
        me.timer.moveToThread(me)

    def run(me):
        me.timer.start(me.parent.main['interval'])
        me.exec_()

    def logData(me,self):
        rowName=time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime())
        print(rowName)
        me.sig.emit()        
