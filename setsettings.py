from JSONParser import loadset,saveset,getset
from re import search
from goto import with_goto
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
    print('选项前的x说明了当前选中的设置，直接回车(exe版本请不要这么做，会闪退)会保持当前设置')
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
    print('在合并完成后是否删除文件？')
    r=gk(se,'ad')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'ad',se)
    print('是否开启继续下载功能？')
    r=gk(se,'cd')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'cd',se)
    print('是否开启下载失败后自动重新下载？')
    r=gk(se,'rd')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'rd',se)
    print('是否不使用ffmpeg合并（不设置相当于否）？')
    r=gk(se,'nf')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'nf',se)
    print('默认下载最高画质偏好编码器：')
    r=gk(se,'mpc')
    print2('%s1.avc(h.264)\t%s2.hevc(h.265)\t%s3.不设置（默认）',r)
    sk(ne,'mpc',se)
    print('是否使用aria2c下载？')
    r=gk(se,'a')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'a',se)
    n=3
    if 'ax' in se :
        n=se['ax']
    print('aria2c单个服务器最大连接数即-x的参数(1-16，默认3，目前为%s)：'%(n))
    inp=input('请输入1-16中的数字：')
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i<=16 and i!=3:
                ne['ax']=i
    n=5
    if 'as' in se :
        n=se['as']
    print('aria2c单个文件最大连接数即-s的参数(1-*，默认5，目前为%s)：'%(n))
    inp=input('请输入大于等于1的数字：')
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i!=5:
                ne['as']=i
    n=5
    if 'ak' in se :
        n=se['ak']
    print('aria2c文件分片大小即-k的参数(单位M，1-1024，默认5，目前为%s)：'%(n))
    inp=input('请输入1-1024的数字：')
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i<=1024 and i!=5:
                ne['ak']=i
    print('在使用aria2c下载时是否使用备用网址？（不设置情况下为是）')
    r=gk(se,'ab')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'ab',se)
    saveset(ne)
