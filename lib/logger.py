#! /usr/bin/env python3

import sqlite3,pymysql
from PyQt5 import QtCore
import time,os,platform
from PyQt5.QtCore import pyqtSlot
class logger(QtCore.QObject):
    sig=QtCore.pyqtSignal()

    def __init__(me,self,name,thread=None):
        super(me.__class__, me).__init__(thread)
        me.dbName="hydrogenousLogs_{}".format(platform.uname().node)
        me.tableName=time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime())

        me.name=name
        #self is parent
        me.parent=self
        #QtCore.QThread.__init__(me,self)
        me.timer=QtCore.QTimer()
        me.timer.timeout.connect(me.logData)
        me.run()
        #me.timer.moveToThread(me)

    def run(me):
        me.timer.start(me.parent.main['interval'])
        me.sig.emit()
        #me.exec_()
    
    def quit(me):
        me.timer.stop()
        me.sig.emit()

    def wait(me):
        pass

    def start(me):
        me.timer.start(me.parent.main['interval'])

    @pyqtSlot()
    def logData(me):
        self=me.parent
        rowName=time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime())
        print(rowName)
        me.sig.emit()        
