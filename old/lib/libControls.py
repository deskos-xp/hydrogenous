#! /usr/bin/python3

from PyQt5 import QtWidgets,QtCore,QtGui
import os,json

class control:
    def __init__(me,self):
        me.actors(self)
        me.buttons(self)
        me.valueChanged(self)
        me.tab_changed(self)

    def tab_changed(me,self):
        self.tabWidget.currentChanged.connect(lambda sig: me.start_proper_timers(self,sig))

    def stop_everything(me,self):
        timers=self.main['thread_timer']
        for key in timers.keys():
            timers[key].quit()

    def start_proper_timers(me,self,index):
        obj=self.sender()    
        currentTab=obj.tabText(index)
        me.stop_everything(self)
        timers=self.main['thread_timer']
        if currentTab == 'Processing':
            timers['swap'].start()
            timers['cpu'].start()
            timers['ram'].start()
        if currentTab == 'Processes':
            timers['tasks'].start()
        if currentTab == 'Network':
            for i in self.main['net']['monitor'].keys():
                for x in self.main['net']['monitor'][i].keys():
                    self.main['net']['monitor'][i][x].quit()
                    self.main['net']['monitor'][i][x].start()

    def quit(me,self):
        for k in self.main['timers'].keys():
            self.main['timers'][k].stop()

        for k in ['cpu','ram','swap','tasks']:
            self.main['thread_timer'][k].quit()
            self.main['thread_timer'][k].wait()
        QtWidgets.QApplication.quit()

    def actors(me,self):
        self.actionQuit.triggered.connect(lambda: me.quit(self))
        self.tasks.clicked.connect(lambda sig: me.tasks_clicked(self,sig))        

    def buttons(me,self):
        self.intervalSet.clicked.connect(lambda: me.saveInterval(self))
        self.setGraphSize.clicked.connect(lambda: me.saveGraphSize(self))
        self.select_facecolor.clicked.connect(lambda: me.saveFaceColor(self,noLEChange=False))
        self.setLineFmt.clicked.connect(lambda: me.saveLineFmt(self))
        self.select_gridColor.clicked.connect(lambda: me.saveGridColor(self,noLEChange=False))
        
        self.deselect_all.clicked.connect(lambda: me.clear(self,self.tasks))

    def tasks_clicked(me,self,sig):
        skipNext=False
        '''
        for i in range(1,count):
            w=self.main['tasks']['model'].item(i,column=1)
            if w != None:
                if w.text() not in sig.keys():
                    print(w.text())
                    self.main['tasks']['model'].removeRow(i)
                    self.selected_pid=None
                    skipNext=True
        '''
        if skipNext == False:
            obj=self.sender()
            row=sig.row()
            col=1
            self.selected_pid=sig.sibling(row,col).data() 
            w=self.main['tasks']['model'].item(row,1)
            if w != None:
                ind=self.main['tasks']['proxy'].mapFromSource(w.index())
                #print(ind.row())
                #self.tasks.setCurrentIndex(ind)
                self.tasks.selectRow(ind.row())

    def clear(me,self,task):
        task.selectColumn(-1)
        task.selectRow(-1)
        task.clearSelection()
        self.selected_pid=None

    def valueChanged(me,self):
        self.facecolor.textChanged.connect(lambda: me.saveFaceColor(self,noLEChange=True))
        self.gridColor.textChanged.connect(lambda: me.saveGridColor(self,noLEChange=True))

    def saveLineFmt(me,self):
        self.main['line-fmt']['current']=self.main['line-fmt']['available'][self.line_fmt.currentText()]
        print(self.line_fmt.currentText())
        me.saveSettings(self)

    def saveGridColor(me,self,noLEChange=False):
        if noLEChange == False:
            tmp=QtWidgets.QColorDialog.getColor(QtGui.QColor(self.gridColor.text()))
            if tmp.isValid():
                self.main['gridColor']['current']=tmp.name()
                self.gridColor.setText(self.main['gridColor']['current'])
        else:
            self.main['gridColor']['current']=self.gridColor.text()
        me.saveSettings(self)

    def saveFaceColor(me,self,noLEChange=False):
        if noLEChange == False:
            tmp=QtWidgets.QColorDialog.getColor(QtGui.QColor(self.facecolor.text()))
            if tmp.isValid():
                self.main['facecolor']['current']=tmp.name()
                self.facecolor.setText(self.main['facecolor']['current'])
        else:
            self.main['facecolor']['current']=self.facecolor.text()
        me.saveSettings(self)

    def saveInterval(me,self):
        self.main['interval']=self.interval.value()
        for i in ['cpu','ram','swap']:
            self.main['timer'][i].stop()
        self.define_timer()
        me.saveSettings(self)

    def saveGraphSize(me,self):
        self.main['graphSize']=self.graphSize.value()
        me.saveSettings(self)

    def saveSettings(me,self):
        tmp={}
        tmp['graphSize']=self.main['graphSize']
        tmp['interval']=self.main['interval']
        tmp['line-fmt']=self.main['line-fmt']
        tmp['facecolor']=self.main['facecolor']
        tmp['gridColor']=self.main['gridColor']

        print(tmp)
        with open(os.path.join(self.main['config']['dir'],self.main['config']['startup']),'w') as cfg:
            json.dump(tmp,cfg)

