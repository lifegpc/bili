import file
import biliPlayerXmlParser
from os.path import exists
if __name__!="__main__" :
    print('请直接运行filter.py')
else :
    read=biliPlayerXmlParser.loadXML()
    if read==-1 :
        print('没有tv.bilibili.plater.xml文件')
        exit(-1)
    bs=True
    while bs :
        inp=input('请输入要过滤的文件数量：')
        if len(inp)>0 :
            if inp.isnumeric() :
                g=int(inp)
                bs=False
    fl=file.getfilen(g=g)
    for i in fl :
        if exists(i['a']) :
            pass