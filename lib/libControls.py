#! /usr/bin/python3

from PyQt5 import QtWidgets,QtCore,QtGui
import os,json
import time
import psutil
import subprocess as sp
import sudoBox
class control(QtCore.QObject):
    def __init__(me,self):
        super(me.__class__,me).__init__()
        me.parent=self
        me.actors(self)
        me.buttons(self)
        me.valueChanged(self)
        me.spinBoxes(self)


    def spinBoxes(me,self):
        spins=[
            [
                self.main['renice_obj'].pid,
                me.valueChange_spin
            ],
            [
                self.main['renice_obj'].nice,
                me.valueChange_spin
            ],
        ]
        for s in spins:
            s[0].valueChanged.connect(lambda sig,value=s[0]:s[1](sig,value))

    def valueChange_spin(self,sig,value):
        if value.objectName() == 'pid':
            try:
                proc=psutil.Process(value.value())
                self.parent.main['renice_obj'].name.setText('[{}]-[{}]'.format(proc.name(),proc.cmdline()))
                self.parent.main['renice_obj'].nice.setValue(proc.nice())
            except Exception as e:
                proc=0
                print(e)

    def tab_changed(me,self):
        me.stop_all_timers(me.parent)
        me.start_tab_timer(self,tab=me.parent.tabWidget.tabText(me.parent.tabWidget.currentIndex()))
        self.tabWidget.currentChanged.connect(me.tabChanged)
     
    def tabChanged(me,sig):
        me.stop_all_timers(me.parent)
        me.start_tab_timer(me.parent,tab=me.parent.tabWidget.tabText(me.parent.tabWidget.currentIndex()))
        
        tab=me.parent.tabWidget.tabText(sig)
        if tab == 'Processes':
            subTab=me.parent.tabWidget_4.tabText(me.parent.tabWidget_4.currentIndex())
            if subTab == 'All':
               me.parent.tasks.setFocus()
            elif subTab == 'Search':
                me.parent.discovered_tasks.setFocus()
        elif tab == 'Processing':
            me.parent.processing.setFocus()
        elif tab == 'Disk':
            me.parent.disk_sub.setFocus()
        elif tab == 'Network':
            me.parent.net_sub.setFocus()
        elif tab == 'Sensors':
            me.parent.sensors_tabs.setFocus()
        elif tab == 'Settings':
            me.parent.interval.setFocus()

    def start_tab_timer(me,self,tab='Processing'):
        self.main['collector']['thread_obj'].timer.start(self.main['interval'])
        tab=tab.lower()
        print('currentTab: {}'.format(tab))
        if 'disk_timer' in self.main.keys(): 
            self.main['disk_timer'].stop()
        for i in self.main['tabs'].keys(): 
            if type(self.main['tabs'][i]) == type(dict()):
                for ii in self.main['tabs'][i].keys():
                    if type(self.main['tabs'][i][ii]) == type(dict()): 
                        for iii in self.main['tabs'][i][ii].keys():
                            if type(self.main['tabs'][i][ii][iii]) != type(QtCore.QThread()):
                                #print(self.main['tabs'][i][ii][iii],'obj')
                                if 'timer' in dir(self.main['tabs'][i][ii][iii]):
                                    if tab in i:
                                        self.main['tabs'][i][ii][iii].timer.start(self.main['interval'])
                    else:
                        if type(self.main['tabs'][i][ii]) != type(QtCore.QThread()):
                            if 'timer' in dir(self.main['tabs'][i][ii]):
                                if tab in i:
                                    self.main['tabs'][i][ii].timer.start(self.main['interval'])
            else:
                if type(self.main['tabs'][i]) != type(QtCore.QThread()):
                    if 'timer' in dir(self.main['tabs'][i]):
                        if tab in i:
                            self.main['tabs'][i].timer.start(self.main['interval'])
        if tab == 'processes':             
            self.main['tasks_search_obj'].start()

    def stop_all_timers(me,self):
        self.main['collector']['thread_obj'].timer.stop()
        if 'disk_timer' in self.main.keys():
            self.main['disk_timer'].stop()
        for i in self.main['tabs'].keys(): 
            if type(self.main['tabs'][i]) == type(dict()):
                for ii in self.main['tabs'][i].keys():
                    if type(self.main['tabs'][i][ii]) == type(dict()): 
                        for iii in self.main['tabs'][i][ii].keys():
                            if type(self.main['tabs'][i][ii][iii]) != type(QtCore.QThread()):
                                #print(self.main['tabs'][i][ii][iii],'obj')
                                if 'timer' in dir(self.main['tabs'][i][ii][iii]):
                                    try:
                                        self.main['tabs'][i][ii][iii].stop()
                                    except:
                                        self.main['tabs'][i][ii][iii].quit()
                    else:
                        if type(self.main['tabs'][i][ii]) != type(QtCore.QThread()):
                            if 'timer' in dir(self.main['tabs'][i][ii]):
                                try:
                                    self.main['tabs'][i][ii].stop()
                                except:
                                    self.main['tabs'][i][ii].quit()
            else:
                if type(self.main['tabs'][i]) != type(QtCore.QThread()):
                    if 'timer' in dir(self.main['tabs'][i]):
                        try:
                            self.main['tabs'][i].stop()
                        except:
                            self.main['tabs'][i].quit()

    def start_all_threads(me,self):
        for i in self.main['tabs'].keys():
            if type(self.main['tabs'][i]) == type(dict()):
                for x in self.main['tabs'][i].keys():
                    if i not in ['network']:
                        if x not in ['gateway_setup',]:
                            if i in ['processing','network_info','network_info_obj','disk_info','disk_info_obj','sensors']:
                                self.main['tabs'][i][x].quit()
                                self.main['tabs'][i][x].wait()
                                self.main['tabs'][i][x].start()
                            else:
                                #print(i,x)
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
        
        self.main['disk_timer'].setInterval(self.main['interval'])
        self.logger_handler(reset=True)
        self.main['disk_timer'].start()
        self.main['collector']['thread_obj'].timer.stop()
        #self.main['collector']['thread_obj'].timer.start(self.main['interval'])
 
    def handle_threads(me,self,sig):
        caller=self.sender()
        me.stop_all_timers(self)
        me.start_tab_timer(me.parent,tab=me.parent.tabWidget.tabText(me.parent.tabWidget.currentIndex()))
        self.main['collector']['thread_obj'].timer.start(self.main['interval'])

        #me.start_all_threads(self)
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

    @QtCore.pyqtSlot()
    def preQuit_calls(me):
        secs=2
        msg='user called quit...sleeping for {}s while threads quit.'.format(secs)
        print(msg)
        time.sleep(secs)


    def quit(me,self):
        QtWidgets.QApplication.quit()
        
    def actors(me,self):
        self.actionQuit.triggered.connect(lambda: me.quit(self))
        self.tasks.clicked.connect(lambda sig: me.tasks_clicked(self,sig))        
        #self.aboutToQuit.connect(me.preQuit_calls)
        #QtWidgets.QApplication.aboutToQuit.connect(me.preQuit_calls)
        QtCore.QCoreApplication.instance().aboutToQuit.connect(me.preQuit_calls)

    def lateLoad(me,self):
        self.tasks.clicked.connect(lambda sig: me.tasks_clicked(self,sig))        
        self.deselect_all.clicked.connect(lambda: me.clear(self,self.tasks))
        me.tab_changed(self)

    def buttons(me,self):
        self.intervalSet.clicked.connect(lambda sig: me.saveInterval(self,sig))
        self.setGraphSize.clicked.connect(lambda: me.saveGraphSize(self))
        self.select_facecolor.clicked.connect(lambda: me.saveFaceColor(self,noLEChange=False))
        self.setLineColor.clicked.connect(lambda: me.saveLineColor(self))
        
        self.deselect_all.clicked.connect(lambda: me.clear(self,self.tasks))
        self.main['renice_obj'].renice_button.clicked.connect(lambda: me.renice(self))

    failCount=3
    def getPass(me,self,attempts_left,mode,signal=None,pid=None):
        def getPass_passwd(me,obj,dialog,parent,self,mode,signal=None,pid=None):
            if pid == None:
                pid=parent.pid.value()
            nice=parent.nice.value()
            passwd=obj.passwd.text()
            cmd=""
            if mode == 'renice':
                cmd=" printf '%s' {2} | sudo -k -S renice {0} {1}".format(nice,pid,passwd)
            if mode == 'send_sig':
                cmd=" printf '%s' {2} | sudo -k -S kill -{0} {1}".format(signal,pid,passwd)
            proc=sp.Popen(cmd,shell=True,stdout=sp.PIPE,stderr=sp.PIPE)
            stdout,err=proc.communicate()
            if b'[sudo] password for carl: \nsudo: no password was provided\n' in err:
                self.statusBar().showMessage(err.decode())
                me.failCount-=1
                if me.failCount > 0:
                    me.getPass(self,me.failCount,'renice',signal,pid)
                else:
                    msg='Too many failed attempts!'
                    print(msg)
                    self.statusBar().showMessage(msg)
                    me.failCount=3
            else:
                self.statusBar().showMessage('Success!')
                me.failCount=3
            
        def getPass_quit(me,obj,dialog):
            me.failCount=3
            dialog.close()    
            dialog.deleteLater()
            del(dialog)
            del(obj)

        dialog=QtWidgets.QDialog(self)
        getPass=sudoBox.Ui_sudoBox()
        getPass.setupUi(dialog)
        getPass.message.setText(getPass.message.text().format(attempts_left))
        getPass.buttonBox.accepted.connect(lambda: getPass_passwd(me,getPass,dialog,self.main['renice_obj'],self,mode=mode,signal=signal,pid=pid))
        getPass.buttonBox.rejected.connect(lambda: getPass_quit(me,getPass,dialog))
        dialog.show()        

    def renice(me,self):
        pid=self.main['renice_obj'].pid.value()
        nice=self.main['renice_obj'].nice.value()
        try:
            proc=psutil.Process(pid)
            proc.nice(value=nice)
        except psutil.AccessDenied as e:
            proc=psutil.Process(pid)
            me.getPass(self,me.failCount,mode='renice')
        except Exception as e:
            msg='Nothing was set: {}'.format(e)
            print(msg)
            self.statusBar().showMessage(msg)
            
        
    def tasks_clicked(me,self,sig):
        #print(sig)
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
            
            '''
            columns=self.main['tasks']['model'].columnCount()
            rowData=' | '.join([str(sig.sibling(sig.row(),i).data()) for i in range(columns)])
            self.statusBar().showMessage('"{}" copied to clipboard'.format(rowData))
            '''
            self.selected_pid=sig.sibling(row,col).data()
            '''
            cb=QtWidgets.QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(rowData,mode=cb.Clipboard)
            '''
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
        tmp['format']=self.main['format']
        tmp['graphSize']=self.main['graphSize']
        tmp['interval']=self.main['interval']
        tmp['line-fmt']=self.main['line-fmt']
        tmp['facecolor']=self.main['facecolor']
        tmp['tabsConfig']=self.main['tabsConfig']
        tmp['useLogger']=self.main['useLogger']
        tmp['dbName']=self.main['dbName']
        tmp['dbTable']=self.main['dbTable']
        tmp['serverAddress']=self.main['serverAddress']
        tmp['serverPort']=self.main['serverPort']
        tmp['serverUser']=self.main['serverUser']

        print(tmp)
        with open(os.path.join(self.main['config']['dir'],self.main['config']['startup']),'w') as cfg:
            json.dump(tmp,cfg)

