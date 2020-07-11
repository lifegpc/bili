# (C) 2019-2020 lifegpc
# This file is part of bili.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from JSONParser import loadset,saveset,getset
from re import search
from PrintInfo import pr
from file import filterd
from lang import lan,getlan,getdict
import sys
from command import gopt
from JSONParser import loadset
la=None
se=loadset()
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
la=getdict('setsettings',getlan(se,ip))
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
        i=input(la['INPUT1'])#请输入选项中的数字以选择
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
            if re and key in re:
                se[key]=re[key]
if __name__=='__main__' :
    pr()
    ne={}
    se=loadset()
    if not isinstance(se,dict) :
        se=None
    r=[]
    print(la['OUTPUT1'])#选项前的x指明了当前选中的设置，直接回车会保持当前设置
    if se :
        print(la['OUTPUT2'])#删除当前文件夹下的setting.json可以重置设置
    n=la['NOTSET']#不设置
    p=""
    if se and 'lan' in se :
        p=se['lan']
        n=lan[p]
    print(la['OUTPUT3'].replace('<languagename>',n))#请选择程序语言（目前为<languagename>）：
    print(f'null : {la["NOTSET"]}')
    for i in lan.keys() :
        print(f'{i} : {lan[i]}')
    r=input(la['INPUT2'])#请输入:之前的语言代码：
    if len(r) >0 and (r in lan or r=="null"):
        p=r
    if p!="null" :
        ne['lan']=p
    print(la['INPUT3'])#是否默认启用弹幕过滤？
    r=gk(se,'dmgl')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'dmgl',se)
    print(la['INPUT4'])#是否要默认下载最高画质（这样将不会询问具体画质）？
    r=gk(se,'mp')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'mp',se)
    print(la['INPUT5'])#在合并完成后是否删除无用文件？
    r=gk(se,'ad')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'ad',se)
    print(la['INPUT6'])#是否开启继续下载功能？
    r=gk(se,'cd')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'cd',se)
    print(la['INPUT7'])#是否开启下载失败后自动重新下载？
    r=gk(se,'rd')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'rd',se)
    print(f"{la['INPUT8']}{la['NTN']}")#是否不使用ffmpeg合并？ （不设置相当于否）
    r=gk(se,'nf')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'nf',se)
    print(la['INPUT9'])#默认下载最高画质时偏好的视频编码：
    r=gk(se,'mpc')
    print2(f'%s1.avc(h.264)\t%s2.hevc(h.265)\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'mpc',se)
    print(f"{la['INPUT10']}{la['NTY']}")#是否使用aria2c下载？（不设置相当于是）
    r=gk(se,'a')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}',r)
    sk(ne,'a',se)
    n=3
    if se and 'ax' in se :
        n=se['ax']
    print(la['INPUT11'].replace('<value3>',str(n)).replace('<value1>','1-16').replace('<value2>','3'))#使用aria2c时单个服务器最大连接数(有效值：<value1>，默认：<value2>，目前：<value3>)： 1-16 3
    inp=input(la['INPUT12'].replace('<min>','1').replace('<max>','16'))#请输入<min>-<max>中的数字： 1 16
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i<=16 and i!=3:
                ne['ax']=i
    elif n!=3 :
        ne['ax']=n
    n=5
    if se and 'as' in se :
        n=se['as']
    print(la['INPUT13'].replace('<value3>',str(n)).replace('<value1>','1-*').replace('<value2>','5'))#使用aria2c时单个文件最大连接数(1-*，默认5，目前为%s)：
    inp=input(la['INPUT14'].replace('<min>','1'))#请输入大于等于<min>的数字： 1
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i!=5:
                ne['as']=i
    elif n!=5:
        ne['as']=n
    n=5
    if se and 'ak' in se :
        n=se['ak']
    print(la['INPUT15'].replace('<value4>',str(n)).replace('<value1>','M').replace('<value2>','1-1024').replace('<value3>','5'))#aria2c文件分片大小(单位M，1-1024，默认5，目前为%s)：
    inp=input(la['INPUT12'].replace('<min>','1').replace('<max>','1024'))#请输入1-1024的数字：
    if len(inp)>0 :
        if inp.isnumeric() :
            i=int(inp)
            if i>=1 and i<=1024 and i!=5:
                ne['ak']=i
    elif n!=5 :
        ne['ak']=n
    print('在使用aria2c下载时是否使用备用网址？（不设置情况下为是）')
    r=gk(se,'ab')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'ab',se)
    n='prealloc'
    if se and 'fa' in se:
        n=se['fa']
    print('在使用arai2c下载时预分配方式即--file-allocation的参数(默认为prealloc，目前为%s)'%(n))
    print('1.none\t2.prealloc\t3.trunc\t4.falloc')
    inp=input('请输入选项中的数字以选择')
    if len(inp)>0 and inp.isnumeric() :
        i=int(inp)
        x=['none','prealloc','trunc','falloc']
        if i>0 and i<5 and i!=2 :
            ne['fa']=x[i-1]
    elif n!="prealloc" :
        ne['fa']=n
    print('文件名中是否输出视频画质信息？（不设置情况下为是）')
    r=gk(se,'sv')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'sv',se)
    print('是否强制增加视频元数据（这会导致原本不需要转码的视频被转码，转码不会影响画质）？（不设置情况下为否）')
    r=gk(se,'ma')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'ma',se)
    n="0"
    if se and 'ms' in se :
        n=se['ms']
    print('在使用aria2c下载时最大总体速度，即--max-overall-download-limit的参数，默认单位为B，可以使用K和M为单位（默认为0，即不限制，目前为%s）：'%(n))
    inp=input('请输入大小（100B可以输入100，100KiB输入100K，100MiB输入100M）：')
    if len(inp)>0 :
        t=search("^[0-9]+[MK]?$",inp)
        if t!=None :
            if inp!="0" :
                ne['ms']=inp
    elif n!="0" :
        ne['ms']=n
    print('收藏夹是否自动下载每一个视频的所有分P？')
    r=gk(se,'da')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'da',se)
    print('下载全弹幕时两次抓取之间的天数默认设置为自动？（不设置情况下为否）')
    r=gk(se,'jt')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'jt',se)
    o="Download/"
    if se and 'o' in se:
        o=se['o']
    print('下载文件夹位置（默认为Download/，当前为%s）'%(o))
    inp=input('请输入下载文件夹的位置：')
    if len(inp)>0:
        if inp!='Download/':
            ne['o']=filterd(inp)
    elif o!='Download/' :
        ne['o']=o
    print('解析收藏夹时若未指定收藏夹，是否不自动解析为默认收藏夹而是返回列表以选择？（不设置情况下为否）')
    r=gk(se,'af')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'af',se)
    print('下载小视频时，放入文件名中的描述长度是否可以超过20字？（不设置情况下为否）')
    r=gk(se,'slt')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'slt',se)
    print('requests是否使用环境变量中的代理设置？（不设置情况下为是）')
    r=gk(se,'te')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'te',se)
    print('合并完成后删除文件时是否保留字幕文件？（不设置情况下为否）')
    r=gk(se,'bd')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'bd',se)
    print('使用aria2c时是否关闭异步DNS（关闭后在Windows系统下可以解决Timeout while contacting DNS servers问题）？（不设置情况下为否）')
    r=gk(se,'cad')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'cad',se)
    print('直播回放简介写入元数据时是否进行去HTML化？（不设置情况下为是）')
    r=gk(se,'lrh')
    print2('%s1.是\t%s2.否\t%s3.不设置（默认）',r)
    sk(ne,'lrh',se)
    saveset(ne)
