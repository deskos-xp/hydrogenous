
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import Qt
import os,sys,engineering_notation,json
import hurry.filesize
import psutil,copy
lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import canvas

class netwisk(QtCore.QThread,QtCore.QCoreApplication):
    def __init__(me,self,name,row,mode):
        me.self=self
        me.data={}
        me.name=name
        me.mode=mode
        me.data[name]={x:[0 for i in range(self.main['graphSize'])] for x in ['tx','rx']}
        if 'net' not in self.main.keys():
            self.main['net']={}
        if 'graphs' not in self.main['net'].keys():
            self.main['net']['graphs']={}
        
        QtCore.QThread.__init__(me,self)

    def run(me):
        self=me.self
        me.timer=QtCore.QTimer()
        me.timer.timeout.connect(lambda: me.mon(self,me.mode))
        me.timer.start(self.main['interval'])
        me.exec_()

    def mon(me,self,mode):
        try:
            #print(me.data[me.name]) 
            self.main['net']['graphs'][me.name][mode].plot(
                fmt=self.main['line-fmt']['current'],
                glen=self.main['graphSize'],
                data=me.data[me.name][mode],
                bg=self.main['facecolor']['current'],
                gridColor=self.main['gridColor']['current'],
                title=me.name.upper(),
                ylim=sorted(me.data[me.name][mode])[-1])
            #print(me.data)
        except Exception as e:
            #me.notify(self,e)
            print(e,me.name)

