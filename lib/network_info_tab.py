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
import network_info
from PyQt5.QtCore import pyqtSlot

class grapher(QtCore.QObject):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent,thread=None):
        #QtCore.QThread.__init__(me,parent)
        super(me.__class__,me).__init__(thread)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.timer=QtCore.QTimer()
        #me.timer.moveToThread(me)
        #work this data into network tab thread
        me.timer.timeout.connect(me.updateData)
        me.graph=QtWidgets.QDialog(me.parent)
        me.tool=network_info.Ui_network_info()
        me.tool.setupUi(me.graph)
        me.tool.nic.setTitle(me.name)        
        #prefill rows of qtablewidget with data
        #reference document from stack over flow
        #https://stackoverflow.com/questions/40815730/how-to-add-and-retrieve-items-to-and-from-qtablewidget-using-pyqt5?rq=1
        #rows=me.tool.tableWidget.rowCount()
        #me.tool.tableWidget.insertRow(rows)
        me.setup=False
        me.gridWidget(parent)
        me.run()

    def setupWidget(me,self): 
        #me.tool.tableWidget.clear()
        me.tool.tableWidget.clearContents()
        me.tool.tableWidget.setRowCount(0)
        for num,i in enumerate(self.data_sig['net']['addrs'][me.name]):
            me.tool.tableWidget.insertRow(num)
            items=[]
            for x in i:
                if type(x) != type(str()) and x != None:
                    try:
                        x=x.name
                    except Exception as e:
                        x=None
                        print(e)
                items.append(QtWidgets.QTableWidgetItem(x))
            for num2,x in enumerate(items):
                me.tool.tableWidget.setItem(num,num2,x)
                #header = me.tool.tableWidget.horizontalHeader()       
                #header.setSectionResizeMode(num2, QtWidgets.QHeaderView.Stretch)
        
        me.setup=True      

    def gridWidget(me,self):
        currentRows=self.net_info_grid.rowCount()
        myRow=currentRows+1
        self.net_info_grid.addWidget(me.graph,myRow,0,1,1)

    def run(self):
        try:
            self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        #self.exec_()
    
    def quit(me):
        me.timer.stop()

    def wait(me):
        pass

    def start(me):
        me.timer.start(me.parent.main['interval'])
       
    def update_info(me,self):
        #iterate through the rows for the address
        #if the address does not exist in data_sig
        #drop the row
        #if the address does exist
        #check if any fields have changed and update them if necessary        
        #print(self.data_sig['net']['addrs'][me.name])
        table=me.tool.tableWidget
        rows=table.rowCount()
        columns=table.columnCount()
        addrs=[i.address for i in self.data_sig['net']['addrs'][me.name]]
        col=1
        for i in range(rows):
            rowD=self.data_sig['net']['addrs'][me.name]
            if len(rowD) == rows:
                rowD=rowD[i]
                item=table.item(i,col)
                found=item.text()
                counter=0
                if found in rowD.address:
                    row=item.row()
                    col=item.column()
                    #print(rowD.address,row,col)
                    counter+=1
                    #print(found,rowD.address)
                else:
                    me.setupWidget(self)
            else:
                me.setupWidget(self)    
        #me.sig.emit()

    @pyqtSlot()
    def updateData(me,k=None,noStatPrint=False):
        self=me.parent
        k=me.name
        if 'net' in self.data_sig.keys():
            tabIndex=self.tabWidget.currentIndex()
            tabText=self.tabWidget.tabText(tabIndex)

            if tabText.lower() == 'network':
                if self.net_sub.tabText(self.net_sub.currentIndex()).lower() == 'info.':
                    if me.setup == False:
                        me.setupWidget(self)
                    else:
                        me.update_info(self)
            me.sig.emit()
        else:
            print('missing data key "net"')
