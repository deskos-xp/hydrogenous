# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/rsrc.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_rsrc(object):
    def setupUi(self, rsrc):
        rsrc.setObjectName("rsrc")
        rsrc.resize(1055, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("usr/share/hydrogenous/icons/app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        rsrc.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(rsrc)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.processing = QtWidgets.QWidget()
        self.processing.setObjectName("processing")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.processing)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.scrollArea = QtWidgets.QScrollArea(self.processing)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 428, 428))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.swap_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.swap_box.setMinimumSize(QtCore.QSize(200, 200))
        self.swap_box.setObjectName("swap_box")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.swap_box)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.swap_percent = QtWidgets.QGridLayout()
        self.swap_percent.setObjectName("swap_percent")
        self.gridLayout_8.addLayout(self.swap_percent, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.swap_box, 1, 0, 1, 1)
        self.ram_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.ram_box.setMinimumSize(QtCore.QSize(200, 200))
        self.ram_box.setObjectName("ram_box")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.ram_box)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.ram_percent = QtWidgets.QGridLayout()
        self.ram_percent.setObjectName("ram_percent")
        self.gridLayout_10.addLayout(self.ram_percent, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.ram_box, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.cpu_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.cpu_box.setMinimumSize(QtCore.QSize(200, 200))
        self.cpu_box.setObjectName("cpu_box")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.cpu_box)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.cpu = QtWidgets.QGridLayout()
        self.cpu.setObjectName("cpu")
        self.gridLayout_9.addLayout(self.cpu, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.cpu_box, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_7.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.processing, "")
        self.processes = QtWidgets.QWidget()
        self.processes.setObjectName("processes")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.processes)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.tabWidget_4 = QtWidgets.QTabWidget(self.processes)
        self.tabWidget_4.setObjectName("tabWidget_4")
        self.all = QtWidgets.QWidget()
        self.all.setObjectName("all")
        self.gridLayout_45 = QtWidgets.QGridLayout(self.all)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.gridLayout_44 = QtWidgets.QGridLayout()
        self.gridLayout_44.setObjectName("gridLayout_44")
        self.deselect_all = QtWidgets.QPushButton(self.all)
        self.deselect_all.setObjectName("deselect_all")
        self.gridLayout_44.addWidget(self.deselect_all, 1, 0, 1, 1)
        self.tasks = QtWidgets.QTableView(self.all)
        self.tasks.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tasks.setObjectName("tasks")
        self.gridLayout_44.addWidget(self.tasks, 0, 0, 1, 1)
        self.gridLayout_45.addLayout(self.gridLayout_44, 0, 0, 1, 1)
        self.tabWidget_4.addTab(self.all, "")
        self.search = QtWidgets.QWidget()
        self.search.setObjectName("search")
        self.gridLayout_26 = QtWidgets.QGridLayout(self.search)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.frameTasks = QtWidgets.QFrame(self.search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameTasks.sizePolicy().hasHeightForWidth())
        self.frameTasks.setSizePolicy(sizePolicy)
        self.frameTasks.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTasks.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTasks.setObjectName("frameTasks")
        self.gridLayout_40 = QtWidgets.QGridLayout(self.frameTasks)
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.gridLayout_36 = QtWidgets.QGridLayout()
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.discovered_tasks = QtWidgets.QTableView(self.frameTasks)
        self.discovered_tasks.setObjectName("discovered_tasks")
        self.gridLayout_36.addWidget(self.discovered_tasks, 0, 0, 1, 1)
        self.gridLayout_40.addLayout(self.gridLayout_36, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.frameTasks, 0, 1, 1, 1)
        self.frameControls = QtWidgets.QFrame(self.search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameControls.sizePolicy().hasHeightForWidth())
        self.frameControls.setSizePolicy(sizePolicy)
        self.frameControls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameControls.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameControls.setObjectName("frameControls")
        self.gridLayout_35 = QtWidgets.QGridLayout(self.frameControls)
        self.gridLayout_35.setObjectName("gridLayout_35")
        self.gridLayout_28 = QtWidgets.QGridLayout()
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.searchOption_pid = QtWidgets.QRadioButton(self.frameControls)
        self.searchOption_pid.setChecked(True)
        self.searchOption_pid.setObjectName("searchOption_pid")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(rsrc)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.searchOption_pid)
        self.gridLayout_28.addWidget(self.searchOption_pid, 6, 0, 1, 1)
        self.searchOption_user = QtWidgets.QRadioButton(self.frameControls)
        self.searchOption_user.setObjectName("searchOption_user")
        self.buttonGroup_2.addButton(self.searchOption_user)
        self.gridLayout_28.addWidget(self.searchOption_user, 5, 0, 1, 1)
        self.searchOption_ram = QtWidgets.QRadioButton(self.frameControls)
        self.searchOption_ram.setObjectName("searchOption_ram")
        self.buttonGroup_2.addButton(self.searchOption_ram)
        self.gridLayout_28.addWidget(self.searchOption_ram, 2, 0, 1, 1)
        self.searchOption_name = QtWidgets.QRadioButton(self.frameControls)
        self.searchOption_name.setObjectName("searchOption_name")
        self.buttonGroup_2.addButton(self.searchOption_name)
        self.gridLayout_28.addWidget(self.searchOption_name, 4, 0, 1, 1)
        self.searchOption_cpu = QtWidgets.QRadioButton(self.frameControls)
        self.searchOption_cpu.setObjectName("searchOption_cpu")
        self.buttonGroup_2.addButton(self.searchOption_cpu)
        self.gridLayout_28.addWidget(self.searchOption_cpu, 3, 0, 1, 1)
        self.gridLayout_41 = QtWidgets.QGridLayout()
        self.gridLayout_41.setObjectName("gridLayout_41")
        self.searchExact = QtWidgets.QRadioButton(self.frameControls)
        self.searchExact.setObjectName("searchExact")
        self.buttonGroup = QtWidgets.QButtonGroup(rsrc)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.searchExact)
        self.gridLayout_41.addWidget(self.searchExact, 2, 1, 1, 1)
        self.searchFuzzy = QtWidgets.QRadioButton(self.frameControls)
        self.searchFuzzy.setChecked(True)
        self.searchFuzzy.setObjectName("searchFuzzy")
        self.buttonGroup.addButton(self.searchFuzzy)
        self.gridLayout_41.addWidget(self.searchFuzzy, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_41.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_28.addLayout(self.gridLayout_41, 1, 0, 1, 1)
        self.process_search = QtWidgets.QLineEdit(self.frameControls)
        self.process_search.setObjectName("process_search")
        self.gridLayout_28.addWidget(self.process_search, 0, 0, 1, 1)
        self.gridLayout_35.addLayout(self.gridLayout_28, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(self.frameControls, 0, 0, 1, 1)
        self.gridLayout_26.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.tabWidget_4.addTab(self.search, "")
        self.renice = QtWidgets.QWidget()
        self.renice.setObjectName("renice")
        self.gridLayout_43 = QtWidgets.QGridLayout(self.renice)
        self.gridLayout_43.setObjectName("gridLayout_43")
        self.renice_grid = QtWidgets.QGridLayout()
        self.renice_grid.setObjectName("renice_grid")
        self.gridLayout_43.addLayout(self.renice_grid, 0, 0, 1, 1)
        self.tabWidget_4.addTab(self.renice, "")
        self.gridLayout_16.addWidget(self.tabWidget_4, 0, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        self.tabWidget.addTab(self.processes, "")
        self.disk = QtWidgets.QWidget()
        self.disk.setObjectName("disk")
        self.gridLayout_25 = QtWidgets.QGridLayout(self.disk)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.gridLayout_24 = QtWidgets.QGridLayout()
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.disk_sub = QtWidgets.QTabWidget(self.disk)
        self.disk_sub.setObjectName("disk_sub")
        self.info = QtWidgets.QWidget()
        self.info.setObjectName("info")
        self.gridLayout_33 = QtWidgets.QGridLayout(self.info)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.info)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_30 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.disk_info = QtWidgets.QGridLayout()
        self.disk_info.setObjectName("disk_info")
        self.gridLayout_30.addLayout(self.disk_info, 0, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_33.addWidget(self.scrollArea_4, 0, 0, 1, 1)
        self.disk_sub.addTab(self.info, "")
        self.monitor = QtWidgets.QWidget()
        self.monitor.setObjectName("monitor")
        self.gridLayout_31 = QtWidgets.QGridLayout(self.monitor)
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.monitor)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.gridLayout_39 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.disk_monitor = QtWidgets.QGridLayout()
        self.disk_monitor.setObjectName("disk_monitor")
        self.gridLayout_39.addLayout(self.disk_monitor, 0, 0, 1, 1)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_31.addWidget(self.scrollArea_3, 0, 0, 1, 1)
        self.disk_sub.addTab(self.monitor, "")
        self.gridLayout_24.addWidget(self.disk_sub, 0, 0, 1, 1)
        self.gridLayout_25.addLayout(self.gridLayout_24, 0, 0, 1, 1)
        self.tabWidget.addTab(self.disk, "")
        self.network = QtWidgets.QWidget()
        self.network.setObjectName("network")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.network)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.gridLayout_22 = QtWidgets.QGridLayout()
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.net_sub = QtWidgets.QTabWidget(self.network)
        self.net_sub.setObjectName("net_sub")
        self.info1 = QtWidgets.QWidget()
        self.info1.setObjectName("info1")
        self.gridLayout_29 = QtWidgets.QGridLayout(self.info1)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.net_info_grid_t = QtWidgets.QGridLayout()
        self.net_info_grid_t.setObjectName("net_info_grid_t")
        self.scrollArea_8 = QtWidgets.QScrollArea(self.info1)
        self.scrollArea_8.setWidgetResizable(True)
        self.scrollArea_8.setObjectName("scrollArea_8")
        self.scrollAreaWidgetContents_8 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_8.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_8.setObjectName("scrollAreaWidgetContents_8")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_8)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.net_info_grid = QtWidgets.QGridLayout()
        self.net_info_grid.setObjectName("net_info_grid")
        self.gridLayout_21.addLayout(self.net_info_grid, 0, 0, 1, 1)
        self.scrollArea_8.setWidget(self.scrollAreaWidgetContents_8)
        self.net_info_grid_t.addWidget(self.scrollArea_8, 0, 0, 1, 1)
        self.gridLayout_29.addLayout(self.net_info_grid_t, 0, 0, 1, 1)
        self.net_sub.addTab(self.info1, "")
        self.monitor1 = QtWidgets.QWidget()
        self.monitor1.setObjectName("monitor1")
        self.gridLayout_27 = QtWidgets.QGridLayout(self.monitor1)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.network_monitor = QtWidgets.QGridLayout()
        self.network_monitor.setObjectName("network_monitor")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.monitor1)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_38 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.net = QtWidgets.QGridLayout()
        self.net.setObjectName("net")
        self.gridLayout_38.addLayout(self.net, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.network_monitor.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.gridLayout_27.addLayout(self.network_monitor, 0, 0, 1, 1)
        self.net_sub.addTab(self.monitor1, "")
        self.gridLayout_22.addWidget(self.net_sub, 0, 0, 1, 1)
        self.gridLayout_23.addLayout(self.gridLayout_22, 0, 0, 1, 1)
        self.tabWidget.addTab(self.network, "")
        self.sensors = QtWidgets.QWidget()
        self.sensors.setObjectName("sensors")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.sensors)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.sensors_tabs = QtWidgets.QTabWidget(self.sensors)
        self.sensors_tabs.setObjectName("sensors_tabs")
        self.battery_sub = QtWidgets.QWidget()
        self.battery_sub.setObjectName("battery_sub")
        self.gridLayout_37 = QtWidgets.QGridLayout(self.battery_sub)
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.battery_grid_t = QtWidgets.QGridLayout()
        self.battery_grid_t.setObjectName("battery_grid_t")
        self.scrollArea_7 = QtWidgets.QScrollArea(self.battery_sub)
        self.scrollArea_7.setWidgetResizable(True)
        self.scrollArea_7.setObjectName("scrollArea_7")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.gridLayout_34 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_34.setObjectName("gridLayout_34")
        self.battery_grid = QtWidgets.QGridLayout()
        self.battery_grid.setObjectName("battery_grid")
        self.gridLayout_34.addLayout(self.battery_grid, 0, 0, 1, 1)
        self.scrollArea_7.setWidget(self.scrollAreaWidgetContents_7)
        self.battery_grid_t.addWidget(self.scrollArea_7, 0, 0, 1, 1)
        self.gridLayout_37.addLayout(self.battery_grid_t, 0, 0, 1, 1)
        self.sensors_tabs.addTab(self.battery_sub, "")
        self.temperatures_sub = QtWidgets.QWidget()
        self.temperatures_sub.setObjectName("temperatures_sub")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.temperatures_sub)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.scrollArea_6 = QtWidgets.QScrollArea(self.temperatures_sub)
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollArea_6.setObjectName("scrollArea_6")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.gridLayout_32 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.temperature_grid = QtWidgets.QGridLayout()
        self.temperature_grid.setObjectName("temperature_grid")
        self.gridLayout_32.addLayout(self.temperature_grid, 0, 0, 1, 1)
        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)
        self.gridLayout_18.addWidget(self.scrollArea_6, 0, 0, 1, 1)
        self.gridLayout_20.addLayout(self.gridLayout_18, 0, 0, 1, 1)
        self.sensors_tabs.addTab(self.temperatures_sub, "")
        self.gridLayout_14.addWidget(self.sensors_tabs, 0, 0, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_14, 0, 0, 1, 1)
        self.tabWidget.addTab(self.sensors, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.settings)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lineColor = QtWidgets.QLineEdit(self.settings)
        self.lineColor.setMaximumSize(QtCore.QSize(125, 16777215))
        self.lineColor.setObjectName("lineColor")
        self.gridLayout_6.addWidget(self.lineColor, 8, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.settings)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.settings)
        self.label_4.setObjectName("label_4")
        self.gridLayout_6.addWidget(self.label_4, 10, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.settings)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 7, 0, 1, 1)
        self.intervalSet = QtWidgets.QPushButton(self.settings)
        self.intervalSet.setObjectName("intervalSet")
        self.gridLayout_6.addWidget(self.intervalSet, 2, 0, 1, 1)
        self.setGraphSize = QtWidgets.QPushButton(self.settings)
        self.setGraphSize.setObjectName("setGraphSize")
        self.gridLayout_6.addWidget(self.setGraphSize, 6, 0, 1, 1)
        self.select_facecolor = QtWidgets.QPushButton(self.settings)
        self.select_facecolor.setObjectName("select_facecolor")
        self.gridLayout_6.addWidget(self.select_facecolor, 12, 0, 1, 1)
        self.interval = QtWidgets.QSpinBox(self.settings)
        self.interval.setMaximum(1000000177)
        self.interval.setSingleStep(100)
        self.interval.setProperty("value", 2000)
        self.interval.setObjectName("interval")
        self.gridLayout_6.addWidget(self.interval, 1, 0, 1, 1)
        self.setLineColor = QtWidgets.QPushButton(self.settings)
        self.setLineColor.setObjectName("setLineColor")
        self.gridLayout_6.addWidget(self.setLineColor, 9, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.settings)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.graphSize = QtWidgets.QSpinBox(self.settings)
        self.graphSize.setMaximum(5000)
        self.graphSize.setSingleStep(1)
        self.graphSize.setProperty("value", 25)
        self.graphSize.setObjectName("graphSize")
        self.gridLayout_6.addWidget(self.graphSize, 5, 0, 1, 1)
        self.facecolor = QtWidgets.QLineEdit(self.settings)
        self.facecolor.setMaximumSize(QtCore.QSize(125, 16777215))
        self.facecolor.setObjectName("facecolor")
        self.gridLayout_6.addWidget(self.facecolor, 11, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 2, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.logger_groupbox = QtWidgets.QGroupBox(self.settings)
        self.logger_groupbox.setMinimumSize(QtCore.QSize(400, 0))
        self.logger_groupbox.setObjectName("logger_groupbox")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.logger_groupbox)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.logger_grid = QtWidgets.QGridLayout()
        self.logger_grid.setObjectName("logger_grid")
        self.label_5 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_5.setObjectName("label_5")
        self.logger_grid.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_9.setObjectName("label_9")
        self.logger_grid.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_7.setObjectName("label_7")
        self.logger_grid.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_6.setObjectName("label_6")
        self.logger_grid.addWidget(self.label_6, 1, 0, 1, 1)
        self.serverUser = QtWidgets.QLineEdit(self.logger_groupbox)
        self.serverUser.setObjectName("serverUser")
        self.logger_grid.addWidget(self.serverUser, 3, 1, 1, 1)
        self.serverAddress = QtWidgets.QLineEdit(self.logger_groupbox)
        self.serverAddress.setObjectName("serverAddress")
        self.logger_grid.addWidget(self.serverAddress, 2, 1, 1, 1)
        self.connect = QtWidgets.QPushButton(self.logger_groupbox)
        self.connect.setObjectName("connect")
        self.logger_grid.addWidget(self.connect, 7, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_8.setObjectName("label_8")
        self.logger_grid.addWidget(self.label_8, 3, 0, 1, 1)
        self.loggerSQLFormat = QtWidgets.QComboBox(self.logger_groupbox)
        self.loggerSQLFormat.setObjectName("loggerSQLFormat")
        self.loggerSQLFormat.addItem("")
        self.loggerSQLFormat.addItem("")
        self.logger_grid.addWidget(self.loggerSQLFormat, 1, 1, 1, 1)
        self.sqlite3Browse = QtWidgets.QPushButton(self.logger_groupbox)
        self.sqlite3Browse.setObjectName("sqlite3Browse")
        self.logger_grid.addWidget(self.sqlite3Browse, 6, 2, 1, 1)
        self.dbName = QtWidgets.QLineEdit(self.logger_groupbox)
        self.dbName.setObjectName("dbName")
        self.logger_grid.addWidget(self.dbName, 6, 1, 1, 1)
        self.serverPassword = QtWidgets.QLineEdit(self.logger_groupbox)
        self.serverPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.serverPassword.setDragEnabled(True)
        self.serverPassword.setClearButtonEnabled(True)
        self.serverPassword.setObjectName("serverPassword")
        self.logger_grid.addWidget(self.serverPassword, 4, 1, 1, 1)
        self.serverPort = QtWidgets.QSpinBox(self.logger_groupbox)
        self.serverPort.setMaximum(65565)
        self.serverPort.setProperty("value", 3306)
        self.serverPort.setObjectName("serverPort")
        self.logger_grid.addWidget(self.serverPort, 2, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.logger_groupbox)
        self.label_10.setObjectName("label_10")
        self.logger_grid.addWidget(self.label_10, 5, 0, 1, 1)
        self.dbTable = QtWidgets.QLineEdit(self.logger_groupbox)
        self.dbTable.setDragEnabled(True)
        self.dbTable.setObjectName("dbTable")
        self.logger_grid.addWidget(self.dbTable, 5, 1, 1, 1)
        self.gridLayout_13.addLayout(self.logger_grid, 0, 0, 1, 1)
        self.gridLayout_19.addWidget(self.logger_groupbox, 0, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_19, 1, 1, 1, 1)
        self.useLogger = QtWidgets.QCheckBox(self.settings)
        self.useLogger.setObjectName("useLogger")
        self.gridLayout_11.addWidget(self.useLogger, 0, 1, 1, 1)
        self.tabWidget.addTab(self.settings, "")
        self.gridLayout_2.addWidget(self.tabWidget, 1, 2, 1, 1)
        rsrc.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(rsrc)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 22))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        rsrc.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(rsrc)
        self.statusbar.setObjectName("statusbar")
        rsrc.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(rsrc)
        self.actionQuit.setObjectName("actionQuit")
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(rsrc)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_4.setCurrentIndex(0)
        self.disk_sub.setCurrentIndex(0)
        self.net_sub.setCurrentIndex(1)
        self.sensors_tabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(rsrc)

    def retranslateUi(self, rsrc):
        _translate = QtCore.QCoreApplication.translate
        rsrc.setWindowTitle(_translate("rsrc", "Hydrogenous Resource Monitor"))
        self.swap_box.setTitle(_translate("rsrc", "Swap"))
        self.ram_box.setTitle(_translate("rsrc", "Memory"))
        self.cpu_box.setTitle(_translate("rsrc", "CPU"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.processing), _translate("rsrc", "Processing"))
        self.deselect_all.setText(_translate("rsrc", "Deselect"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.all), _translate("rsrc", "All"))
        self.searchOption_pid.setText(_translate("rsrc", "PID"))
        self.searchOption_user.setText(_translate("rsrc", "User"))
        self.searchOption_ram.setText(_translate("rsrc", "RAM Bytes"))
        self.searchOption_name.setText(_translate("rsrc", "Name"))
        self.searchOption_cpu.setText(_translate("rsrc", "CPU Percent"))
        self.searchExact.setText(_translate("rsrc", "Search Exact"))
        self.searchFuzzy.setText(_translate("rsrc", "Search Fuzzy"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.search), _translate("rsrc", "Search"))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.renice), _translate("rsrc", "Re-Nice"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.processes), _translate("rsrc", "Processes"))
        self.disk_sub.setTabText(self.disk_sub.indexOf(self.info), _translate("rsrc", "Info."))
        self.disk_sub.setTabText(self.disk_sub.indexOf(self.monitor), _translate("rsrc", "Monitor"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.disk), _translate("rsrc", "Disk"))
        self.net_sub.setTabText(self.net_sub.indexOf(self.info1), _translate("rsrc", "Info."))
        self.net_sub.setTabText(self.net_sub.indexOf(self.monitor1), _translate("rsrc", "Monitor"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.network), _translate("rsrc", "Network"))
        self.sensors_tabs.setTabText(self.sensors_tabs.indexOf(self.battery_sub), _translate("rsrc", "Battery"))
        self.sensors_tabs.setTabText(self.sensors_tabs.indexOf(self.temperatures_sub), _translate("rsrc", "Temperatures"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.sensors), _translate("rsrc", "Sensors"))
        self.label_2.setText(_translate("rsrc", "Graph Size"))
        self.label_4.setText(_translate("rsrc", "Background Color"))
        self.label_3.setText(_translate("rsrc", "Line Color"))
        self.intervalSet.setText(_translate("rsrc", "Set"))
        self.setGraphSize.setText(_translate("rsrc", "Set"))
        self.select_facecolor.setText(_translate("rsrc", "Select"))
        self.setLineColor.setText(_translate("rsrc", "Set"))
        self.label.setText(_translate("rsrc", "Interval"))
        self.logger_groupbox.setTitle(_translate("rsrc", "Logging"))
        self.label_5.setText(_translate("rsrc", "DB Name"))
        self.label_9.setText(_translate("rsrc", "Password"))
        self.label_7.setText(_translate("rsrc", "Host"))
        self.label_6.setText(_translate("rsrc", "DB Format"))
        self.serverUser.setToolTip(_translate("rsrc", "user to log into Host for data logging when MySQL Format is Used"))
        self.serverAddress.setToolTip(_translate("rsrc", "Server Address if MySQL Format is Used"))
        self.connect.setText(_translate("rsrc", "Connect"))
        self.label_8.setText(_translate("rsrc", "User"))
        self.loggerSQLFormat.setToolTip(_translate("rsrc", "format to use for storing resource useage details"))
        self.loggerSQLFormat.setItemText(0, _translate("rsrc", "MySQL"))
        self.loggerSQLFormat.setItemText(1, _translate("rsrc", "SQLite3"))
        self.sqlite3Browse.setToolTip(_translate("rsrc", "Location to save datalog if Format is SQLite3"))
        self.sqlite3Browse.setText(_translate("rsrc", "Browse"))
        self.dbName.setToolTip(_translate("rsrc", "DB Name; if SQLite3 is used, then this is the filename"))
        self.label_10.setText(_translate("rsrc", "Table Name"))
        self.useLogger.setText(_translate("rsrc", "Log Resources"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("rsrc", "Settings"))
        self.menu_File.setTitle(_translate("rsrc", "&File"))
        self.actionQuit.setText(_translate("rsrc", "&Quit"))
        self.actionQuit.setShortcut(_translate("rsrc", "Ctrl+Q"))


