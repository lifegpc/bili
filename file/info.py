from os.path import getatime,getmtime,getctime,getsize,exists,isfile,isdir
from file.time import ttos
from file.str import width,size,ftts
def getinfo(fn) :
    "获取文件信息"
    if not exists(fn['a']) :
        return -1
    if isfile(fn['a']) :
        try :
            atime=getatime(fn['a'])
        except :
            atime='N/A'
        try :
            ctime=getctime(fn['a'])
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn['a'])
        except :
            mtime='N/A'
        try :
            size=getsize(fn['a'])
        except :
            size='N/A'
        return {'l':fn['a'],'f':fn['f'],'a':atime,'c':ctime,'m':mtime,'s':size,'i':'f'}
    if isdir(fn['a']) :
        try :
            atime=getatime(fn['a'])
        except :
            atime='N/A'
        try :
            ctime=getctime(fn['a'])
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn['a'])
        except :
            mtime='N/A'
        size='N/A'
        return {'l':fn['a'],'f':fn['f'],'a':atime,'c':ctime,'m':mtime,'s':size,'i':'d'}
def getinfox(fn,xc) :
    "获取信息时带上序号"
    re=getinfo(fn)
    if re==-1 :
        return re
    else :
        re['x']=xc
        return re
def printinfo(o,m) :
    "打印单条内容"
    if 'x' in o :
        print('%s、\t' %(o['x']) , end='')
    print('%s\t' %(o['f']),end='')
    t=width(o['f'])
    t=t-t%8+8
    while t<m :
        print('\t',end='')
        t=t+8
    print('%s\t%s\t%s\t%s\t%s' %(ftts(o['i']),ttos(o['a']),ttos(o['c']),ttos(o['m']),size(o['s'])))