import sys
 
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
import matplotlib as mpl
import gc
import random

class PlotCanvas(FigureCanvas,QtCore.QCoreApplication): 
    axes=None
    finished=QtCore.pyqtSignal()

    def __init__(self, parent=None,fmt='r-',bg='w',glen=25,title='',gridColor=None,edgeColor='g', width=3, height=1, dpi=40,data=None,ylabel='% Used',xlabel='Interval',ylim=100):
        #        self.fig = plt.figure(figsize=(width, height), dpi=dpi,facecolor=bg)
        
        self.callback=None    
        #self.fig=None
        self.axes=None
        
        self.data=None
        self.title=None
        self.fmt=None
        self.glen=None
        self.bg=None
        self.gridColor=None

        if gridColor != None:
            mpl.rcParams['text.color']=gridColor
            mpl.rcParams['axes.labelcolor']=gridColor
            mpl.rcParams['xtick.color']=gridColor
            mpl.rcParams['ytick.color']=gridColor
            mpl.rcParams['font.size']=20


        self.fig = plt.figure(figsize=(width, height), dpi=dpi,facecolor=bg)
 
        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.setMinimumHeight(self,200)
        FigureCanvas.updateGeometry(self)
        self.plot(
                data=data,
                title=title,
                glen=glen,
                fmt=fmt,
                bg=bg,
                gridColor=gridColor,
                ylim=100,
                ylabel=ylabel,
                xlabel=xlabel,
                )

    def plot(self,data,title,glen,fmt='r-',bg='w',gridColor=None,ylim=100,ylabel='% Used',xlabel='Interval'):
        #print(len(data))
        if self.axes != None:
            self.axes.remove() 
            self.axes=None
            self.fig.clf()
            plt.close()
            gc.collect()
            
            #QtWidgets.QApplication.processEvents()
        self.fig.set_facecolor(bg)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_facecolor(bg)
        self.axes.plot(data, fmt)
        self.axes.set_xlim(0,glen)
        self.axes.set_ylim(0,ylim)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.grid(color=gridColor)
        self.draw()
        self.update()
        self.flush_events()
