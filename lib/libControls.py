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
        pass
        #self.tabWidget.currentChanged.connect(lambda sig: me.handle_threads(self,sig))
    
    def stop_all_threads(me,self):
        self.main['disk_timer'].stop()
        for i in self.main['tabs'].keys():
            if type(self.main['tabs'][i]) == type(dict()):
                for x in self.main['tabs'][i].keys():
                    if i not in ['network']:
                        if x not in ['gateway_setup',]:
                            print(self.main['tabs'][i][x],i,x)
                            if i in ['processing','network_info','disk_info','sensors']:
                                self.main['tabs'][i][x].quit()
                                self.main['tabs'][i][x].wait()
                                self.main['tabs'][i][x].start()
                            else:
                                for z in self.main['tabs'][i][x].keys():
                                    self.main['tabs'][i][x][z].quit()
                                    self.main['tabs'][i][x][z].wait()
                                    self.main['tabs'][i][x][z].start()
                    else:
                        for z in self.main['tabs'][i][x].keys():
                            self.main['tabs'][i][x][z].quit()
                            self.main['tabs'][i][x][z].wait()              
                            self.main['tabs'][i][x][z].start()              
            else:
                self.main['tabs'][i].quit()
                self.main['tabs'][i].wait()
                self.main['tabs'][i].start()
        self.main['disk_timer'].start()
    
    def handle_threads(me,self,sig):
        caller=self.sender()
        me.stop_all_threads(self)
        #tabText=caller.tabText(sig).lower()
        '''
        if tabText in self.main['tabs'].keys():
            for i in self.main['tabs'][tabText].keys():
                if tabText not in ['network']:
                    self.main['tabs'][tabText][i].start()
                else:
                    for z in self.main['tabs'][tabText][i].keys():
                        self.main['tabs'][tabText][i][z].start()
        '''
        #me.saveSettings(self)

    def quit(me,self):
        QtWidgets.QApplication.quit()

    def actors(me,self):
        self.actionQuit.triggered.connect(lambda: me.quit(self))
        self.tasks.clicked.connect(lambda sig: me.tasks_clicked(self,sig))        

    def buttons(me,self):
        self.intervalSet.clicked.connect(lambda sig: me.saveInterval(self,sig))
        self.setGraphSize.clicked.connect(lambda: me.saveGraphSize(self))
        self.select_facecolor.clicked.connect(lambda: me.saveFaceColor(self,noLEChange=False))
        self.setLineColor.clicked.connect(lambda: me.saveLineColor(self))
        
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
        self.lineColor.textChanged.connect(lambda: me.saveLineColor(self,noLEChange=True))

    def saveLineFmt(me,self):
        self.main['line-fmt']['current']=self.main['line-fmt']['available'][self.line_fmt.currentText()]
        print(self.line_fmt.currentText())
        me.saveSettings(self)

    def saveLineColor(me,self,noLEChange=False):
        if noLEChange == False:
            tmp=QtWidgets.QColorDialog.getColor(QtGui.QColor(self.lineColor.text()))
            if tmp.isValid():
                self.main['line-fmt']['current']=tmp.name()
                self.lineColor.setText(self.main['line-fmt']['current'])
        else:
            self.main['line-fmt']['current']=self.lineColor.text()
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

    def saveInterval(me,self,sig):
        self.main['interval']=self.interval.value()
        self.main['collector']['thread'].quit()
        self.main['collector']['thread'].wait()
        self.main['collector']['thread'].start()
        me.handle_threads(self,sig)
        '''
        self.main['tabs']['processing']['cpu'].quit()
        self.main['tabs']['processing']['cpu'].wait()
        self.main['tabs']['processing']['cpu'].start() 
        '''
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
        tmp['tabsConfig']=self.main['tabsConfig']
        tmp['useLogger']=self.main['useLogger']

        print(tmp)
        with open(os.path.join(self.main['config']['dir'],self.main['config']['startup']),'w') as cfg:
            json.dump(tmp,cfg)

