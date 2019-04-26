#! /usr/bin/env python3
from copy import copy

import sqlite3,pymysql
import json,gzip,base64
from datetime import datetime

from PyQt5 import QtCore
import time,os,platform
from PyQt5.QtCore import pyqtSlot
import sys
for i in ['lib','lib_widget']:
    sys.path.append(i)
import mysql,sqlite
import random
import gc
class logger(QtCore.QObject):
    sig=QtCore.pyqtSignal()

    def __init__(me,self,name,thread=None):
        super(me.__class__, me).__init__(thread)
        me.dbName=""
        me.tableName=''
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
        if me.connector != None:
            if me.connector.db != None:
                me.connector.db.close()
        me.sig.emit()

    def wait(me):
        pass

    def setConnector(me):
        me.connector_thread=QtCore.QThread()
        msg='log format is "{}"'.format(me.parent.loggerSQLFormat.currentText())
        if me.parent.loggerSQLFormat.currentText() == 'MySQL':
            if me.connector != None:
                if me.connector.sql_type == 'SQLite3':
                    if me.connector != None:
                        me.connector.disconnect()
    
                me.connector=mysql.handler(
                me.parent,
                host=me.parent.serverAddress.text(),
                port=me.parent.serverPort.value(),
                user=me.parent.serverUser.text(),
                db=me.parent.dbName.text(),
                password=me.parent.serverPassword.text()
                )
            me.connector.moveToThread(me.connector_thread)
            me.formatString='%s'
        elif me.parent.loggerSQLFormat.currentText() == 'SQLite3':
            if me.connector != None:
                if me.connector.sql_type == 'MySQL':
                    me.connector.disconnect()
            f=me.parent.dbName.text() 
            if os.path.splitext(f)[1] != '.db':
                f+='.db'
            me.parent.dbName.setText(f)

            me.connector=sqlite.handler(me.parent)
            me.connector.moveToThread(me.connector_thread)
            me.connector.mkDb()
            me.formatString='?'
            me.parent.statusBar().showMessage(msg)

        print(msg)


    def start(me):
        me.setConnector()
        me.timer.start(me.parent.main['interval'])
    
    table='logs'
    db='hydrogenous'
    formatString=''
    connector=None

    @pyqtSlot()
    def logData(me):
        if me.connector != None:
            if me.connector.cursor != None and me.connector.db != None:
                self=me.parent
                rowName='{}_uS{}'.format(time.strftime('%mm%dd%YY_%HH%MM%SS',time.localtime()),datetime.now().microsecond)
                tmp={rowName:me.parent.data_sig.copy()}
                me.parent.statusBar().showMessage(rowName)       
                me.sig.emit()
                jsonData=json.dumps(tmp)
                del(tmp)
                me.sig.emit()

                sql='insert into {1}(id,data) values({0},{0})'.format(me.formatString,me.table)
                try:
                    if me.connector.sql_type == 'MySQL':
                        if me.connector.db.open:
                            me.connector.cursor.execute(sql,(rowName,jsonData))
                            me.connector.db.commit()
                    if me.connector.sql_type == 'SQLite3':
                        me.connector.queData(sql,rowName,jsonData)
                except Exception as e:
                    print(e) 
                print(rowName)
                
        gc.collect()
        me.sig.emit()        
