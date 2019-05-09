from PyQt5 import QtWidgets,QtGui,QtCore
import os,sys,engineering_notation,json
import hurry.filesize
import psutil,copy
lib=('lib','lib_widget')

class convertFromHurry:
    units=(
            
            )
    def stringToInt(self,string,system=hurry.filesize.iec):
        if string != None:
            if type(string) == type(str()):
                if len(string) > 1:
                    end=-1*len(system[0][1])
                    unit=string[end:]
                    num=int(string[:end])
                    for i in system:
                        if i[1] == unit:
                            num=num*i[0]
                            return num
                    else:
                        return int(string)
                else:
                    return int(string)
            if type(string) == type(int()):
                return string
        else:
            return 0

class taskProxyFilter(QtCore.QSortFilterProxyModel):
    def mousePressEvent(self,event):
        print(event)

    def headerData(self, section, orientation, role):
        # if display role of vertical headers
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            # return the actual row number
            return section + 1
        # for other cases, rely on the base implementation
        return super(taskProxyFilter, self).headerData(section, orientation, role)

    def lessThan(self,left,right):
        leftData=self.sourceModel().data(left)
        rightData=self.sourceModel().data(right)
        if leftData != None and rightData != None:
            if left.column() == 0 and right.column() == 0:
                return leftData < rightData

            if left.column() == 1 and right.column() == 1:
                return leftData < rightData

            if left.column() == 2 and right.column() == 2:
                return leftData < rightData

            if left.column() == 3 and right.column() == 3:
                return leftData < rightData

            if left.column() in [4,5] and right.column() in [4,5]:
                if type(leftData) == type(int()) and type(rightData) == type(int()):
                    return leftData < rightData
                if ('-' not in leftData or '-' not in rightData) or ('-' not in leftData and '-' not in rightData):
                    a=convertFromHurry()
                    l=a.stringToInt(str(leftData),system=hurry.filesize.iec)
                    r=a.stringToInt(str(rightData),system=hurry.filesize.iec)
                else:
                    l=float(leftData)
                    r=float(rightData)
                return l < r
                
        else:
            return False



