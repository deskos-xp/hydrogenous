#! /usr/bin/env python3
import platform
import pymysql
import netifaces as nm
from PyQt5 import QtCore,QtWidgets
class handler(QtCore.QObject):
    sql_type='MySQL'
    database=None
    def __init__(me,self,host,user,password,db,port=3306):
        super(me.__class__,me).__init__(None)

        macAddress=nm.ifaddresses(([i for i in nm.interfaces() if i != 'lo'][0]))[nm.AF_PACKET][0]['addr'].replace(':','_')
        hostname=platform.uname().node
        db='{}__{}__{}'.format(db,macAddress,hostname)
        me.cursor=None
        me.db=None
        sql_use='''use {};'''.format(db)
        sql_create='''create database if not exists {}'''.format(db);
        sql_create_table=''' create table if not exists {}(id text,data blob);'''.format(self.main['dbTable'])

        try:
            me.db=pymysql.connect(
                                    host=host,
                                    user=user,
                                    password=password,
                                    port=port,
                            )
            me.cursor=me.db.cursor()
            print(db)
            me.cursor.execute(sql_create)
            me.db.commit()
            me.cursor.execute(sql_use)
            me.cursor.execute(sql_create_table)
            me.db.commit()
            self.statusBar().showMessage('Successfully Connected "{}@{}:{}"'.format(user,host,port))
        except pymysql.err.OperationalError as err:
            print(err)
            self.statusBar().showMessage(str(err))
            me.db=None
            me.cursor=None
        except pymysql.err.ProgrammingError as err:
            print(err)
            self.statusBar().showMessage(str(err))
            print(
                ['host',host],
                ['password',password],
                ['user',user],
                ['port',port],
                ['db',db],
                ['sql_create',sql_create],
                ['sql_use',sql_use],
                sep='\n',
                )

    def disconnect(me):
        if me.db != None:
            me.db.commit()
            me.db.close()    
