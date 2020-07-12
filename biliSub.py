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
from file import spfn
from requests import Session
from biliTime import tostr3
import os
from lang import getlan,getdict
import sys
from command import gopt
import JSONParser
lan=None
se=JSONParser.loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('biliSub',getlan(se,ip))
def downsub(r:Session,fn:str,i:dict,ip:dict,se:dict,pr:bool=False,pi:int=1) :
    "下载字幕"
    global lan
    fq=spfn(fn)[0]
    fn="%s.%s.srt"%(fq,i['lan'])
    i['fn']=fn
    if os.path.exists(fn) :
        fg=False
        bs=True
        if 's' in ip:
            fg=True
            bs=False
        if 'y' in ip :
            if ip['y'] :
                fg=True
                bs=False
            else :
                fg=False
                bs=False
        while bs:
            inp=input(f'{lan["INPUT1"]}(y/n)'.replace("<filename>",fn))#"<filename>"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            try :
                os.remove('%s'%(fn))
            except :
                print(lan['OUTPUT1'])#删除原有文件失败，跳过下载
                return 0
    re=r.get(i['url'])
    re.encoding='utf8'
    re=re.json()
    if assrt(fn,re['body'])==0 and pr :
        print(lan['OUTPUT2'].replace('<number>',str(pi)).replace('<languagename>',i['land']))#第<number>P<languagename>字幕下载完毕！
    return 0
def assrt(fn:str,b:list):
    "保存至srt格式"
    try :
        f=open(fn,'w',encoding="utf8")
    except :
        print(lan['ERROR1'].replace('<filename>',fn))#保存"<filename>"失败！
        return -1
    i=1
    for k in b:
        try :
            f.write('%s\n'%(i))
            f.write('%s --> %s\n'%(tostr3(k['from']),tostr3(k['to'])))
            f.write('%s\n\n'%(k['content']))
        except :
            print(lan['ERROR2'].replace('<filename>',fn))#写入到文件"<filename>"时失败！
            f.close()
            return -1
        i=i+1
    f.close()
    return 0
def ffinputstr(i:list,n:int) ->(str,str):
    "分别解析出ffmpeg输入参数和元数据参数"
    s=""
    r=""
    z=n
    for k in i :
        s=s+' -i "%s"'%(k['fn'])
        r=r+' -metadata:s:%s language="%s" -metadata:s:%s title="%s"'%(z,k['lan'],z,k['land'])
        z=z+1
    for i in range(z) :
        r=r+' -map %s'%(i)
    return s,r

