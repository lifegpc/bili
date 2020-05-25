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
from file import filtern
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
            if re and key in re:
                se[key]=re[key]
if __name__=='__main__' :
    pr()
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
    if se and 'ax' in se :
        n=se['ax']
    print('aria2c单个服务器最大连接数即-x的参数(1-16，默认3，目前为%s)：'%(n))
    inp=input('请输入1-16中的数字：')
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
    print('aria2c单个文件最大连接数即-s的参数(1-*，默认5，目前为%s)：'%(n))
    inp=input('请输入大于等于1的数字：')
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
    print('aria2c文件分片大小即-k的参数(单位M，1-1024，默认5，目前为%s)：'%(n))
    inp=input('请输入1-1024的数字：')
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
    saveset(ne)
