import PyQt5.QtCore
import psutil,os,sys,json
import engineering_notation as en
class resource_used(PyQt5.QtCore.QCoreApplication):
    def __init__(self,parent):
        self.parent=parent

    def values(self):
        return {
                'ram':'RAM {}'.format(en.EngNumber(psutil.virtual_memory().used,2)),
                'cpu':'CPU {}%',
                'swap':'SWAP {}'.format(en.EngNumber(psutil.swap_memory().used,2))
                }

    def used(self,k=None):
        try:
            a={}
            if k == None:
                a={
                        'ram':psutil.virtual_memory().percent,
                        'cpu':round(psutil.cpu_percent()/psutil.cpu_count(),2),
                        'swap':psutil.swap_memory().percent
                        }
                if int(a['cpu']) < 1:
                    a={
                        'ram':psutil.virtual_memory().percent,
                        'cpu':psutil.cpu_percent(interval=0.5)/psutil.cpu_count(),
                        'swap':psutil.swap_memory().percent
                        }
                    print(a['cpu'],'resource.py')
            else:
                if k == 'cpu':
                    a['cpu']=round(psutil.cpu_percent(),2)
                    if int(a['cpu']) < 1:
                        a['cpu']=psutil.cpu_percent()
                if k == 'ram':
                    a['ram']=psutil.virtual_memory().percent
                if k == 'swap':
                    a['swap']=psutil.swap_memory().percent
                        
            return a
        except Exception as e:
            self.notify(parent,e)

        
