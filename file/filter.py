from re import search
from os.path import isdir,isfile
def listf(filelist,lx=0,ft=["xml"]) :
    "对listd获得列表进行过滤，文件夹都将保留"
    r=[]
    for i in filelist :
        if isdir(i['f']) :
            r.append(i)
            continue
        for j in ft :
            if lx==0 or lx==2 :
                r2=i['f'].rfind('.')
                if r2>-1 :
                    if i['f'][r2+1:]==j :
                        r.append(i)
                        break
                elif lx==2 :
                    r.append(i)
                    break
            else :
                if search(j,i['f'])!=None :
                    r.append(i)
                    break
    return r
def listfd(filelist) :
    "对listd列表进行过滤，只保留文件夹"
    r=[]
    for i in filelist :
        if isdir(i['f']) :
            r.append(i)
    return r
def listff(filelist) :
    "对listd列表进行过滤，只保留文件"
    r=[]
    for i in filelist :
        if isfile(i['f']) :
            r.append(i)
    return r