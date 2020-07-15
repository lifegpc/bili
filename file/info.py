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
from os.path import getatime,getmtime,getctime,getsize,exists,isfile,isdir
from file.time import ttos
from file.str import width,size,ftts
from re import split
from platform import system
def getinfo(fn) :
    "获取文件信息"
    if not exists(fn['a']) :
        return -1
    if isfile(fn['a']) :
        try :
            atime=getatime(fn['a'])
        except :
            atime='N/A'
        try :
            ctime=getctime(fn['a'])
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn['a'])
        except :
            mtime='N/A'
        try :
            size=getsize(fn['a'])
        except :
            size='N/A'
        return {'l':fn['a'],'f':fn['f'],'a':atime,'c':ctime,'m':mtime,'s':size,'i':'f'}
    if isdir(fn['a']) :
        try :
            atime=getatime(fn['a'])
        except :
            atime='N/A'
        try :
            ctime=getctime(fn['a'])
        except :
            ctime='N/A'
        try :
            mtime=getmtime(fn['a'])
        except :
            mtime='N/A'
        size='N/A'
        return {'l':fn['a'],'f':fn['f'],'a':atime,'c':ctime,'m':mtime,'s':size,'i':'d'}
def getinfox(fn,xc) :
    "获取信息时带上序号"
    re=getinfo(fn)
    if re==-1 :
        return re
    else :
        re['x']=xc
        return re
def printinfo(o,m) :
    "打印单条内容"
    if 'x' in o :
        print('%s、\t' %(o['x']) , end='')
    print('%s\t' %(o['f']),end='')
    t=width(o['f'])
    t=t-t%8+8
    while t<m :
        print('\t',end='')
        t=t+8
    print('%s\t%s\t%s\t%s\t%s' %(ftts(o['i']),ttos(o['a']),ttos(o['c']),ttos(o['m']),size(o['s'])))
def geturlfe(uri) ->str:
    "获取网址中的文件扩展名"
    r=str(uri).split('?')
    r=r[0]
    r=r.split('.')
    r=r[len(r)-1]
    return r
def spfn(fn:str) -> (str,str):
    "分离文件名为文件名和扩展名"
    r=fn.split('.')
    h=r[-1]
    s=""
    f=True
    for i in r[:-1]:
        if f :
            f=False
            s=i
        else :
            s=s+"."+i
    return s,h
def spfln(f:str)->(str,str):
    "分离完整文件名为路径和文件名"
    r=split(r'[\\/]',f)
    n=r[-1]
    s=""
    f=True
    for i in r[:-1] :
        if f:
            f=False
            s=i
        else :
            s=s+"/"+i
    if s=="" :
        if system()=="Linux" :
            s="/"
        else :
            s="."
    return s,n
