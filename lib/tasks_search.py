from PyQt5 import QtGui,QtWidgets,QtCore
import gc
#import objgraph
#from pympler.tracker import SummaryTracker
#tracker = SummaryTracker()
import psutil
class threaded_search(QtCore.QObject):
    sig=QtCore.pyqtSignal()
    sigUpd8=QtCore.pyqtSignal()   
    def __init__(me,self):
        super(me.__class__,me).__init__()
        me.parent=self
        me.timer=QtCore.QTimer()

        #me.sigUpd8.connect(me.tasks_search_update)

        me.tasks_search_init(self)
        me.timer.timeout.connect(me.tasks_search_update)
        #me.timer.start(self.main['interval'])

    def quit(me):
        me.timer.stop()

    def wait(me):
        pass

    def stop(me):
        me.timer.stop()

    def start(me):
        me.timer.start(me.parent.main['interval'])

    @QtCore.pyqtSlot()
    def tasks_search_update(me):
        #tracker.print_diff()
        #objgraph.show_most_common_types(limit=20)
        self=me.parent 
        #search model for specific process to get item
        #get row num from item to get column items
        #create iterable for insertion into discovered_tasks
        count=self.main['tasks']['model'].rowCount()
        desired=self.process_search.text()
        col=1
        if self.searchOption_name.isChecked():
            col=0
        elif self.searchOption_pid.isChecked():
            col=1
        elif self.searchOption_user.isChecked():
            col=2
        elif self.searchOption_cpu.isChecked():
            col=3
        elif self.searchOption_ram.isChecked():
            col=4
        for i in range(0,count):
            w=self.main['tasks']['model'].item(i,column=col)
            if w != None:
                if me.modeOfSearch(self,w.text(),desired) == True:
                    #check for dups
                    r=[]
                    for ii in range(self.main['tasks']['model'].columnCount()):
                        r.append(QtGui.QStandardItem(self.main['tasks']['model'].item(w.row(),ii).text()))
                    init=[False,self.main['tasks_search']['model'].rowCount()]
                    #print(r)
                    for pid in range(self.main['tasks_search']['model'].rowCount()):
                        init=[False,pid]
                        a=self.main['tasks_search']['model'].item(pid,1)
                        if a != None:
                            if me.modeOfSearch(self,a.text(),r[1].text()) == True:
                                self.main['tasks_search']['model'].removeRow(init[1])
                    if init[0] != False:
                        self.main['tasks_search']['model'].removeRow(init[1])
                    self.main['tasks_search']['model'].insertRow(init[1],r)
                    del(r)
        count=self.main['tasks_search']['model'].rowCount()
        for pid_num in range(count):
            w=self.main['tasks_search']['model'].item(pid_num,1) 
            if w != None:
                PID=int(w.text())
                try:
                    psutil.Process(PID)
                except Exception as e:
                    print(e)
                    self.main['tasks_search']['model'].removeRow(pid_num)
        gc.collect() 
        
    def tasks_search_init(me,self):
        self.discovered_tasks.setModel(self.main['tasks_search']['proxy'])
        self.discovered_tasks.setAutoScroll(False)
        self.discovered_tasks.setSortingEnabled(True)
        self.discovered_tasks.setWordWrap(False)
        self.discovered_tasks.sortByColumn(3,1)
        self.discovered_tasks.setEditTriggers(QtWidgets.QTableView.NoEditTriggers) 

        self.searchOption_name.toggled.connect(me.setTasksSearchClear)
        self.searchOption_pid.toggled.connect(me.setTasksSearchClear)
        self.searchOption_user.toggled.connect(me.setTasksSearchClear)
        self.searchOption_cpu.toggled.connect(me.setTasksSearchClear)
        self.searchOption_ram.toggled.connect(me.setTasksSearchClear)
        self.process_search.textChanged.connect(me.setTasksSearchClear)
        self.searchFuzzy.toggled.connect(me.setTasksSearchClear)
        self.searchExact.toggled.connect(me.setTasksSearchClear)

    def setTasksSearchClear(me,sig):
        self=me.parent
        self.main['tasks_search']['model'].clear()
        self.main['tasks_search']['model'].setHorizontalHeaderLabels(self.main['tasks']['labels'])
    
    def modeOfSearch(me,self,obj,desired):
            #print(obj,desired)
            if self.searchFuzzy.isChecked():
                if desired in obj and desired != '':
                    #print('fuzzy search')
                    return True
            elif self.searchExact.isChecked():
                if desired == obj and desired != '':
                    #print('exact search')
                    return True
            return False


