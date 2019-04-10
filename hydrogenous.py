#!/usr/bin/python3

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import Qt
import os,sys,engineering_notation,json
import hurry.filesize
import psutil,copy
import platform

lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import rsrc,canvas,libControls,threaded_tasks,processing_graphs,network_graphs,disk_graphs
import sensors_tab_battery,sensors_tab_temperatures,network_info_tab
from libproxyfilter import taskProxyFilter 
       
class rsrc(QtWidgets.QMainWindow,QtCore.QCoreApplication,rsrc.Ui_rsrc):
    safemode_used=False
    whoami=os.environ['USER']
    data={}    
    data_sig={} 
    #overtime data will be held in each thread class

    def define_timer(self):
        currentIndex=self.tabWidget.currentIndex()
        tabText=self.tabWidget.tabText(currentIndex)

        self.tasks_tab_handler()
        self.processing_tab_handler(tabText)
        self.network_tab_handler(tabText)
        self.disk_tab_handler(tabText)
        self.sensors_tab_handler(tabText)

    def disk_tab_handler(self,index):
        self.main['tabs']['disk']={}
        for i in psutil.disk_io_counters(perdisk=True).keys():
            self.main['tabs']['disk'][i]={}
            if i[-1] not in '1234567890':
                for mode in ['tx','rx']:
                    self.main['tabs']['disk'][i][mode]=disk_graphs.grapher(i,self.main,self,mode)
                    self.main['tabs']['disk'][i][mode].sig.connect(lambda: QtWidgets.QApplication.processEvents())
                    self.main['tabs']['disk'][i][mode].start()

    def sensors_tab_handler(self,index):
        if platform.uname().system == 'Linux':
            self.main['tabs']['sensors']={}
            self.main['tabs']['sensors']['battery']=sensors_tab_battery.grapher('battery',self.main,self)
            self.main['tabs']['sensors']['battery'].sig.connect(lambda: QtWidgets.QApplication.processEvents())
            self.main['tabs']['sensors']['battery'].start()
        
            self.main['tabs']['sensors']['temperatures']=sensors_tab_temperatures.grapher('temperatures',self.main,self)
            self.main['tabs']['sensors']['temperatures'].sig.connect(lambda: QtWidgets.QApplication.processEvents())
            self.main['tabs']['sensors']['temperatures'].start()

    def processing_tab_handler(self,index):
        self.main['tabs']['processing']={}
        self.main['tabs']['processing']['cpu']=processing_graphs.grapher('cpu',self.main,self)
        self.main['tabs']['processing']['cpu'].sig.connect(lambda: QtWidgets.QApplication.processEvents())

        
        self.main['tabs']['processing']['ram_percent']=processing_graphs.grapher('ram_percent',self.main,self)
        self.main['tabs']['processing']['ram_percent'].sig.connect(lambda: QtWidgets.QApplication.processEvents())

        
        self.main['tabs']['processing']['swap_percent']=processing_graphs.grapher('swap_percent',self.main,self)
        self.main['tabs']['processing']['swap_percent'].sig.connect(lambda: QtWidgets.QApplication.processEvents())

        self.main['tabs']['processing']['swap_percent'].start()
        self.main['tabs']['processing']['ram_percent'].start()
        self.main['tabs']['processing']['cpu'].start()

    def network_tab_handler(self,index):
        self.main['tabs']['network']={}
        self.main['tabs']['network_info']={}
        if 'net' in self.data_sig.keys():
            print(self.data_sig['net'])
            #create threads based on interfaces detected
        for i in psutil.net_if_addrs().keys():
            self.main['tabs']['network'][i]={}
            for mode in ['rx','tx']:
                self.main['tabs']['network'][i][mode]=network_graphs.grapher(i,self.main,self,mode)
                self.main['tabs']['network'][i][mode].sig.connect(lambda: QtWidgets.QApplication.processEvents())


                self.main['tabs']['network'][i][mode].start()

        for i in psutil.net_if_addrs().keys():
            self.main['tabs']['network_info'][i]=network_info_tab.grapher(i,self.main,self)
            self.main['tabs']['network_info'][i].sig.connect(lambda: QtWidgets.QApplication.processEvents())
            self.main['tabs']['network_info'][i].start()

    def tasks_tab_handler(self):
        currentTab=self.tabWidget.tabText(self.tabWidget.currentIndex())
        print(currentTab,0)
        self.main['collector']={}
        self.main['collector']['data']=[]       
        self.main['collector']['thread']=threaded_tasks.threaded_tasks('collector',self.main,self)
        self.main['collector']['thread'].sig.connect(self.update_data_internal)
        print(currentTab,1)
        #when adding more columns update this to update columns headers
        labels=['Task','PID','User','CPU %','RAM Bytes']
        self.main['tasks']['model']=QtGui.QStandardItemModel(0,len(labels))
        self.main['tasks']['proxy']=taskProxyFilter(self)
        #QtCore.QSortFilterProxyModel(self)
        self.main['tasks']['proxy'].setSourceModel(self.main['tasks']['model'])
        self.main['tasks']['model'].setHorizontalHeaderLabels(labels)
        self.tasks.setModel(self.main['tasks']['proxy'])
        self.tasks.setColumnWidth(0,250)
        self.tasks.setAutoScroll(False)
        self.tasks.setSortingEnabled(True)
        self.tasks.setWordWrap(False)
        self.tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tasks.sortByColumn(3,1)
        self.main['collector']['thread'].start()

    def update_data_internal(self,sig):    
        self.data_sig=sig
        self.tasks_update(sig)

    selected_pid=None
    def tasks_update(self,sig):
        sig_temp={}
        for key in sig.keys():
            if key not in ['disk','net','total','sensors']:
                sig_temp[key]=sig[key]
        sig=sig_temp
            
        #been hunting a arithmetic based logical error for 2 days now, found the issue. man, pixies would complain over starting
        #the counting of salt grains with one, when it was zero. LMAO!
    
        order=self.tasks.horizontalHeader().sortIndicatorOrder()
        sortedBy=self.tasks.horizontalHeader().sortIndicatorSection()
        self.tasks.sortByColumn(sortedBy,order)

        count=len(sig.keys())
        for i in range(0,count):
            w=self.main['tasks']['model'].item(i,column=1)
            if w != None:
                if w.text() not in sig.keys():
                    self.main['tasks']['model'].removeRow(i)


        empty=[
                    QtGui.QStandardItem(''),
                    QtGui.QStandardItem(''),
                    QtGui.QStandardItem(''),
                    QtGui.QStandardItem(''),
                    QtGui.QStandardItem(''),
                ]
        try:
            #if self.tasks == None:
            self.main['tasks']['model'].setRowCount(len(sig.keys()))
            #self.tasks=len(sig.keys())+1
            for num,i in enumerate(sig.keys()):
                w=self.main['tasks']['model'].findItems(i,QtCore.Qt.MatchExactly,column=1)
                #when adding new columns to each table, update column to reflect the info gained from sig
                columns=[
                            QtGui.QStandardItem(sig[i]['name']),
                            QtGui.QStandardItem(),
                            QtGui.QStandardItem(sig[i]['user']),
                            QtGui.QStandardItem(sig[i]['cpu']),
                            QtGui.QStandardItem(),
                            ]

                columns[1].setData(int(i),QtCore.Qt.DisplayRole)
                columns[3].setData(float(sig[i]['cpu']),QtCore.Qt.DisplayRole)
                columns[4].setData(sig[i]['ram'],QtCore.Qt.DisplayRole)
                #columns[4].setText(hurry.filesize.size(sig[i]['ram']))
                if w == []:
                    #find the next empty line 
                    self.main['tasks']['model'].insertRow(num,columns)
                else:
                    for ii in w:
                        if ii.text() == i:
                            #print(dir(ii))
                            r=ii.row()
                            #for num,i in enumerate(columns):
                            #    self.tasks.update(ii)
                            self.main['tasks']['model'].removeRow(r)
                            #print(w)
                            self.main['tasks']['model'].insertRow(r,columns)
    
                    #update rows
                #QtWidgets.QApplication.processEvents() 
           
           
            count=len(sig.keys())
            for i in range(0,count):
                w=self.main['tasks']['model'].item(i,column=1)
                if w != None:
                    if w.text() not in sig.keys():
                        self.main['tasks']['model'].removeRow(i)

        except:
            print('lets try again next cycle: {}'.format(sys.exc_info()))
        #print(self.selected_pid)
        if self.selected_pid != None:
            for i in range(self.main['tasks']['model'].rowCount()):
                skipNext=False
                w=self.main['tasks']['model'].item(i,1)
                if w != None:
                    if w.text() not in sig.keys():
                        print(w.text(),'removed')
                        self.main['tasks']['model'].removeRow(i)
                        skipNext=True
                    try:
                        if int(w.text()) == self.selected_pid and skipNext == False:
                            ind=self.main['tasks']['proxy'].mapFromSource(w.index())
                            #print(ind.row())
                            #self.tasks.setCurrentIndex(ind)
                            self.tasks.selectRow(ind.row())
                    except Exception as e:
                        print(e)
        self.tasks.updateEditorData()
        QtWidgets.QApplication.processEvents() 
        
    def load_settings(self):
        with open(os.path.join(self.main['config']['dir'],self.main['config']['startup']),'r') as cfg:
            tmp=json.load(cfg)
            self.main['graphSize']=tmp['graphSize']
            self.main['graphSize']=tmp['graphSize']

            self.main['interval']=tmp['interval']
            self.main['line-fmt']=tmp['line-fmt']
            self.main['facecolor']=tmp['facecolor']
         
    def setWidget_settings(self):
        self.interval.setValue(self.main['interval'])
        self.graphSize.setValue(self.main['graphSize'])
        #for i in self.main['line-fmt']['available'].keys():
        #    self.line_fmt.addItem(i)
        '''
        name=None
        for i in self.main['line-fmt']['available'].keys():
            if self.main['line-fmt']['available'][i] == self.main['line-fmt']['current']:
                name=i
        if name != None:
            self.line_fmt.setCurrentIndex(self.line_fmt.findText(name))
        '''
        self.facecolor.setText(self.main['facecolor']['current'])
        self.lineColor.setText(self.main['line-fmt']['current'])

    def notify(self,rec,event):
        try:
            return QApplication.notify(rev,event)
        except Exception as e:
            return e

    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.main={}
        self.main['tabs']={}        
        self.main['tasks']={}
        self.main['line-fmt']={}
        self.main['line-fmt']['current']='r-'
        self.main['facecolor']={}
        self.main['facecolor']['current']='w'

        self.main['graphSize']={}
        self.main['graphSize']=25
        self.main['gridColor']={}
        self.main['gridColor']['current']='w'

        self.main['config']={}
        
        self.main['config']['dir']=os.path.join(os.environ['PWD'],'etc')
        self.main['config']['startup']='hydrogenous.json'

        self.main['used']={}
        self.main['controls']=libControls.control(self)

        self.main['interval']=2000
        self.load_settings()
        self.setWidget_settings()
        self.define_timer()
        self.show()
       
       
def setFusionColor():
    #this bit can be found at https://gist.github.com/mstuttgart/37c0e6d8f67a0611674e08294f3daef7
    #it is not mine
    dark_palette = QPalette() 
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    return dark_palette
    

    #App.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


if __name__ == '__main__': 
    a=QtWidgets.QApplication(sys.argv)
    app=rsrc()
    a.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    a.setPalette(setFusionColor())
    print(QtWidgets.QStyleFactory.keys())
    a.exec_()
