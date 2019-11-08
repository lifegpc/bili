from time import strftime,localtime
def ttos(tm) :
    "将时间戳转换为字符串（当地时间）"
    return strftime('%Y-%m-%d %H-%M-%S',localtime(tm))