from time import strftime,localtime
def ttos(tm) :
    "将时间戳转换为字符串（当地时间）"
    if tm=='N/A':
        return 'N/A'
    elif tm>=0:
        return strftime('%Y-%m-%d %H-%M-%S',localtime(tm))
    else :
        return str(tm)