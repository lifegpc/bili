from JSONParser import loadset,saveset,getset
from re import search
l1=['x','','']
l2=['','x','']
l3=['','','x']
def print2(s:str,l:list) :
    t=search('%s',s)
    u=len(l)
    i=0
    while t :
        s=s.replace('%s',str(l[i]),1)
        t=search('%s',s)
        i=i+1
        if i==u :
            i=0
    print(s)
def gk(se:dict,key:str) :
    if not se:
        return l3
    else :
        no=getset(se,key)
        if no==None :
            return l3
        elif no :
            return l1
        else :
            return l2
def sk(se:dict,key:str,re:dict) :
    b=True
    while b:
        i=input('请输入选项中的数字以选择')
        if len(i) > 0 and i.isnumeric():
            i=int(i)
            if i==1 :
                b=False
                se[key]=True
            elif i==2 :
                b=False
                se[key]=False
            elif i==3 :
                b=False
        else :
            b=False
            if key in re:
                se[key]=re[key]
if __name__=='__main__' :
    ne={}
    se=loadset()
    if not isinstance(se,dict) :
        se=None
    r=[]
    print('选项前的x说明了当前选中的设置，直接回车会保持当前设置')
    if se :
        print('删除当前文件夹下的setting.json可以重置设置')
    print('是否默认启用弹幕过滤？')
    r=gk(se,'dmgl')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'dmgl',se)
    print('是否要默认下载最高画质（这样将不会询问具体画质）？')
    r=gk(se,'mp')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'mp',se)
    print('在合并完成后是否默认删除文件（设置该项后将不会询问是否自动删除）？')
    r=gk(se,'ad')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'ad',se)
    print('是否开启继续下载功能？')
    r=gk(se,'cd')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'cd',se)
    saveset(ne)
