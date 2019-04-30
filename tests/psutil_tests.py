import tracemalloc,psutil

tracemalloc.start(10)
import sys
sys.path.append('../lib')
import os,sys,json
import psutil,copy
import engineering_notation as en
from hurry.filesize import si,size,iec
import netifaces as ni
import gc

class tests:
    def __init__(self):
        #obj=threaded_tasks.threaded_tasks()
        self.psutil_cpu_count()
        
    def psutil_cpu_count(self):
        self.parent=None
        self.name='tests'
        #snapshots
        while True:
            mod=self.updateData()
    tx={}
    rx={}
    disk_rx={}
    disk_tx={} 

    def gateway_info(me,self,mod):
        gt=ni.gateways()
        gateways={}
        for i in gt.keys():
            if i != 'default':
                gateways[ni.address_families[i]]=gt[i]
        mod['net']['gateways']=gateways
        #print(mod['net']['gateways'])
        return mod

    #@pyqtSlot()
    def updateData(me,k=None,noStatPrint=False): 
        self=me.parent
        k=me.name

        mod={}
        cmd=None
                
        mod=me.tasks_collection(self,mod)
        #me.upd8.emit()
        mod=me.net_collection(self,mod)
        #me.upd8.emit()
        mod=me.disk_collection(self,mod)
        #me.upd8.emit()
        mod=me.sensors_collection(self,mod)
        #me.upd8.emit()
        mod=me.gateway_info(self,mod)
        #me.upd8.emit()
        #print(mod['disk']['speed']['sda3'])
        gc.collect()
        #me.sig.emit(mod)       

    def tasks_collection(me,self,mod):
        for i in psutil.process_iter():
            cmd=' '.join(i.cmdline())
            name_list=[i.name(),]
            if cmd != '':
                name_list.append(cmd)
            if psutil.pid_exists(i.pid):
                mod[str(i.pid)]={
                                'name':' | '.join(name_list),
                                'pid':i.pid,
                                'user':i.username(),
                                'cpu':float(round(i.cpu_percent()/psutil.cpu_count(),2)),
                                'ram':size(i.memory_info().rss,system=iec),
                            }
            
        mod['total']={
                'cpu':psutil.cpu_percent(),
                'ram_bytes':psutil.virtual_memory().used,
                'ram_percent':psutil.virtual_memory().percent,
                'swap_percent':psutil.swap_memory().percent,
                'swap_bytes':psutil.swap_memory().used,
                }
        return mod
        
    def sensors_collection(me,self,mod):
        mod['sensors']={}
        mod=me.sensors_fans(self,mod) 
        mod=me.sensors_battery(self,mod)
        mod=me.sensors_temperatures(self,mod)
        return mod

    def sensors_fans(me,self,mod):
        mod['sensors']['fans']=psutil.sensors_fans()
        return mod

    def sensors_battery(me,self,mod):
        mod['sensors']['battery']=psutil.sensors_battery()
        return mod

    def sensors_temperatures(me,self,mod):
        mod['sensors']['temperatures']=psutil.sensors_temperatures()
        return mod

    def net_collection(me,self,mod):
        mod['net']={
                    'io':psutil.net_io_counters(pernic=True),
                    'stats':psutil.net_if_stats(),
                    'addrs':psutil.net_if_addrs(),
                    'speed':{}
                    }

        if me.rx == {}:
            for i in mod['net']['io'].keys():
                me.rx[i]=0
        if me.tx == {}:
            for i in mod['net']['io'].keys():
                me.tx[i]=0
        
        if mod['net']['speed'] == {}:
            for i in mod['net']['io'].keys():
                mod['net']['speed'][i]={}
                for k in ['rx','tx']:
                    mod['net']['speed'][i][k]=0

        for i in me.rx.keys():
            if me.rx[i] > 0:
                mod['net']['speed'][i]['rx']=int((mod['net']['io'][i].bytes_recv-me.rx[i])/2)
        for i in me.tx.keys():
            if me.tx[i] > 0:
                mod['net']['speed'][i]['tx']=int((mod['net']['io'][i].bytes_sent-me.tx[i])/2)

        for i in me.tx.keys():
            me.tx[i]=mod['net']['io'][i].bytes_sent

        for i in me.rx.keys():
            me.rx[i]=mod['net']['io'][i].bytes_recv
        return mod

    def disk_collection(me,self,mod):
        mod['disk']={
                'io':psutil.disk_io_counters(perdisk=True),
                'partitions':psutil.disk_partitions(),
                'usage':{},
                'speed':{},
                }

        tmp_tx={}
        tmp_rx={}
        #print(me.disk_rx)
        for i in me.disk_rx.keys():
            if i in mod['disk']['io'].keys():
                tmp_rx[i]=me.disk_rx[i]
                tmp_tx[i]=me.disk_tx[i]
        me.disk_rx=tmp_rx
        me.disk_tx=tmp_tx

        for path in mod['disk']['partitions']:
            Path=path.mountpoint
            mod['disk']['usage'][path.device]=psutil.disk_usage(Path)

        for path in mod['disk']['io'].keys():
            mod['disk']['speed'][path]={}
            for mode in ['rx','tx']:
                Path='dev/{}'.format(path)
                mod['disk']['speed'][path][mode]=0
    
        if me.disk_rx == {}:
            for i in mod['disk']['speed'].keys():
                me.disk_rx[i]=0
        if me.disk_tx == {}:
            for i in mod['disk']['speed'].keys():
                me.disk_tx[i]=0

        for i in me.disk_rx.keys():
            if i in mod['disk']['io'].keys():
                if me.disk_rx[i] > 0:
                    mod['disk']['speed'][i]['rx']=int((mod['disk']['io'][i].read_bytes-me.disk_rx[i]))

        for i in me.disk_tx.keys():
            if i in mod['disk']['io'].keys():
                if me.disk_tx[i] > 0:
                    mod['disk']['speed'][i]['tx']=int((mod['disk']['io'][i].write_bytes-me.disk_tx[i]))

        for i in me.disk_tx.keys():
            me.disk_tx[i]=mod['disk']['io'][i].write_bytes

        for i in me.disk_rx.keys():
            me.disk_rx[i]=mod['disk']['io'][i].read_bytes
        return mod


if __name__ == '__main__':
    t=tests()
    
