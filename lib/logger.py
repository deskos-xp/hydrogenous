#! /usr/bin/env python3
from copy import copy

import sqlite3,pymysql
import json,gzip,base64

from PyQt5 import QtCore
import time,os,platform
from PyQt5.QtCore import pyqtSlot
import sys
for i in ['lib','lib_widget']:
    sys.path.append(i)
import mysql
import random

class logger(QtCore.QObject):
    sig=QtCore.pyqtSignal()

    def __init__(me,self,name,thread=None):
        super(me.__class__, me).__init__(thread)
        me.dbName="hydrogenousLogs_{}".format(platform.uname().node)
        me.tableName=time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime())
        me.data=[]
        me.name=name
        #self is parent
        me.parent=self
        #QtCore.QThread.__init__(me,self)
        me.timer=QtCore.QTimer()
        me.timer.timeout.connect(me.logData)
        me.setConnector()
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

    def setConnector(me):
        if me.parent.loggerSQLFormat.currentText() == 'MySQL':
            if me.connector != None:
                if me.connector.sql_type == 'SQLite3':
                    #me.connector.disconnect()
                    pass
            me.connector=mysql.handler(
                me.parent,
                host=me.parent.serverAddress.text(),
                port=me.parent.serverPort.value(),
                user=me.parent.serverUser.text(),
                db=me.parent.dbName.text(),
                password=me.parent.serverPassword.text()
                )
            me.formatString='%s'
        elif me.parent.loggerSQLFormat.currentText() == 'SQLite3':
            if me.connector != None:
                if me.connector.sql_type == 'MySQL':
                    me.connector.disconnect()
            me.formatString='?'


    def start(me):
        me.setConnector()
        me.timer.start(me.parent.main['interval'])
    
    table='logs'
    db='hydrogenous'
    formatString=''
    connector=None

    @pyqtSlot()
    def logData(me):
        self=me.parent
        rowName='{}_{}'.format(time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime()),random.randint(0,999999))
        tmp={rowName:me.parent.data_sig.copy()}
               
        me.sig.emit()
        jsonData=json.dumps(tmp)
        me.sig.emit()
        jsonData=jsonData.encode()
        me.sig.emit()
        gz=gzip.compress(jsonData)
        me.sig.emit()
        b64=base64.b64encode(gz).decode()
        me.sig.emit()

        #db hydrogenous
        #table logs
        sql='insert {1} (id,data) values({0},{0})'.format(me.formatString,me.table)
        me.data.append((sql,(rowName,b64)))
        me.sig.emit()
        print(len(me.data))
        
        if len(me.data) >= self.main['graphSize']:
            for i in me.data:
                print(i)
                if me.connector.cursor != None:
                    me.connector.cursor.execute(i[0],i[1])
            print(me.connector.db)
            if me.connector.db != None:
                me.connector.db.commit()
                print('log saved!')
            me.data=[]

        me.sig.emit()        
