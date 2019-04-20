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

class grapher(QtCore.QObject):
    #anything that updates the GUI should go in here so define_timer() can be called to run the timers
    sig=QtCore.pyqtSignal()
    err=QtCore.pyqtSignal(tuple)
    def __init__(me,name,mainCopy,parent,mode,thread=None):
        #QtCore.QThread.__init__(me,parent)
        super(me.__class__, me).__init__(thread)
        me.main=mainCopy
        me.parent=parent
        me.name=name
        me.mode=mode
        me.timer=QtCore.QTimer()
        #me.timer.moveToThread(me)
        me.QUIT=False
        #work this data into network tab thread
        me.timer.timeout.connect(lambda: me.updateData(me.parent,k=me.name))
        me.data=[0 for i in range(me.main['graphSize'])]
        me.old=me.data
        me.ylimit=1024
        ylimit=sorted(me.data)[-1]
        me.tool=canvas2.PlotCanvas(
                data=me.data,
                title='{} - {}'.format(me.name.upper(),mode),
                fmt=me.main['line-fmt']['current'],
                glen=me.main['graphSize'],
                bg=me.main['facecolor']['current'],
                #ylabel='Speed (Bps)',
                ylim=1024**2
                )
        me.graph=me.tool.graph
        me.gridWidget(parent)
        me.run()

    def gridWidget(me,self):
        currentRows=self.disk_monitor.rowCount()
        myRow=currentRows+1

        self.disk_monitor.addWidget(me.graph,myRow,0,1,1)

    def run(self):
        try:
            self.timer.start(self.main['interval'])
            self.err.emit(())    
        except Exception as e:
            self.err.emit((e,))
        #self.exec_()
        #loop=QtCore.QEventLoop()
        #loop.exec_

    def update_buffer(me,self):
        #print(self.data_sig['disk']['speed'][me.name][me.mode],me.mode,me.name)
        if me.name in self.data_sig['disk']['speed'].keys():
            d=self.data_sig['disk']['speed'][me.name][me.mode]
            me.data.append(d)
            glen=self.main['graphSize']
            buffer_end=glen*-1
            me.data=me.data[buffer_end:]
            #print(me.data,me.name,me.mode)
            try:
                me.graph.show()
            except Exception as e:
                print(e)
                me.quit()
                me.wait()
        else:
            #me.quit()
            #me.wait()
            me.graph.hide()
            #need to delete this thread and its widget
            #collector should create new widgets based on what is provided

    def stop(me,self):
        self.disk_monitor.removeWidget(me.graph)
        me.QUIT=True
        #me.timer.stop()
        me.graph.deleteLater()
        me.quit()
        me.wait()

    def update_grid(me,self):
        #print(me.data,me.name)
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
            ylabel='Speed',
            )
        else:
            me.stop(self)
            print('data for "{}" has not changed... not painting new plot'.format(me.name))
        me.old=me.data
        me.sig.emit()
        
    def update_titles(me,self):
        me.box.setTitle('{} {}%'.format(me.name.upper(),str(self.data_sig['total'][me.name])))

    def quit(me):
        me.timer.stop()

    def wait(me):
        pass

    def start(me):
        me.timer.start(me.parent.main['interval'])

    def updateData(me,self,k=None,noStatPrint=False):
        if me.QUIT == False:
            if 'disk' in self.data_sig.keys():
                tabIndex=self.tabWidget.currentIndex()
                tabText=self.tabWidget.tabText(tabIndex)
                #print(self.data_sig['total'][me.name])
                me.update_buffer(self)
                #me.update_titles(self)
                if tabText.lower() == 'disk':
                    if self.disk_sub.tabText(self.disk_sub.currentIndex()).lower() == 'monitor':
                        me.update_grid(self)
                        #print('disk monitor tab')
            else:
                print('missing data key "disk"')
        else:
            me.quit()
            #me.wait()
            #me.timer.moveToThread(me)
            #me.timer.stop()
