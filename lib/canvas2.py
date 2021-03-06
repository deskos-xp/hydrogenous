import sys
 
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore 

import gc
import random
import pyqtgraph as pg
import time
class PlotCanvas(): 
    axes=None
    finished=QtCore.pyqtSignal()

    def __init__(self, parent=None,fmt='r',bg='w',glen=25,title='', width=3, height=1, dpi=40,data=None,ylabel='% Used',xlabel='Interval',ylim=100):
        self.parent=parent
        pg.setConfigOption('foreground','w')
        self.GRAPH=pg.PlotWidget(title=title)
        self.title=title
        self.GRAPH.setBackground(pg.mkColor(bg)) 
        self.GRAPH.setAntialiasing(False)

        self.GRAPH.showGrid(True,True)
        #print([i for i in dir(self.GRAPH.items)])
        #allow zooming, need to move to config
        self.GRAPH.setMouseEnabled(x=False,y=False)
        self.GRAPH.useOpenGL()
        #self.GRAPH.setLimits(yMin=0,xMax=len(data),xMin=0)
        #self.GRAPH.setLimits(yMax=4*(sorted(data)[-1]))
        self.graph=QtWidgets.QFrame(parent)
        self.graph.setMinimumHeight(200)
        self.grid=QtWidgets.QGridLayout(parent)
        self.graph.setLayout(self.grid)
        self.grid.addWidget(self.GRAPH,0,0,1,1)
        self.plt=self.GRAPH.plot(y=data,pen=pg.mkPen(pg.mkColor(fmt),width=1))

    def Plot(self,data,title,glen,fmt='r-',bg='w',gridColor=None,ylim=100,ylabel='% Used',xlabel='Interval'): 
        #self.GRAPH.setLimits(xMax=len(data))
        #self.GRAPH.autoRange(padding=10)
        self.GRAPH.setBackground(pg.mkColor(bg)) 
        #'{} - {}'.format(title,sorted(data)[-1])
        self.GRAPH.setBackground(pg.mkColor(bg)) 
        self.plt.setData(data,pen=pg.mkPen(pg.mkColor(fmt),width=1)) 
        self.plt.informViewBoundsChanged()
        #self.GRAPH.updateGeometry()
        #self.plt.update()
        #QtWidgets.QApplication.processEvents() 
