from file.info import getinfox
from os.path import exists
def getinfod(filelist) :
    "从listdir获得的列表得到信息"
    j=1
    ar=[]
    for i in filelist :
        r=getinfox(i,j)
        if r!=-1 :
            j=j+1
            ar.append(r)
    return ar