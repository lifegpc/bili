from time import gmtime,strftime,time,strptime
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
if __name__=='__main__' :
    print(getNowDate())