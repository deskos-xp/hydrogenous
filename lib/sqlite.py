#! /usr/bin/env python3

import os,json
from datetime import datetime
import time
import sqlite3
from PyQt5 import QtCore,QtWidgets

class handler(QtCore.QObject):
    sql_type='SQLite3'
    commit=QtCore.pyqtSignal()
    def __init__(me,self):
        super(me.__class__,me).__init__(None)
        me.cursor=None
        me.db=None
        me.parent=self
        me.data=()        
        me.commit.connect(me.saveData)

    def saveData(me):
        if me.db == None:
            me.mkDb()
        if me.data != ():
            me.commitData(me.data[0],me.data[1],me.data[2])
            me.data=()

    def mkDb(me):
        self=me.parent
        sql_create_table='''create table if not exists {}(id text,data blob);'''.format(self.main['dbTable'])
        if self.main['dbName'] not in ['',None]:
            me.db=sqlite3.connect(self.main['dbName'])
            me.cursor=me.db.cursor()
        me.cursor.execute(sql_create_table)
        me.db.commit()

    def queData(me,sql,rowName,jsonData):
        me.data=(sql,rowName,jsonData)
        me.commit.emit()

    def commitData(me,sql,rowName,jsonData):
        me.cursor.execute(sql,(rowName,jsonData))
        me.db.commit()

    def disconnect(me):
        if me.db != None:
            me.db.commit()
            me.db.close()
