from PyQt5 import QtWidgets,QtGui,QtCore
import os,sys,json
import psutil,copy
import engineering_notation as en
#from hurry.filesize import si,size,iec
import hurry.filesize
lib=('lib','lib_widget')
for i in lib:
    sys.path.append(i)

import rsrc,canvas,resource
import canvas2
from PyQt5.QtCore import pyqtSlot
import time
class grapher(QtCore.QObject):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent,thread=None):
        #QtCore.QThread.__init__(me,parent)
        super(me.__class__,me).__init__(thread)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.timer=QtCore.QTimer()
        #me.timer.moveToThread(me)
        me.timer.timeout.connect(me.updateData)
        me.data=[0 for i in range(me.parent.main['graphSize'])]
        me.old=me.data
        me.tool=canvas2.PlotCanvas(
                data=me.data,
                title='{}'.format(me.name.upper()),
                fmt=me.main['line-fmt']['current'],
                glen=me.main['graphSize'],
                bg=me.main['facecolor']['current'],
                ylabel='% Used',
                xlabel='Interval',
                )
        me.graph=me.tool.graph
        '''
        me.graph=canvas.PlotCanvas(
                data=me.data,
                title='{}'.format(me.name.upper()),
                fmt=me.main['line-fmt']['current'],
                glen=me.main['graphSize'],
                bg=me.main['facecolor']['current'],
                gridColor=me.main['gridColor']['current'],
                ylabel='% Used',
                xlabel='Interval',
                )
        '''
        me.gridWidget(me.parent)
        me.boxWidget(me.parent)
        me.run()
        
    def gridWidget(me,self):
        match=me.parent.tabWidget.findChildren(
                QtWidgets.QGridLayout,
                me.name,
                QtCore.Qt.FindChildrenRecursively)
        me.grid=None
        if match != None:
            for i in match:
                if i.objectName() == me.name:
                    me.grid=i
            if me.grid != None and type(me.grid) == type(QtWidgets.QGridLayout()):
                me.grid.addWidget(me.graph,0,0,1,1)
            else:
                print('no QtWidgets.QGridLayout() to attach me.grid to')
        else:
            print('no QtWidgets.QGridLayout() to attach me.grid to')

    def boxWidget(me,self):
        boxname='_'.join([me.name.split('_')[0],'box'])
        title='{} {}%'.format(me.name.upper(),0)

        if 'total' in me.parent.data_sig.keys():        
            title='{} {}%'.format(me.name.upper(),str(self.data_sig['total'][k]))

        me.box=None
        match=self.tabWidget.findChildren(
                QtWidgets.QGroupBox,
                boxname,
                QtCore.Qt.FindChildrenRecursively)
        if match != None:
            for i in match:
                if i.objectName() == boxname:
                    me.box=i
            if me.box != None and type(me.box) == type(QtWidgets.QGroupBox()):
                me.box.setTitle(title)
            else:
                print('no QtWidgets.QGroupBox() set title for: {}'.format(boxname))
        else:
            print('no QtWidgets.QGroupBox() set title for: {}'.format(boxname))

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
    def stop(me):
        me.timer.stop()

    def start(me):
        me.timer.start(me.parent.main['interval'])

    def update_buffer(me,self):
        if len(me.data) < self.main['graphSize']:
            tmp=[0 for i in range(self.main['graphSize']-len(me.data))]
            tmp.extend(me.data)
            me.data=tmp
        me.data.append(self.data_sig['total'][me.name])
        glen=self.main['graphSize']
        buffer_end=glen*-1
        me.data=me.data[buffer_end:]

    def update_grid(me,self):
        
        if me.old != me.data:  
            #was me.graph.plot
            me.tool.Plot(
            data=me.data,
            title='{}'.format(''.join(me.name.upper())),
            fmt=me.main['line-fmt']['current'],
            glen=me.main['graphSize'],
            bg=me.main['facecolor']['current'],
            ylabel='% Used',
            xlabel='Interval',
            ylim=100,
            )
        else:
            print('data for "{}" has not changed... not painting new plot'.format(me.name))
        me.old=me.data
        me.sig.emit()
                
    def update_titles(me,self):
        if me.name in ['ram_percent','swap_percent']:
            if me.name == 'ram_percent':
                val=psutil.virtual_memory().used
            if me.name == 'swap_percent':
                val=psutil.swap_memory().used
            me.box.setTitle(
                '{} {}% - {}'.format(
                        me.name.upper(),
                        str(self.data_sig['total'][me.name]),
                        hurry.filesize.size(
                        val,
                        system=hurry.filesize.iec
                    )
                )
            ) 
        elif me.name == 'cpu':
            me.box.setTitle(
                '{} {}% - {}'.format(
                        me.name.upper(),
                        str(self.data_sig['total'][me.name]),
                        psutil.cpu_count(),
                )
            )

    @pyqtSlot()
    def updateData(me,k=None,noStatPrint=False):
        self=me.parent
        k=me.name
        if 'total' in self.data_sig.keys():
            #print(self.data_sig['total'][me.name])
            tabIndex=self.tabWidget.currentIndex()
            tabText=self.tabWidget.tabText(tabIndex)
            me.update_buffer(self)
            me.update_titles(self)
            if tabText.lower() == 'processing':
                me.update_grid(self)
                print(tabText.lower(),time.ctime(),me.name)
                QtWidgets.QApplication.processEvents()
            me.sig.emit()
        else:
            print('missing data key "total"')
