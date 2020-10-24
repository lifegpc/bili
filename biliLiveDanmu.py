# (C) 2019-2020 lifegpc
# This file is part of bili.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from requests import Session
from JSONParser import getset,loadset
from file import mkdir
import os
from biliDanmuXmlFilter import Filter
from biliDanmuCreate import objtoxml
import file
import sys
from command import gopt
from lang import getdict,getlan
lan=None
se=loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('biliDanmu',getlan(se,ip))
def lrdownload(data:dict,r:Session,ip:dict,se:dict,xml,xmlc:list) :
    """下载直播回放弹幕
    -1 文件夹创建失败
    -2 API解析失败
    -3 打开文件失败"""
    ns=True
    if 's' in ip :
        ns=False
    o="Download/"
    read=getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR3'].replace('<dirname>',o))#创建文件夹<dirname>失败。
        return -1
    fin=True
    if getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    if fin:
        filen='%s%s.xml'%(o,file.filtern('%s(%s,%s)'%(data['title'],data['rid'],data['roomid'])))
    else :
        filen=f"{o}{file.filtern(data['title'])}.xml"
    if os.path.exists(filen) :
        fg=False
        bs=True
        if not ns:
            fg=True
            bs=False
        if 'y' in se:
            fg = se['y']
            bs = False
        if 'y' in ip :
            fg = ip['y']
            bs = False
        while bs:
            inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)？")#文件"<filename>"已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            os.remove(filen)
        else :
            return 0
    dm=[]
    ot={'chatserver':'api.live.bilibili.com','chatid':data['rid'],'mission':0,'maxlimit':8000,'state':0,'real_name':0,'source':'k-v'}
    ot['list']=[]
    for i in data['dm']['index_info']:
        re=r.get('https://api.live.bilibili.com/xlive/web-room/v1/dM/getDMMsgByPlayBackID?rid=%s&index=%s'%(data['rid'],i['index']))
        re=re.json()
        if re['code']!=0 :
            print('%s %s'%(re['code'],re['message']))
            return -2
        for j in re['data']['dm']['dm_info'] :
            dm.append(j)
    if ns:
        print(lan['OUTPUT19'].replace('<number>',str(len(dm))))#解析完毕，共获得<number>条弹幕。\n正在将JSON转换为XML……
    for i in dm :
        t={}
        t['ti']='%.5f'%(i['ts']/1000)
        t['mod']=i['dm_mode']
        t['fs']=i['dm_fontsize']
        t['fc']=i['dm_color']
        t['ut']=round(i['check_info']['ts']/1000)
        t['dp']=i['dm_type']
        t['si']=i['user_hash']
        t['ri']=0
        t['t']=i['text']
        ot['list'].append(t)
    try :
        f=open(filen,mode='w',encoding='utf8')
        f.write('<?xml version="1.0" encoding="UTF-8"?>')
        f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (ot['chatserver'],ot['chatid'],ot['mission'],ot['maxlimit'],ot['state'],ot['real_name'],ot['source']))
    except:
        print(lan['ERROR5'].replace('<filename>',filen))#打开文件"<filename>"失败
        return -3
    if xml==1 :
        l=0 #过滤数量
        z=len(dm) #总数量
        for i in ot['list'] :
            read=Filter(i,xmlc)
            if read :
                l=l+1
            else :
                try :
                    f.write(objtoxml(i))
                except :
                    print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                    return -3
        if ns:
            print(lan['OUTPUT3'].replace('<number>',str(l)))#共计过滤%s条
            print(lan['OUTPUT4'].replace('<number>',str(z-l)))#实际输出<number>条
    else :
        for i in ot['list'] :
            f.write(objtoxml(i))
    try :
        f.write('</i>')
        f.close()
    except :
        print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
        return -3
    print(lan['OUTPUT20'])#下载完毕！
    return 0
