#!/usr/bin/python3

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import Qt
import os,sys,engineering_notation,json
import hurry.filesize
import psutil,copy

lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import rsrc,canvas,resources,libControls,threaded_tasks
from netwisk import netwisk
from libproxyfilter import taskProxyFilter 

class threaded_update(QtCore.QThread,QtCore.QCoreApplication):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    safemode_used=False
    sig=QtCore.pyqtSignal(tuple)
    
    def __init__(self,name,mainCopy,parent):
        self.main=mainCopy
        self.parent=parent
        self.name=name
        QtCore.QThread.__init__(self,parent)
    
    def run(self):
        try:
            self.main['timer'][self.name]=QtCore.QTimer()
            self.main['timer'][self.name].timeout.connect(lambda: self.updateData(self.parent,k=self.name))
            self.main['timer'][self.name].start(self.main['interval'])
            self.sig.emit(())    
        except Exception as e:
            self.sig.emit((e,))
        self.exec_()

    def updateTitles(me,self,k=None):
        if k == 'ram':
            self.rambox.setTitle(self.main['used']['ram']) 
        if k == 'cpu':
            self.cpubox.setTitle(self.main['used']['cpu'].format(self.main['data']['cpu'][-1]))
        if k == 'swap':
            self.swapbox.setTitle(self.main['used']['swap'])

    def updateData(me,self,k=None,noStatPrint=True):
        d=resources.resource_used.used(self,k)
        QtWidgets.QApplication.processEvents()
        self.main['used']=resources.resource_used.values(None)

        if k == None:
            exit('missing "k" value to updateData()')
        else:
            self.main['data'][k].append(d[k])
            self.main['data'][k]=self.main['data'][k][-1*self.main['graphSize']:]
            try:
                if self.safemode_used == True:
                    self.safemode_used=False
                    self.main['line-fmt']['current']=self.main['line-fmt']['available'][self.line_fmt.currentText()]
                #print(psutil.cpu_percent())
                #print(self.main['data'][k],k)
                self.main['graphs'][k].plot(
                    self.main['data'][k],
                    '{}'.format(k.upper()),
                    fmt=self.main['line-fmt']['current'],
                    glen=self.main['graphSize'],
                    bg=self.main['facecolor']['current'],
                    gridColor=self.main['gridColor']['current'],
                    )
            except Exception as e:
                print(e)
                self.safemode_used=True
                self.safeMode()
                self.main['graphs'][k].plot(
                    self.main['data'][k],
                    '{}'.format(k.upper()),
                    fmt=self.main['line-fmt']['current'],
                    glen=self.main['graphSize'],
                    bg=self.main['facecolor']['current'],
                    gridColor=self.main['gridColor']['current']
                    )
            me.updateTitles(self,k=k)
            QtWidgets.QApplication.processEvents()
        if noStatPrint == False:
            print(self.main['data'][k][-1],self.main['used'][k],self.main['interval'],k)
        
class rsrc(QtWidgets.QMainWindow,QtCore.QCoreApplication,rsrc.Ui_rsrc):
    data={
            'ram':[0 for i in range(25)],
            'cpu':[0 for i in range(25)],
            'swap':[0 for i in range(25)]
            }
    safemode_used=False
    whoami=os.environ['USER']
    
    def define_timer(self):
        currentTab=self.tabWidget.tabText(self.tabWidget.currentIndex())
        print(currentTab,0)
        k=['ram','cpu','swap']
        self.main['timer']={}
        for i in k:
            self.main['timer'][i]=QtCore.QTimer(self)
       
        self.main['thread_timer']={}
        
        self.main['thread_timer']['swap']=threaded_update('swap',self.main,self)
        self.main['thread_timer']['cpu']=threaded_update('cpu',self.main,self)
        self.main['thread_timer']['ram']=threaded_update('ram',self.main,self)

        if currentTab == 'Processing':
            self.main['thread_timer']['swap'].start()
            self.main['thread_timer']['cpu'].start()
            self.main['thread_timer']['ram'].start()
        
        self.main['tasks']['data']=[]       
        self.main['thread_timer']['tasks']=threaded_tasks.threaded_tasks('tasks',self.main,self)
        self.main['thread_timer']['tasks'].sig.connect(self.update_gui)
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
        #t=mySortFilterProxy(self.main['tasks']['model'])
        self.tasks.setAutoScroll(False)
        self.tasks.setSortingEnabled(True)
        self.tasks.setWordWrap(False)
        self.tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.tasks.sortByColumn(3,1)
        print(currentTab,2)
        if currentTab == 'Processes' or currentTab == 'Network':
            self.main['thread_timer']['tasks'].start()
        print(currentTab,3)
        '''
        for i in range(self.tabWidget_4.count()):
            tab=self.tabWidget_4.tabText(i)
            if self.whoami == 'root':
                if tab == 'Root':
                    self.tabWidget_4.setCurrentIndex(i)
            else:
                if tab == 'User':
                    self.tabWidget_4.setCurrentIndex(i)
        '''


        #self.main['tasks']['model'].item(
        #obj()

    def update_gui(self,sig):    
        self.tasks_update(sig)
        print(self.main['net']['monitor']['wlp1s0'].keys())       
        for key in self.main['net']['monitor'].keys():
            for key_mode in ['rx','tx']:
                self.main['net']['monitor'][key][key_mode].data[key][key_mode].append(sig['net']['speed'][key][key_mode])
                self.main['net']['monitor'][key][key_mode].data[key][key_mode]=self.main['net']['monitor'][key][key_mode].data[key][key_mode][self.main['graphSize']*-1:]

                    #[key_mode].data[key][key_mode],'#')
        #update lists for tabs here 

    selected_pid=None

    def tasks_update(self,sig):
        sig_temp={}
        for key in sig.keys():
            if key not in ['disk','net']:
                sig_temp[key]=sig[key]
        sig=sig_temp
            
        #been hunting a arithmetic based logical error for 2 days now, found the issue. man, pixies would complain over starting
        #the counting of salt grains with one, when it was zero. LMAO!
        '''
        try:
            print(self.main['tasks']['model'].item(0,0).text(),self.main['tasks']['model'].item(0,1).text())
        except Exception as e:
            print(e)
        '''
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
            '''
            if self.tasks == None:
                for i in range(0,len(sig.keys())+1):
                    self.main['tasks']['model'].insertRow(num,empty)
            '''
            #if self.tasks == None:
            self.main['tasks']['model'].setRowCount(len(sig.keys()))
            #self.tasks=len(sig.keys())+1
            '''
            elif self.tasks != len(sig.keys())+1:
                disp=self.main['tasks']['model'].rowCount()
                proc=(len(sig.keys())+1)-disp
                for i in range(disp):
                    self.main['tasks']['model'].appendRow(empty)
                self.tasks=len(sig.keys())+1
            #ineshot
            '''
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

        except Exception as e:
            print('lets try again next cycle: {}'.format(e))
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
            self.main['gridColor']=tmp['gridColor']
         
    def setWidget_settings(self):
        self.interval.setValue(self.main['interval'])
        self.graphSize.setValue(self.main['graphSize'])
        for i in self.main['line-fmt']['available'].keys():
            self.line_fmt.addItem(i)
        
        name=None
        for i in self.main['line-fmt']['available'].keys():
            if self.main['line-fmt']['available'][i] == self.main['line-fmt']['current']:
                name=i
        if name != None:
            self.line_fmt.setCurrentIndex(self.line_fmt.findText(name))
        self.facecolor.setText(self.main['facecolor']['current'])
        self.gridColor.setText(self.main['gridColor']['current'])

    def notify(self,rec,event):
        try:
            return QApplication.notify(rev,event)
        except Exception as e:
            return e

    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)
        self.main={}
        self.main['timers']={}
        self.main['tasks']={}
        self.main['line-fmt']={}
        self.main['line-fmt']['current']='r-'
        self.main['facecolor']={}
        self.main['facecolor']['current']='w'

        self.main['graphs']={}
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
        self.main['data']={
            'ram':[0 for i in range(self.main['graphSize'])],
            'cpu':[0 for i in range(self.main['graphSize'])],
            'swap':[0 for i in range(self.main['graphSize'])]
            }

        self.setWidget_settings()

        self.main['used']=resources.resource_used.values(None)

        self.rambox.setTitle(self.main['used']['ram'])
        self.cpubox.setTitle(self.main['used']['cpu'].format(self.main['data']['cpu'][-1*self.main['graphSize']]))
        self.swapbox.setTitle(self.main['used']['swap'])
        
        self.define_timer()

        self.main['net']={}
        self.main['net']['monitor']={}


        try:
            self.graphWidgets()
        except:
            self.safeMode()
            self.graphWidgets()


        for num,key in enumerate(psutil.net_if_addrs().keys()):
            self.main['net']['monitor'][key]={}
            self.main['net']['graphs'][key]={}
            for key_mode in ['rx','tx']:

                self.main['net']['monitor'][key][key_mode]=netwisk(self,key,num,mode=key_mode)
                self.main['net']['graphs'][key][key_mode]=canvas.PlotCanvas(
                    fmt=self.main['line-fmt']['current'],
                    glen=self.main['graphSize'],
                    data=self.main['net']['monitor'][key][key_mode].data[key][key_mode],
                    bg=self.main['facecolor']['current'],
                    gridColor=self.main['gridColor']['current'],
                    title=key.upper())
                #print(num,key) 
                #self.main['net']['graphs'][key]=None
                self.net.addWidget(self.main['net']['graphs'][key][key_mode],num,0,1,1)
                self.main['net']['monitor'][key][key_mode].start()

        self.cpu.addWidget(self.main['graphs']['cpu'],0,0,0,0)
        self.ram.addWidget(self.main['graphs']['ram'],0,0,0,0)
        self.swap.addWidget(self.main['graphs']['swap'],0,0,0,0)


            #self.main['net']['monitor'][key].sig.connect(self.update_gui,'net')
        self.show()

    def safeMode(self):
        self.main['facecolor']['current']='w'
        self.main['line-fmt']['current']='r-'

    def graphWidgets(self):
        self.main['graphs']['cpu']=canvas.PlotCanvas(
                fmt=self.main['line-fmt']['current'],
                glen=self.main['graphSize'],
                data=self.main['data']['cpu'],
                bg=self.main['facecolor']['current'],
                gridColor=self.main['gridColor']['current'],
                title='CPU')

        self.main['graphs']['ram']=canvas.PlotCanvas(
                fmt=self.main['line-fmt']['current'],
                glen=self.main['graphSize'],
                data=self.main['data']['ram'],
                bg=self.main['facecolor']['current'],
                gridColor=self.main['gridColor']['current'],
                title='RAM')

        self.main['graphs']['swap']=canvas.PlotCanvas(
                fmt=self.main['line-fmt']['current'],
                glen=self.main['graphSize'],
                data=self.main['data']['swap'],
                bg=self.main['facecolor']['current'],
                gridColor=self.main['gridColor']['current'],
                title='SWAP')
        
        if 'net' not in self.main.keys():
            self.main['net']={}
        if 'graphs' not in self.main['net'].keys():
            self.main['net']['graphs']={}
        
       
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
