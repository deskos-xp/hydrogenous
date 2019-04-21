from PyQt5 import QtWidgets,QtGui,QtCore
import os,sys,json
import psutil,copy
import engineering_notation as en
from hurry.filesize import si,size,iec
lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import rsrc,canvas,resource
import canvas2
import disk_info
from hurry.filesize import size,iec
from PyQt5.QtCore import pyqtSlot

class grapher(QtCore.QObject):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent,thread=None):
        super(me.__class__, me).__init__(thread)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.setup=False
        me.timer=QtCore.QTimer()
        #me.timer.moveToThread(me)
        #work this data into network tab thread
        me.timer.timeout.connect(me.updateData)
        me.graph=QtWidgets.QDialog(parent)
        #load obj from 
        me.tool=disk_info.Ui_disk_info()
        me.tool.setupUi(me.graph)

        me.gridWidget(parent)
        me.run()

    def update_info(me,self):
        #update disk widgets
        partitions=self.data_sig['disk']['partitions']
        usage=self.data_sig['disk']['usage']
        if me.data_partitions != partitions:
            me.setupWidget(self)
        me.sig.emit()

        if me.data_usage != usage:
            me.setupWidget(self)        

        #print(partitions,usage,end='\n')
        me.sig.emit()

    def setupWidget(me,self):
        me.tool.diskTable.clearContents()
        me.tool.diskTable.setRowCount(0)
        partitions=self.data_sig['disk']['partitions']
        me.data_partitions=copy.copy(partitions)
        
        usage=self.data_sig['disk']['usage']
        me.data_usage=copy.copy(usage)

        for rowN,p in enumerate(partitions):
            row=[]
            me.tool.diskTable.insertRow(rowN)
            for col in p:
                row.append(QtWidgets.QTableWidgetItem(str(col)))

            for col in usage[p.device]:
                if len(str(col)) <= 4:
                    row.append(QtWidgets.QTableWidgetItem(str(col)))
                else:
                    row.append(QtWidgets.QTableWidgetItem(str(size(col,system=iec))))

            for colN,col in enumerate(row):    
                me.tool.diskTable.setItem(rowN,colN,col)
        #setup widget for first time
        #or
        #refresh widget from disk change
        me.setup=True

        #me.sig.emit()

    def quit(me):
        me.timer.stop()

    def wait(me):
        pass

    def start(me):
        me.timer.start(me.parent.main['interval'])

    def gridWidget(me,self):
        currentRows=self.disk_info.rowCount()
        myRow=currentRows+1

        self.disk_info.addWidget(me.graph,myRow,0,1,1)

    def run(self):
        try:
            self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        #self.exec_()

    @pyqtSlot()
    def updateData(me,k=None,noStatPrint=False):
        self=me.parent
        k=me.name
        if 'disk' in self.data_sig.keys():
            tabIndex=self.tabWidget.currentIndex()
            tabText=self.tabWidget.tabText(tabIndex)

            if tabText.lower() == 'disk':
                if self.disk_sub.tabText(self.disk_sub.currentIndex()).lower() == 'info.':
                    if me.setup == False:
                        me.setupWidget(self)
                    else:
                        me.update_info(self)
            me.sig.emit()
        else:
            print('missing data key "disk"')
