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
import gateway_info_tab,disk_info_tab
import logger,settings_logger
from PyQt5.QtCore import pyqtSlot
from tracemalloc import Filter
import gc
import tracemalloc
import tasks_search

class TableView(QtWidgets.QTableView):
    def __init__(self,WINDOW, *args, **kwargs):
        QtWidgets.QTableView.__init__(self, *args, **kwargs)
        #self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        #self.ScrollHint(QtWidgets.QAbstractItemView.EnsureVisible)
        self.WINDOW=WINDOW

    def clipboard(self,mode,sig):
        rowData=''
        if mode == 'left':
            columns=self.model().columnCount()
            rowData=' | '.join([str(sig.sibling(sig.row(),i).data()) for i in range(columns)])
        elif mode == 'right':
            rowData=str(sig.data())
        cb=QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(rowData,mode=cb.Clipboard)
        self.WINDOW.statusBar().showMessage('"{}" copied to clipboard'.format(rowData))
        
        #print(mode,sig.data())

    def process_context_menu(self,index):
        pid=index.sibling(index.row(),1).data()
        self.WINDOW.process_search.setText(str(pid))
        self.WINDOW.searchOption_pid.setChecked(True)
        for i in range(self.WINDOW.tabWidget_4.count()):
            if self.WINDOW.tabWidget_4.tabText(i) == 'Search':
                self.WINDOW.tabWidget_4.setCurrentIndex(i)
        print('this is placeholder for process control functionality: {}'.format(pid))
    
    def mousePressEvent(self,event):
        pos=(event.pos().x(),event.pos().y())
        index=self.indexAt(event.pos())
        
        if event.button() == QtCore.Qt.MiddleButton:
            self.clipboard('middle',index)
        if event.button() == QtCore.Qt.RightButton:
            self.process_context_menu(index)
        if event.button() == QtCore.Qt.LeftButton:
            self.clipboard('left',index)
        self.clicked.emit(index)
    
class rsrc(QtWidgets.QMainWindow,QtWidgets.QApplication,QtCore.QCoreApplication,rsrc.Ui_rsrc):
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
        #setup disks tab first
        self.disk_tab_handler(tabText)
        #start polling for new data
        self.disk_timer()
        self.sensors_tab_handler(tabText)
        self.logger_handler()
        self.tasks_search_handler()

    def tasks_search_handler(self):
        self.main['tasks_search_thread']=QtCore.QThread()
        self.main['tasks_search_obj']=tasks_search.threaded_search(self)
        self.main['tasks_search_obj'].moveToThread(self.main['tasks_search_thread'])
        self.main['tasks_search_thread'].start()
        self.main['tasks_search_obj'].start()

    def logger_handler(self,reset=False):
        self.logger_groupbox.setEnabled(self.useLogger.isChecked())
        if self.useLogger.isChecked() == True:
            if reset == False:
                if 'logger' not in self.main.keys():
                    self.main['logger']=QtCore.QThread()
                    self.main['logger_obj']=logger.logger(self,"logger")
                    self.main['logger_settings'].__init__(self)
                    self.main['logger_obj'].moveToThread(self.main['logger'])
                self.main['logger'].start()
                if self.main['logger_obj'].timer.isActive() == False:
                    self.main['logger_obj'].timer.start(self.main['interval'])
            else:
                self.main['logger_obj'].timer.stop()
                self.main['logger_obj'].timer.setInterval(self.main['interval'])
                self.main['logger_obj'].start()
        else:
            print('quit')
            if 'logger' in self.main.keys():
                self.main['logger_obj'].quit()
                self.main['logger'].quit()
                self.main['logger'].wait()
                self.main.pop('logger')
                self.main.pop('logger_obj')
    @pyqtSlot()        
    def detect_disk(self):
        disks=psutil.disk_partitions()
        main_disks=self.main['tabs']['disk'].keys()

        tmp=[]
        for i in main_disks:
            count=0
            for ii in '1234567890':
                if ii not in i:
                    count+=1
            if count < len('1234567890'):
                tmp.append(i)
        main_disks=tmp

        tmp=[]
        all_part=[x.fstype for x in psutil.disk_partitions(all=True)]
        for i in main_disks:
            ap=[os.path.basename(p.device) for p in psutil.disk_partitions()]
            if i in ap:
                    tmp.append(i)
        main_disks=tmp
        tmp=[]
        
        #print(len(disks),len(main_disks),self.disks)
        if len(disks) != self.disks:
            self.disks=len(psutil.disk_partitions())
            for i in self.main['tabs']['disk_obj'].keys():
                for ii in self.main['tabs']['disk_obj'][i].keys():
                    self.main['tabs']['disk_obj'][i][ii].stop(self)
            for i in self.main['tabs']['disk'].keys():
                for ii in self.main['tabs']['disk'][i].keys():
                    self.main['tabs']['disk'][i][ii].quit()
                    self.main['tabs']['disk'][i][ii].wait()

            self.main['tabs']['disk']={}
            self.disk_tab_handler('disks',stage1Only=True)

    def disk_timer(self):
        print('started disk timer')
        self.main['disk_timer']=QtCore.QTimer()
        self.main['disk_timer'].timeout.connect(self.detect_disk)
        self.main['disk_timer'].start(self.main['interval'])

    def disk_tab_handler(self,index,stage1Only=False):
        self.disks=len(psutil.disk_partitions())
        self.main['tabs']['disk']={}
        self.main['tabs']['disk_obj']={}
        for i in psutil.disk_io_counters(perdisk=True).keys():
            self.main['tabs']['disk'][i]={}
            self.main['tabs']['disk_obj'][i]={}
            if i[-1] not in '1234567890':
                for mode in ['tx','rx']:
                    self.main['tabs']['disk'][i][mode]=QtCore.QThread()
                    self.main['tabs']['disk_obj'][i][mode]=disk_graphs.grapher(i,self.main,self,mode)
                    self.main['tabs']['disk_obj'][i][mode].moveToThread(self.main['tabs']['disk'][i][mode])
                    self.main['tabs']['disk'][i][mode].start()
        if stage1Only == False:
            self.main['tabs']['disk_info']=QtCore.QThread()
            self.main['tabs']['disk_info_obj']=disk_info_tab.grapher('Partitions',self.main,self)
            self.main['tabs']['disk_info_obj'].moveToThread(self.main['tabs']['disk_info'])
            self.main['tabs']['disk_info'].start()
 
    def sensors_tab_handler(self,index):
        if platform.uname().system == 'Linux':
            self.main['tabs']['sensors']={}
            self.main['tabs']['sensors']['battery']=QtCore.QThread()
            self.main['tabs']['sensors']['battery_obj']=sensors_tab_battery.grapher('battery',self.main,self)
            self.main['tabs']['sensors']['battery_obj'].moveToThread(self.main['tabs']['sensors']['battery'])
            self.main['tabs']['sensors']['battery'].start()

            self.main['tabs']['sensors']['temperatures']=QtCore.QThread()
            self.main['tabs']['sensors']['temperatures_obj']=sensors_tab_temperatures.grapher('temperatures',self.main,self)
            self.main['tabs']['sensors']['temperatures_obj'].moveToThread(self.main['tabs']['sensors']['temperatures'])
            self.main['tabs']['sensors']['temperatures'].start()

    def processing_tab_handler(self,index):
        self.main['tabs']['processing']={}
        self.main['tabs']['processing']['cpu']=QtCore.QThread()
        self.main['tabs']['processing']['cpu_obj']=processing_graphs.grapher('cpu',self.main,self)
        self.main['tabs']['processing']['cpu_obj'].moveToThread(self.main['tabs']['processing']['cpu'])

        self.main['tabs']['processing']['ram_percent']=QtCore.QThread()
        self.main['tabs']['processing']['ram_percent_obj']=processing_graphs.grapher('ram_percent',self.main,self)
        self.main['tabs']['processing']['ram_percent_obj'].moveToThread(self.main['tabs']['processing']['ram_percent']) 

        self.main['tabs']['processing']['swap_percent']=QtCore.QThread()
        self.main['tabs']['processing']['swap_percent_obj']=processing_graphs.grapher('swap_percent',self.main,self)
        self.main['tabs']['processing']['swap_percent_obj'].moveToThread(self.main['tabs']['processing']['swap_percent'])

        self.main['tabs']['processing']['swap_percent'].start()
        self.main['tabs']['processing']['ram_percent'].start()
        self.main['tabs']['processing']['cpu'].start()

    def network_tab_handler(self,index):
        self.main['tabs']['network']={}
        self.main['tabs']['network_obj']={}
        self.main['tabs']['network_info']={}
        self.main['tabs']['network_info_obj']={}
        if 'net' in self.data_sig.keys():
            print(self.data_sig['net'])
            #create threads based on interfaces detected
        for i in psutil.net_if_addrs().keys():
            self.main['tabs']['network'][i]={}
            self.main['tabs']['network_obj'][i]={}
            for mode in ['rx','tx']:
                self.main['tabs']['network'][i][mode]=QtCore.QThread()
                self.main['tabs']['network_obj'][i][mode]=network_graphs.grapher(i,self.main,self,mode)
                self.main['tabs']['network_obj'][i][mode].moveToThread(self.main['tabs']['network'][i][mode])

                self.main['tabs']['network'][i][mode].start()

        for i in psutil.net_if_addrs().keys():
            self.main['tabs']['network_info'][i]=QtCore.QThread()
            self.main['tabs']['network_info_obj'][i]=network_info_tab.grapher(i,self.main,self)
            self.main['tabs']['network_info_obj'][i].moveToThread(self.main['tabs']['network_info'][i])

            self.main['tabs']['network_info'][i].start()

        self.main['tabs']['network_info']['gateway_setup']=False
        self.main['tabs']['network_info']['gateway']=QtCore.QThread()
        self.main['tabs']['network_info']['gateway_obj']=gateway_info_tab.grapher('gateways',self.main,self)
        self.main['tabs']['network_info']['gateway_obj'].moveToThread(self.main['tabs']['network_info']['gateway'])
        self.main['tabs']['network_info']['gateway'].start()

        currentTab=self.tabWidget.tabText(self.tabWidget.currentIndex())
        print(currentTab,0)

    def tasks_tab_handler(self):        
        self.main['collector']={}
        self.main['collector']['data']=[] 
        self.main['collector']['thread']=QtCore.QThread()      
        
        self.main['collector']['thread_obj']=threaded_tasks.threaded_tasks('collector',self.main,self)
        self.main['collector']['thread_obj'].sig.connect(self.update_data_internal)
        self.main['collector']['thread_obj'].moveToThread(self.main['collector']['thread'])
        self.main['tasks_search']={} 
        #print(currentTab,1)
        self.tasks=TableView(self)
        self.discovered_tasks=TableView(self)
        self.gridLayout_44.addWidget(self.tasks,0,0,1,1)
        #add discovered tasks on search tab
        self.gridLayout_36.addWidget(self.discovered_tasks,0,0,1,1)
        self.main['controls'].lateLoad(self)
        #when adding more columns update this to update columns headers
        self.main['tasks']['labels']=['Task','PID','User','CPU %','RAM Bytes']
        self.main['tasks']['model']=QtGui.QStandardItemModel(0,len(self.main['tasks']['labels']))
        self.main['tasks']['proxy']=taskProxyFilter(self)

        self.main['tasks']['proxy'].setSourceModel(self.main['tasks']['model'])
        self.main['tasks']['model'].setHorizontalHeaderLabels(self.main['tasks']['labels'])
        self.tasks.setModel(self.main['tasks']['proxy'])
        self.tasks.setColumnWidth(0,250)
        self.tasks.setAutoScroll(False)
        self.tasks.setSortingEnabled(True)
        self.tasks.setWordWrap(False)
        self.tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tasks.sortByColumn(3,1)
        self.main['collector']['thread'].start()
        
        self.main['tasks_search']['model']=QtGui.QStandardItemModel(0,len(self.main['tasks']['labels']))
        self.main['tasks_search']['proxy']=taskProxyFilter(self)
        self.main['tasks_search']['proxy'].setSourceModel(self.main['tasks_search']['model'])
        self.main['tasks_search']['model'].setHorizontalHeaderLabels(self.main['tasks']['labels'])

    def update_data_internal(self,sig):    
        self.data_sig=sig
        self.tasks_update(sig)
        #self.tasks_search_update()
        gc.collect()

    def collect_stats(self,filtered=True):
        #need to iterate through data_sig in lib threaded tasks recursively and what is not a dict do a del() before adding new data and gc.collect() 
        if filtered == True:
            if 'old' not in dir(self):
                self.old=tracemalloc.take_snapshot()
            snapshot=tracemalloc.take_snapshot()
            filters = [Filter(inclusive=True, filename_pattern="*hydrogenous*")]    
            filtered_stats = snapshot.filter_traces(filters).compare_to(self.old.filter_traces(filters), 'traceback')    
            for stat in filtered_stats[:10]:
                print('''{}	
        new KiB {} 
        total KiB {} 
        new {} 
        total memory blocks: '''.format(stat.size_diff/1024, stat.size / 1024, stat.count_diff ,stat.count))        
    
                for line in stat.traceback.format():            
                    print(line)
            self.old=snapshot
        else:
            filters=[]
            if 'snapshots' not in dir(self):
                self.snapshots=[]
            self.snapshots.append(tracemalloc.take_snapshot())        
            if len(self.snapshots) >= 2: 
                stats = self.snapshots[-1].filter_traces(filters).compare_to(self.snapshots[-2], 'filename')    
                for stat in stats[:10]:                
                    print("""
{} 
    new KiB {} 
    total KiB {} 
    new {} total memory blocks: """.format(stat.size_diff/1024, stat.size / 1024, stat.count_diff ,stat.count))

                    for line in stat.traceback.format():                    
                        print(line)
    selected_pid=None

    def tasks_update(self,sig):
        if self.tabWidget.tabText(self.tabWidget.currentIndex()) != 'Processes':
            return None

        if self.debug == True:    
            self.collect_stats()
        sig_temp={}
        for key in sig.keys():
            if key not in ['disk','net','total','sensors']:
                sig_temp[key]=sig[key]
        sig=sig_temp
        del(sig_temp)            
        #been hunting a arithmetic based logical error for 2 days now, found the issue. man, pixies would complain over starting
        #the counting of salt grains with one, when it was zero. LMAO!
    
        order=self.tasks.horizontalHeader().sortIndicatorOrder()
        sortedBy=self.tasks.horizontalHeader().sortIndicatorSection()
        self.tasks.sortByColumn(sortedBy,order)
        del(order)
        del(sortedBy)

        count=len(sig.keys())
        for i in range(0,count):
            w=self.main['tasks']['model'].item(i,column=1)
            if w != None:
                if w.text() not in sig.keys():
                    self.main['tasks']['model'].removeRow(i)
 
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
                            del(r)
                    #update rows
                #QtWidgets.QApplication.processEvents() 
                 
           
            count=len(sig.keys())
            for i in range(0,count):
                w=self.main['tasks']['model'].item(i,column=1)
                if w != None:
                    if w.text() not in sig.keys():
                        self.main['tasks']['model'].removeRow(i)
                del(w)
            del(count)
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
                        gc.collect()
                        print(e,'3#')
                del(w)
        self.tasks.updateEditorData()
        QtWidgets.QApplication.processEvents() 
        
    def load_settings(self):
        with open(os.path.join(self.main['config']['dir'],self.main['config']['startup']),'r') as cfg:
            tmp=json.load(cfg)
            self.main['tabsConfig']=tmp['tabsConfig']
            self.main['graphSize']=tmp['graphSize']
            self.main['graphSize']=tmp['graphSize']
            self.main['useLogger']=tmp['useLogger']
            self.main['interval']=tmp['interval']
            self.main['line-fmt']=tmp['line-fmt']
            self.main['facecolor']=tmp['facecolor']
            self.main['dbName']=tmp['dbName']
            self.main['dbTable']=tmp['dbTable']

            self.main['format']=tmp['format']

            self.main['serverUser']=tmp['serverUser']
            self.main['serverAddress']=tmp['serverAddress']
            self.main['serverPort']=tmp['serverPort']

 
    def setWidget_settings(self):
        self.interval.setValue(self.main['interval'])
        self.graphSize.setValue(self.main['graphSize'])
        self.facecolor.setText(self.main['facecolor']['current'])
        self.lineColor.setText(self.main['line-fmt']['current'])
        self.useLogger.setChecked(self.main['useLogger'])
        self.dbName.setText(self.main['dbName'])
        self.dbTable.setText(self.main['dbTable'])
        self.serverPort.setValue(self.main['serverPort'])
        self.serverAddress.setText(self.main['serverAddress'])
        self.serverUser.setText(self.main['serverUser'])
        self.loggerSQLFormat.setCurrentIndex(self.loggerSQLFormat.findText(self.main['format']))
        self.setDefaultTabs()

    def setDefaultTabs(self):
        tabs=(
            (
                self.tabWidget,
                self.main['tabsConfig']['main']
            ),
            (
                self.sensors_tabs,
                self.main['tabsConfig']['sensors']
            ),
            (
                self.net_sub,
                self.main['tabsConfig']['net']
            ),
            (
                self.disk_sub,
                self.main['tabsConfig']['disk']
            ),
        )
        for t,Text in tabs:
            tabCount=t.count()
            for i in range(tabCount):
                text=t.tabText(i)    
                if text == Text:
                    t.setCurrentIndex(i)
                    break

    def notify(self,rec,event):
        try:
            return QApplication.notify(rev,event)
        except Exception as e:
            return e

    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.startup=False
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
        self.main['format']='MySQL' 
        self.main['config']['dir']=os.path.join(os.environ['PWD'],'etc')
        self.main['config']['startup']='hydrogenous.json'

        self.main['used']={}
        self.main['controls']=libControls.control(self)
        self.main['interval']=2000
        self.load_settings()
        self.setWidget_settings()

        self.main['logger_settings']=settings_logger.settings_logger(self)
        
        self.define_timer()
        self.startup=True
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
    app.debug=False
    if app.debug == True:
        tracemalloc.start(10)
    a.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    a.setPalette(setFusionColor())
    print(QtWidgets.QStyleFactory.keys())
    a.exec_()
