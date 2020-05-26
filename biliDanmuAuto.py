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
import biliDanmu
import json
import biliLogin
import time
import biliTime
def getMembers(filen,r,da,pos,mri,ip) :
    "获取弹幕条数"
    ns=True
    if 's' in ip :
        ns=False
    bs=True
    ts=300
    rec=0
    m2=mri
    if ns:
        print('正在抓取%s的弹幕......' % (biliTime.tostr(biliTime.getDate(da))))
    while bs :
        read=biliDanmu.downloadh(filen,r,pos,da)
        if read==-1 :
            return -1
        elif read == -3 :
            rec=rec+1
            if rec%5!=0 :
                print('5秒后将进行第%s次重连' % (rec))
                time.sleep(5)
            else :
                bss=True
                while bss:
                    inn=input('已经第%s次失败了，是否继续重连？(y/n)' % (rec))
                    if len(inn)>0 and inn[0].lower()=='y' :
                        print('5秒后将进行第%s次重连' % (rec))
                        time.sleep(5)
                        bss=False
                    elif len(inn)>0 and inn[0].lower()=='n' :
                        exit()
        elif 'status' in read and read['status']==-2 :
            obj=json.loads(read['d'])
            if obj['code']==-101 :
                if obj['message']=='账户未登录' :
                    ud={}
                    read=biliLogin.login(r,ud,ip)
                    if read>1 :
                        exit()
                else :
                    print(obj)
                    print('休眠%ss' % (ts))
                    time.sleep(ts)
                    ts=ts+300
            else :
                print(obj)
                print('休眠%ss' % (ts))
                time.sleep(ts)
                ts=ts+300
        else :
            bs=False
    d=read
    l=0
    li=[]
    z=len(d['list'])
    if ns:
        print('正在处理......')
    for i in d['list'] :
        if int(m2)<int(i['ri']) :
            m2=i['ri']
        if int(mri)<int(i['ri']) :
            l=l+1
            li.append(i)
    d['list']=li
    return {'z':z,'l':l,'m':m2,'d':d}
def reload(d,mri,ns) :
    l=0
    li=[]
    if ns:
        print('正在处理......')
    for i in d['d']['list'] :
        if int(mri)<int(i['ri']) :
            l=l+1
            li.append(i)
    d['d']['list']=li
    return {'z':d['z'],'l':l,'m':d['m'],'d':d['d']}
def getnownumber(d,mri) :
    l=0
    m=len(d['list'])
    for i in d['list'] :
        if int(mri)<int(i['ri']) :
            l=l+1
    return {'l':l,'m':m}