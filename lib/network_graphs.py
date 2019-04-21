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
from PyQt5.QtCore import pyqtSlot

class grapher(QtCore.QObject):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent,mode,thread=None):
        #QtCore.QThread.__init__(me,parent)
        super(me.__class__,me).__init__(thread)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.mode=mode
        me.timer=QtCore.QTimer()
        #me.timer.moveToThread(me)
        #work this data into network tab thread
        me.timer.timeout.connect(me.updateData)
        me.data=[0 for i in range(me.main['graphSize'])]
        me.old=me.data
        me.ylimit=1024
        me.tool=canvas2.PlotCanvas(
                data=me.data,
                title='{} - {}'.format(me.name.upper(),mode),
                fmt=me.main['line-fmt']['current'],
                glen=me.main['graphSize'],
                bg=me.main['facecolor']['current'],
                ylabel='Speed (Bps)',
                ylim=1024
                )
        me.graph=me.tool.graph

        ylimit=sorted(me.data)[-1]
        '''
        me.graph=canvas.PlotCanvas(
                data=me.data,
                title='{} - {}'.format(me.name.upper(),mode),
                fmt=me.main['line-fmt']['current'],
                glen=me.main['graphSize'],
                bg=me.main['facecolor']['current'],
                gridColor=me.main['gridColor']['current'], 
                ylabel='Speed (Bps)',
                ylim=1024
                )
        '''
        me.gridWidget(parent)
        me.run()

    def gridWidget(me,self):
        currentRows=self.net.rowCount()
        myRow=currentRows+1

        self.net.addWidget(me.graph,myRow,0,1,1)

    def run(self):
        try:
            self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        #self.exec_()
        #loop=QtCore.QEventLoop()
        #loop.exec_

    def quit(me):
        me.timer.stop()

    def wait(me):
        pass

    def start(me):
        me.timer.start(me.parent.main['interval'])

    def update_buffer(me,self):
        d=self.data_sig['net']['speed'][me.name][me.mode]
        me.data.append(d)
        glen=self.main['graphSize']
        buffer_end=glen*-1
        me.data=me.data[buffer_end:]
        #print(me.data,me.name,me.mode)

    def update_grid(me,self):
        if me.old != me.data:
            ylimit=sorted(me.data)[-1]
            if me.ylimit > ylimit:
                ylimit=me.ylimit
            me.tool.Plot(
            data=me.data,
            title='{} - {}'.format(''.join(me.name.upper()),me.mode),
            fmt=me.main['line-fmt']['current'],
            glen=me.main['graphSize'],
            bg=me.main['facecolor']['current'],
            ylim=ylimit,
            ylabel='Speed (Bps)',
            )
        else:
            print('data for "{}" has not changed... not painting new plot'.format(me.name))
        me.old=me.data
        me.sig.emit()
        
    def update_titles(me,self):
        me.box.setTitle('{} {}%'.format(me.name.upper(),str(self.data_sig['total'][me.name])))

    @pyqtSlot()
    def updateData(me,k=None,noStatPrint=False):
        self=me.parent
        k=me.name
        if 'net' in self.data_sig.keys():
            tabIndex=self.tabWidget.currentIndex()
            tabText=self.tabWidget.tabText(tabIndex)
            #print(self.data_sig['total'][me.name])
            me.update_buffer(self)
            #me.update_titles(self)
            if tabText.lower() == 'network':
                if self.net_sub.tabText(self.net_sub.currentIndex()).lower() == 'monitor':
                    me.update_grid(self)
            me.sig.emit()
        else:
            print('missing data key "net"')
