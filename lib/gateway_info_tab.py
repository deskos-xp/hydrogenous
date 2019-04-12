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
import gateways_info

class grapher(QtCore.QThread,QtCore.QCoreApplication):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent):
        QtCore.QThread.__init__(me,parent)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.timer=QtCore.QTimer()
        me.timer.moveToThread(me)
        #work this data into network tab thread
        me.timer.timeout.connect(lambda: me.updateData(me.parent,k=me.name))
        me.graph=QtWidgets.QDialog(me.parent)
        me.tool=gateways_info.Ui_gateway_info()
        me.tool.setupUi(me.graph)
        
        #me.tool.nic.setTitle(me.name)        
        #prefill rows of qtablewidget with data
        #reference document from stack over flow
        #https://stackoverflow.com/questions/40815730/how-to-add-and-retrieve-items-to-and-from-qtablewidget-using-pyqt5?rq=1
        #rows=me.tool.tableWidget.rowCount()
        #me.tool.tableWidget.insertRow(rows)
        me.setup=False
        me.setupWidget(parent)
        me.gridWidget(parent)
        

    def setupWidget(me,self): 
        #this line clears header text as well, do not use it
        #me.tool.tableWidget.clear()
        me.tool.tableWidget.clearContents()
        me.tool.tableWidget.setRowCount(0)
        if 'net' in self.data_sig.keys(): 
            local=self.data_sig['net']['gateways']
            counter=0
            for family in local.keys():
                for subElements in local[family]:
                    me.tool.tableWidget.insertRow(counter)
                    items=[]
                    items.append(QtWidgets.QTableWidgetItem(family))
                    for i in subElements:
                        items.append(QtWidgets.QTableWidgetItem(i))
                    print(family,subElements,items) 
                    for col,i in enumerate(items):
                        me.tool.tableWidget.setItem(counter,col,i)
                    counter+=1
               
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
        self.exec_()
    '''   
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
                    pass
                    #me.setupWidget(self)
            else:
                pass
                #me.setupWidget(self)     
        me.sig.emit()
    '''

    def updateData(me,self,k=None,noStatPrint=False):
        if 'net' in self.data_sig.keys():
            tabIndex=self.tabWidget.currentIndex()
            tabText=self.tabWidget.tabText(tabIndex)

            if tabText.lower() == 'network':
                if self.net_sub.tabText(self.net_sub.currentIndex()).lower() == 'info.':
                    if me.setup == False:
                        me.setupWidget(self)
                    else:
                        pass
                        #me.update_info(self)
        else:
            print('missing data key "net"')
