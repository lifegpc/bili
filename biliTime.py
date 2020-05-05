from time import gmtime,strftime,time,strptime,timezone,mktime,struct_time
from math import floor
def getDate(s) :
    "获取时间戳对应日期 UTF+8"
    i=float(s)
    return gmtime(i+3600*8)
def getNowDate() :
    "获取当前日期 UTF+8"
    return getDate(time())
def tostr(fa) :
    "转化为字符串"
    return strftime("%Y-%m-%d",fa)
def equal(a,b) :
    "比较是否同一天，同一天0，前面大1，后面大-1"
    if a[0]>b[0] :
        return 1
    elif a[0]<b[0] :
        return -1
    else :
        if a[1]>b[1] :
            return 1
        elif a[1]<b[1] :
            return -1
        else:
            if a[2]>b[2] :
                return 1
            elif a[2]<b[2] :
                return -1
            else  :
                return 0
def checktime(s:str) :
    """检查时间是否无问题\n
    True 无问题\n
    False 有问题"""
    try :
        s=strptime(s,'%Y-%m-%d')
        return True
    except :
        return False
def mkt(t) :
    "将UTC+8 时间返回为UTC时间戳（忽略本地）"
    return mktime(t)-timezone-8*3600
def tostr2(s):
    if isinstance(s,struct_time) :
        return strftime('%Y-%m-%d %H:%M:%S',s)
    else :
        return strftime('%Y-%m-%d %H:%M:%S',getDate(s))
def tostr3(i:int):
    "转换为适合srt的时间"
    return "%02d:%02d:%02d,%03d"%(floor(i/3600),floor(i%3600/60),floor(i%60),floor(i*1000%1000))
if __name__=='__main__' :
    print(getNowDate())