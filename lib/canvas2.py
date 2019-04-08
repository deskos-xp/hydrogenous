import sys
 
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore 

import gc
import random
import pyqtgraph as pg

class PlotCanvas(): 
    axes=None
    finished=QtCore.pyqtSignal()

    def __init__(self, parent=None,fmt='r',bg='w',glen=25,title='', width=3, height=1, dpi=40,data=None,ylabel='% Used',xlabel='Interval',ylim=100):
        pg.setConfigOption('foreground','w')
        self.GRAPH=pg.PlotWidget(title=title)
        self.GRAPH.setBackground(pg.mkColor(bg)) 
        self.GRAPH.setAntialiasing(False)

        self.GRAPH.showGrid(True,True)
        #print([i for i in dir(self.GRAPH.items)])
        #allow zooming, need to move to config
        self.GRAPH.setMouseEnabled(x=False,y=False)
        self.GRAPH.setLimits(yMax=ylim,yMin=0,xMax=len(data),xMin=0)

        self.graph=QtWidgets.QFrame(parent)
        self.graph.setMinimumHeight(200)
        grid=QtWidgets.QGridLayout(parent)
        self.graph.setLayout(grid)
        grid.addWidget(self.GRAPH,0,0,1,1)
        self.plt=self.GRAPH.plot(y=data,pen=pg.mkPen(pg.mkColor(fmt),width=1))

    def Plot(self,data,title,glen,fmt='r-',bg='w',gridColor=None,ylim=100,ylabel='% Used',xlabel='Interval'):
        self.GRAPH.setLimits(yMax=ylim,xMax=len(data))
        self.GRAPH.setBackground(pg.mkColor(bg)) 
       
        self.plt.setData(data,pen=pg.mkPen(pg.mkColor(fmt),width=1)) 
