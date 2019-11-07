from os.path import getatime,getmtime,getctime,getsize,exists,isfile,isdir
def getinfo(fn) :
    if not exists(fn) :
        return -1
    if isfile(fn) :
        try :
            atime=getatime(fn)
        except :
            atime='N/A'
        try :
            ctime=getctime(fn)
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn)
        except :
            mtime='N/A'
        try :
            size=getsize(fn)
        except :
            size='N/A'
        return {'f':fn,'a':atime,'c':ctime,'m':mtime,'s':size,'i':'f'}
    if isdir(fn) :
        try :
            atime=getatime(fn)
        except :
            atime='N/A'
        try :
            ctime=getctime(fn)
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn)
        except :
            mtime='N/A'
        size='N/A'
        return {'f':fn,'a':atime,'c':ctime,'m':mtime,'s':size,'i':'d'}
def getinfox(fn,xc) :
    re=getinfo(fn)
    if re==-1 :
        return re
    else :
        re['x']=xc
        return re