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
import temperature_widget

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
        me.dialogs={}
        me.obj={}
        #work this data into network tab thread
        me.iconPath='usr/share/hydrogenous/icons'
        me.timer.timeout.connect(lambda: me.updateData(me.parent,k=me.name))
        if psutil.sensors_temperatures() not in [None,{}]:                    
            #prefill
            local=psutil.sensors_temperatures()
            for key in local.keys():
                for element in local[key]:
                    me.dialogs[key+element.label]=QtWidgets.QDialog(me.parent)
                    me.obj[key+element.label]=temperature_widget.Ui_temperature()
                    me.obj[key+element.label].setupUi(me.dialogs[key+element.label])
                    me.obj[key+element.label].label.setText(element.label)
                    me.obj[key+element.label].hardware.setText(key)
                    me.obj[key+element.label].current.display(element.current)
                    me.obj[key+element.label].high.display(element.high)
                    me.obj[key+element.label].critical.display(element.critical)
                    print(element,'sub_element,key')          
            me.gridWidget(parent)

    def update_temp(me,self):
        local=self.data_sig['sensors']['temperatures']
        if local not in [None,{}]:                    
            for key in local.keys():
                for element in local[key]:
                    #me.obj[key+element.label].label.setText(element.label)
                    #me.obj[key+element.label].hardware.setText(key)
                    me.obj[key+element.label].current.display(element.current)
                    me.obj[key+element.label].high.display(element.high)
                    me.obj[key+element.label].critical.display(element.critical)
                    QtWidgets.QApplication.processEvents()
 
    def gridWidget(me,self):
        for num,key in enumerate(me.dialogs.keys()):
            self.temperature_grid.addWidget(me.dialogs[key],num,0,1,1)

    def run(self):
        try:
            if psutil.sensors_temperatures() not in [None,{}]:
                self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        self.exec_()

    def update_widget(me,self):
        me.update_temp(self)

    def updateData(me,self,k=None,noStatPrint=False):
        if 'sensors' in self.data_sig.keys():
            if 'temperatures' in self.data_sig['sensors'].keys():
                tabIndex=self.tabWidget.currentIndex()
                tabText=self.tabWidget.tabText(tabIndex)
                if self.tabWidget.tabText(self.tabWidget.currentIndex()).lower() == 'sensors':
                    if self.sensors_tabs.tabText(self.sensors_tabs.currentIndex()).lower() == 'temp':
                        me.update_widget(self)
            else:
                print('missing data key "temperatures"')
        else:
            print('missing data key "sensors"')
