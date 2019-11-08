from unicodedata import east_asian_width
def width(s) :
    '获取字符串宽度'
    t=0
    for i in s :
        if east_asian_width(i) in ('F','W','A') :
            t=t+2
        else :
            t=t+1
    return t