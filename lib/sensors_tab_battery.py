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
import battery_widget

class grapher(QtCore.QThread,QtCore.QCoreApplication):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)

    def secs2hours(me,secs):
        mm, ss = divmod(secs, 60)
        hh, mm = divmod(mm, 60)
        return "%d:%02d:%02d" % (hh, mm, ss)

    def __init__(me,name,mainCopy,parent):

        QtCore.QThread.__init__(me,parent)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.timer=QtCore.QTimer()
        me.timer.moveToThread(me)
        #work this data into network tab thread
        me.iconPath='usr/share/hydrogenous/icons'
        me.timer.timeout.connect(lambda: me.updateData(me.parent,k=me.name))
        if psutil.sensors_battery() != None:        
            me.dialog=QtWidgets.QDialog(me.parent)         
            me.graph=battery_widget.Ui_battery_widget()
            me.graph.setupUi(me.dialog)

            me.battery_icon=QtGui.QPixmap(os.path.join(me.iconPath,'battery.png')).scaled(25,50,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)

            me.plugged_icon=QtGui.QPixmap(os.path.join(me.iconPath,'plugged-in.png')).scaled(25,50,QtCore.Qt.KeepAspectRatio,QtCore.Qt.FastTransformation)
            
            me.percent=psutil.sensors_battery().percent
            me.secsleft=psutil.sensors_battery().secsleft
            if me.secsleft == psutil.POWER_TIME_UNLIMITED:
                tmp='Charging'
            else:
                tmp=me.secs2hours(me.secsleft)
            me.power_plugged=psutil.sensors_battery().power_plugged
            me.graph.time_left.setDigitCount(len(tmp))        
            me.graph.time_left.display(tmp)
            me.graph.battery_level.setValue(round(me.percent,0))

            if me.power_plugged == True:
                me.graph.plugged_in.setPixmap(me.plugged_icon)
            else:
                me.graph.plugged_in.setPixmap(me.battery_icon)
            
            me.gridWidget(parent)
        
    def gridWidget(me,self):
        self.battery_grid.addWidget(me.dialog,0,0,1,1)

    def run(self):
        try:
            if psutil.sensors_battery() != None:
                self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        self.exec_()

    def update_widget(me,self):
        #create an easter egg for april fools where the battery lcd counts down to zero from 2hours
        #the battery level progress bar will display text alongside the batter level "HDD/SDD Reformat CountDown in Progress!"
        #include a lib/ file for display with the potential to actually be used for malicious intent
        #including a dialog to get admin password for elevated privileges for a reformat
        if self.data_sig['sensors']['battery'] != None:
            if self.data_sig['sensors']['battery'].percent != me.percent:
                me.graph.battery_level.setValue(round(self.data_sig['sensors']['battery'].percent,0))
            if self.data_sig['sensors']['battery'].secsleft != me.secsleft:
                if self.data_sig['sensors']['battery'].secsleft != psutil.POWER_TIME_UNLIMITED:
                    tmp=me.secs2hours(self.data_sig['sensors']['battery'].secsleft)
                else:
                    tmp='Charging'
                me.graph.time_left.setDigitCount(len(tmp))
                me.graph.time_left.display(tmp)

            if self.data_sig['sensors']['battery'].power_plugged != me.power_plugged:
                if self.data_sig['sensors']['battery'].power_plugged == True:
                    me.graph.plugged_in.setPixmap(me.plugged_icon)
                else:
                    me.graph.plugged_in.setPixmap(me.battery_icon)

            #print(self.data_sig['sensors']['battery'])
            me.percent=self.data_sig['sensors']['battery'].percent
            me.secsleft=self.data_sig['sensors']['battery'].secsleft
            me.power_plugged=self.data_sig['sensors']['battery'].power_plugged

    def updateData(me,self,k=None,noStatPrint=False):
        if 'sensors' in self.data_sig.keys():
            if 'battery' in self.data_sig['sensors'].keys():
                tabIndex=self.tabWidget.currentIndex()
                tabText=self.tabWidget.tabText(tabIndex)
                #print(self.data_sig['total'][me.name])
                #me.update_buffer(self)
                #me.update_titles(self)
                #if tabText.lower() == 'disk':
                #    if self.disk_sub.tabText(self.disk_sub.currentIndex()).lower() == 'monitor':
                #        me.update_grid(self)
                if self.tabWidget.tabText(self.tabWidget.currentIndex()).lower() == 'sensors':
                    if self.sensors_tabs.tabText(self.sensors_tabs.currentIndex()).lower() == 'battery':
                        me.update_widget(self)
        else:
            print('missing data key "disk"')
