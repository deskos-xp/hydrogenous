from PyQt5 import QtWidgets,QtGui,QtCore
import os,sys,json
import psutil,copy
import engineering_notation as en
from hurry.filesize import si,size,iec
lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import rsrc,canvas,resource


class threaded_tasks(QtCore.QThread,QtCore.QCoreApplication):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal(dict)
    err=QtCore.pyqtSignal(tuple)
    
    def __init__(self,name,mainCopy,parent):
        self.main=mainCopy
        self.parent=parent
        self.name=name
        QtCore.QThread.__init__(self,parent)

    def run(self):
        try:
            self.timer=QtCore.QTimer()
            self.timer.timeout.connect(lambda: self.updateData(self.parent,k=self.name))
            self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        self.exec_()

    tx={}
    rx={}

    def updateData(me,self,k=None,noStatPrint=False):
        mod={}
        cmd=None
        
        for i in psutil.process_iter():
            cmd=' '.join(i.cmdline())
            name_list=[i.name(),]
            if cmd != '':
                name_list.append(cmd)
            mod[str(i.pid)]={
                            'name':' | '.join(name_list),
                            'pid':i.pid,
                            'user':i.username(),
                            'cpu':float(round(i.cpu_percent()/psutil.cpu_count(),2)),
                            'ram':size(i.memory_info().rss,system=iec),
                        }
        mod['net']={
                    'io':psutil.net_io_counters(pernic=True),
                    'stats':psutil.net_if_stats(),
                    'addrs':psutil.net_if_addrs(),
                    'speed':{}
                    }

        if me.rx == {}:
            for i in mod['net']['io'].keys():
                me.rx[i]=0
        if me.tx == {}:
            for i in mod['net']['io'].keys():
                me.tx[i]=0
        if mod['net']['speed'] == {}:
            for i in mod['net']['io'].keys():
                mod['net']['speed'][i]={}
                for k in ['rx','tx']:
                    mod['net']['speed'][i][k]=0

        for i in me.rx.keys():
            if me.rx[i] > 0:
                mod['net']['speed'][i]['rx']=mod['net']['io'][i].bytes_recv-me.rx[i]
        for i in me.tx.keys():
            if me.tx[i] > 0:
                mod['net']['speed'][i]['tx']=mod['net']['io'][i].bytes_sent-me.tx[i]

        for i in me.tx.keys():
            me.tx[i]=mod['net']['io'][i].bytes_sent

        for i in me.rx.keys():
            me.rx[i]=mod['net']['io'][i].bytes_recv
            
        mod['disk']={
                'io':psutil.disk_io_counters(perdisk=True),
                'partitions':psutil.disk_partitions(),
                    'usage':{}
                    }
        for path in mod['disk']['partitions']:
            mod['disk']['usage'][path.device]=path 

        me.sig.emit(mod)
