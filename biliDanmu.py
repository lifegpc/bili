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
import biliDanmuDown
from os.path import exists
from os import remove
import biliDanmuXmlParser
import biliDanmuCreate
import biliDanmuXmlFilter
import biliTime
import time
import json
import biliLogin
import biliDanmuAuto
import file
from JSONParser import getset,loadset
from file import mkdir
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
def downloadh(filen,r,pos,da) :
    d=biliDanmuDown.downloadh(pos,r,biliTime.tostr(biliTime.getDate(da)))
    if d==-1 :
        print(lan['ERROR1'])#网络错误！
        return -3
    if exists(filen) :
        remove(filen)
    try :
        f=open(filen,mode='w',encoding='utf8')
        f.write(d)
        f.close()
    except:
        print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
        return -1
    try :
        d=biliDanmuXmlParser.loadXML(filen)
        remove(filen)
        return d
    except :
        return {'status':-2,'d':d}
def DanmuGetn(c,data,r,t,xml,xmlc,ip:dict,se:dict) :
    "处理现在的弹幕"
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    read=getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not exists(o) :
            mkdir(o)
    except:
        print(lan['ERROR3'].replace('<dirname>',o))#创建文件夹<dirname>失败。
        return -3
    try :
        if not exists('Temp') :
            mkdir('Temp')
    except:
        print(lan['ERROR3'].replace('<dirname>',"Temp"))#创建Temp文件夹失败
        return -3
    if t=='av' :
        d=biliDanmuDown.downloadn(data['page'][c-1]['cid'],r)
        if data['videos'] ==1 :
            filen=o+file.filtern(data['title']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        else :
            filen=o+file.filtern(data['title']+'-'+f"{c}."+data['page'][c-1]['part']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        if d==-1 :
            print(lan['ERROR1'])#网络错误
            exit()
        if exists(filen) :
            fg=False
            bs=True
            if not ns:
                bs=False
                fg=True
            if 'y' in ip:
                if ip['y']:
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)？")#文件"<filename>"已存在，是否覆盖？
                if inp[0].lower()=='y' :
                    bs=False
                    fg=True
                elif inp[0].lower()=='n' :
                    bs=False
            if fg :
                try :
                    remove(filen)
                except :
                    print(lan['ERROR4'])#删除原有文件失败，跳过下载
                    return -1
            else :
                return -1
        if xml==2 :
            try :
                f=open(filen,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                return -2
            return 0
        else :
            filen2="Temp/n_"+str(data['page'][c-1]['cid'])+".xml"
            if exists(filen2) :
                remove(filen2)
            try :
                f=open(filen2,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                return -2
            d=biliDanmuXmlParser.loadXML(filen2)
            remove(filen2)
            try :
                f=open(filen,mode='w',encoding='utf8')
            except:
                print(lan['ERROR5'].replace('<filename>',filen))#打开文件"<filename>"失败
                return -2
            try :
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d['chatserver'],d['chatid'],d['mission'],d['maxlimit'],d['state'],d['real_name'],d['source']))
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -2
            if ns:
                print(f"{lan['OUTPUT1']}{len(d['list'])}")#总计：
                print(lan['OUTPUT2'])#正在过滤……
            l=0
            for i in d['list'] :
                read=biliDanmuXmlFilter.Filter(i,xmlc)
                if read :
                    l=l+1
                else :
                    try :
                        f.write(biliDanmuCreate.objtoxml(i))
                    except :
                        print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                        return -2
            if ns:
                print(lan['OUTPUT3'].replace('<number>',str(l)))#共计过滤%s条
                print(lan['OUTPUT4'].replace('<number>',str(len(d['list'])-l)))#实际输出<number>条
            try :
                f.write('</i>')
                f.close()
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -2
            return 0
    elif t=='ss' :
        d=biliDanmuDown.downloadn(c['cid'],r)
        pat=o+file.filtern('%s(SS%s)' % (data['mediaInfo']['title'],data['mediaInfo']['ssId']))
        try :
            if not exists(pat) :
                mkdir(pat)
        except :
            print(lan['ERROR3'].replace('<dirname>',pat))#创建文件夹<dirname>失败。
            return -3
        if c['s']=='e' :
            filen='%s/%s' %(pat,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        else :
            filen='%s/%s' %(pat,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['title'],c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        if d==-1 :
            print(lan['ERROR1'])#网络错误！
            exit()
        if exists(filen) :
            fg=False
            bs=True
            if not ns:
                fg=True
                bs=False
            if 'y' in ip:
                if ip['y']:
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)？")#文件"<filename>"已存在，是否覆盖？
                if inp[0].lower()=='y' :
                    bs=False
                    fg=True
                elif inp[0].lower()=='n' :
                    bs=False
            if fg :
                try :
                    remove(filen)
                except :
                    print(lan['ERROR4'])#删除原有文件失败，跳过下载
                    return -1
            else :
                return -1
        if xml==2 :
            try :
                f=open(filen,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                return -2
            return 0
        else :
            filen2="Temp/n_"+str(c['cid'])+".xml"
            if exists(filen2) :
                remove(filen2)
            try :
                f=open(filen2,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                return -2
            d=biliDanmuXmlParser.loadXML(filen2)
            remove(filen2)
            try :
                f=open(filen,mode='w',encoding='utf8')
            except:
                print(lan['ERROR5'].replace('<filename>',filen))#打开文件"<filename>"失败
                return -2
            try :
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d['chatserver'],d['chatid'],d['mission'],d['maxlimit'],d['state'],d['real_name'],d['source']))
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -2
            if ns:
                print(f"{lan['OUTPUT1']}{len(d['list'])}")#总计：
                print(lan['OUTPUT2'])#正在过滤……
            l=0
            for i in d['list'] :
                read=biliDanmuXmlFilter.Filter(i,xmlc)
                if read :
                    l=l+1
                else :
                    try :
                        f.write(biliDanmuCreate.objtoxml(i))
                    except :
                        print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                        return -2
            if ns:
                print(lan['OUTPUT3'].replace('<number>',str(l)))#共计过滤%s条
                print(lan['OUTPUT4'].replace('<number>',str(len(d['list'])-l)))#实际输出<number>条
            try :
                f.write('</i>')
                f.close()
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -2
            return 0
def DanmuGeta(c,data,r,t,xml,xmlc,ip:dict,se:dict,che:bool=False) :
    "全弹幕处理"
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    read=getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not exists(o) :
            mkdir(o)
    except:
        print(lan['ERROR3'].replace('<dirname>',o))#创建文件夹<dirname>失败。
        return -1
    try :
        if not exists('Temp') :
            mkdir('Temp')
    except:
        print(lan['ERROR3'].replace('<dirname>',"Temp"))#创建Temp文件夹失败
        return -1
    if t=='av' :
        bs=True
        at2=False
        fi=True
        jt=False
        if getset(se,'jt')==True :
            jt=True
        while bs :
            if fi and 'jt' in ip:
                fi=False
                at=ip['jt']
            elif jt :
                at='a'
            elif ns:
                at=input(lan['INPUT2'].replace('<value>','1-365'))#请输入两次抓取之间的天数（有效值为<value>，a会启用自动模式（推荐））：
            else :
                print(lan['ERROR7'])#请使用"--jt <number>|a|b"来设置两次抓取之间的天数
                return -1
            if at.isnumeric() and int(at)<=365 and int(at)>=1 :
                at=int(at)
                bs=False
            elif len(at)>0 and at[0].lower()=='a' :
                at2=True
                at=1
                bs=False
        if data['videos'] ==1 :
            filen=o+file.filtern(data['title']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        else :
            filen=o+file.filtern(data['title']+'-'+f"{c}."+data['page'][c-1]['part']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        if exists(filen) :
            fg=False
            bs=True
            if not ns:
                fg=True
                bs=False
            if 'y' in ip:
                if ip['y']:
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)？")#文件"<filename>"已存在，是否覆盖？
                if inp[0].lower()=='y' :
                    bs=False
                    fg=True
                elif inp[0].lower()=='n' :
                    bs=False
            if fg :
                try :
                    remove(filen)
                except :
                    print(lan['ERROR4'])#删除原有文件失败，跳过下载
                    return -2
            else :
                return -2
        da=int(data['pubdate'])
        zl=0
        zg=0
        zm=0
        now=1
        now2=now
        if ns:
            print(lan['OUTPUT5'])#正在抓取最新弹幕……
        d2=biliDanmuDown.downloadn(data['page'][c-1]['cid'],r)
        if d2==-1 :
            print(lan['ERROR1'])#网络错误！
            exit()
        filen2="Temp/a_"+str(data['page'][c-1]['cid'])+".xml"
        if exists(filen2) :
            remove(filen2)
        try :
            f=open(filen2,mode='w',encoding='utf8')
            f.write(d2)
            f.close()
        except :
            print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
            return -3
        d3=biliDanmuXmlParser.loadXML(filen2)
        remove(filen2)
        ma=int(d3['maxlimit'])
        allok=False
        if len(d3['list'])<ma-10 :
            bs=True
            if not ns:
                bs=False
            while bs :
                sts=input(f"{lan['INPUT3'].replace('<number>',str(len(d3['list']))).replace('<limit>',str(ma))}(y/n)")
                if len(sts)>0 :
                    if sts[0].lower()=='y' :
                        bs=False
                    elif sts[0].lower()=='n' :
                        allok=True
                        bs=False
        if not allok :
            d2=d3
            if ns:
                print(lan['OUTPUT6'].replace('<number>',str(len(d2['list']))))#抓取到<number>条弹幕，最新弹幕将在最后处理
        try :
            f2=open(filen,mode='w',encoding='utf8')
        except :
            print(lan['ERROR5'].replace('<filename>',filen))#打开文件"<filename>"失败
            return -3
        if not allok :
            try :
                f2.write('<?xml version="1.0" encoding="UTF-8"?>')
                f2.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d2['chatserver'],d2['chatid'],d2['mission'],d2['maxlimit'],d2['state'],d2['real_name'],d2['source']))
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -3
        mri=0
        mri2=0
        t1=0
        t2=0
        tem={}
        fir=True
        while not allok and biliTime.equal(biliTime.getDate(da),biliTime.getNowDate())<0 and ((not at2) or (at2 and biliTime.equal(biliTime.getDate(da+now*24*3600),biliTime.getNowDate())<0)) :
            t1=time.time()
            if (not at2) or fir :
                if ns:
                    print(lan['OUTPUT7'].replace('<date>',biliTime.tostr(biliTime.getDate(da))))#正在抓取<date>的弹幕……
                bs=True
                ts=300
                rec=0
                while bs :
                    read=downloadh(filen2,r,data['page'][c-1]['cid'],da)
                    if read==-1 :
                        return -3
                    elif read==-3:
                        rec=rec+1
                        if rec%5!=0 :
                            time.sleep(5)
                            print(lan['OUTPUT8'].replace('<number>',str(rec)))#正在进行第<number>次重连
                        else :
                            bss=True
                            while bss:
                                inn=input(f"{lan['INPUT4'].replace('<number>',str(rec))}(y/n)")#是否重连？（已经失败<number>次）
                                if len(inn)>0 and inn[0].lower()=='y' :
                                    time.sleep(5)
                                    print(lan['OUTPUT8'].replace('<number>',str(rec)))#正在进行第<number>次重连
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
                                print(lan['OUTPUT9'].replace('<number>',str(ts)))#休眠<number>s
                                time.sleep(ts)
                                ts=ts+300
                        else :
                            print(obj)
                            print(lan['OUTPUT9'].replace('<number>',str(ts)))#休眠<number>s
                            time.sleep(ts)
                            ts=ts+300
                    else :
                        bs=False
                d=read
                l=0
                g=0
                if ns:
                    print(lan['OUTPUT10'])#正在处理弹幕……
                for i in d['list'] :
                    if mri2<int(i['ri']) :
                        mri2=int(i['ri'])
                    if mri<int(i['ri']) :
                        l=l+1
                        if xml==2 :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                return -3
                        elif xml==1 :
                            read=biliDanmuXmlFilter.Filter(i,xmlc)
                            if read :
                                g=g+1
                            else :
                                try :
                                    f2.write(biliDanmuCreate.objtoxml(i))
                                except :
                                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                    return -3
            else :
                rr=False
                rr2=False
                if biliTime.tostr(biliTime.getDate(da+now*24*3600)) in tem :
                    if ns:
                        print(lan['OUTPUT11'].replace('<date>',biliTime.tostr(biliTime.getDate(da+now*24*3600))))#从内存中获取了<date>的弹幕。
                    read=biliDanmuAuto.reload(tem.pop(biliTime.tostr(biliTime.getDate(da+now*24*3600))),mri,ns)
                    rr=True
                    if read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        rr2=True
                if (not rr) or (rr and rr2) :
                    if (not rr) :
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,data['page'][c-1]['cid'],mri,ip)
                        if read==-1 :
                            return -3
                    while read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        #if ns:
                            #print('尝试抓取了%s的弹幕，获取到%s条有效弹幕，未防止遗漏，间隔时间减半' % (biliTime.tostr(biliTime.getDate(da+now*24*3600)),read['l']))
                        tem[biliTime.tostr(biliTime.getDate(da+now*24*3600))]=read
                        now=now/2
                        if now<1 :
                            now=1
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,data['page'][c-1]['cid'],mri,ip)
                        if read==-1 :
                            return -3
                        now2=now
                    if read['l']<ma*0.5 :
                        now2=now*2
                        if now2>365 :
                            now2=365
                l=read['l']
                g=0
                mri2=read['m']
                if ns:
                    print(lan['OUTPUT12'])#正在处理……
                for i in read['d']['list'] :
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                    elif xml==1:
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                                return -3
                bs2=True
                while bs2 and biliTime.equal(biliTime.getDate(da+(now2+now)*24*3600),biliTime.getNowDate())>=0 :
                    if allok :
                        read=biliDanmuAuto.getnownumber(d3,mri2)
                    else :
                        read=biliDanmuAuto.getnownumber(d2,mri2)
                    if read['l']==read['m'] :
                        now2=now2/2
                        if now2<1 :
                            now2=1
                    else :
                        bs2=False
            m=l-g
            zl=zl+l
            zm=zm+m
            zg=zg+g
            if ns:
                print(lan['OUTPUT13'].replace('<number>',f"{l}({zl})"))#获取了<number>条弹幕。
            if xml==1 and ns:
                print(lan['OUTPUT14'].replace('<number>',f"{g}({zg})"))#过滤了<number>条弹幕。
                print(lan['OUTPUT15'].replace('<number>',f"{m}({zm})"))#实际输出了<number>条弹幕。
            if t2==0 or t1-t2<2 :
                time.sleep(2)
            t2=t1
            if not at2:
                da=da+at*3600*24
            elif fir:
                fir=False
            else :
                da=da+now*3600*24
                now=now2
            mri=mri2
        if not allok:
            if ns:
                print(lan['OUTPUT16'])#开始处理最新的弹幕……
            l=0
            g=0
            for i in d2['list'] :
                if int(mri)<int(i['ri']) :
                    l=l+1
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                    elif xml==1 :
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                return -3
            try :
                f2.write('</i>')
                f2.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                return -3
            m=l-g
            zl=zl+l
            zg=zg+g
            zm=zm+m
            if ns:
                print(lan['OUTPUT17'].replace('<number>',str(l)))#在最新弹幕中获取新弹幕<number>条。
            if xml==1 and ns :
                print(lan['OUTPUT14'].replace('<number>',str(g)))#过滤了<number>条弹幕。
                print(lan['OUTPUT15'].replace('<number>',str(m)))#实际输出了<number>条弹幕。
            if ns:
                print(lan['OUTPUT18'].replace('<number>',str(zl)))#总共获取了<number>条弹幕
            if xml==1 and ns:
                print(lan['OUTPUT3'].replace('<number>',str(zg)))#共计过滤<number>条弹幕。
                print(lan['OUTPUT4'].replace('<number>',str(zm)))#实际输出<number>条弹幕。
        else :
            if xml==2 :
                try :
                    f2.write(d2)
                    f2.close()
                except :
                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                    return -3
            if xml==1 :
                z=len(d3['list'])
                g=0
                for i in d3['list'] :
                    read=biliDanmuXmlFilter.Filter(i,xmlc)
                    if read :
                        g=g+1
                    else :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                try :
                    f2.close()
                except :
                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                    return -3
                m=z-g
                if ns:
                    print(lan['OUTPUT13'].replace('<number>',str(z)))#获取了<number>条弹幕。
                    print(lan['OUTPUT14'].replace('<number>',str(g)))#过滤了<number>条弹幕。
                    print(lan['OUTPUT15'].replace('<number>',str(m)))#实际输出了<number>条弹幕。
        return 0
    elif t=='ss' :
        bs=True
        at2=False
        if not che :
            pubt=data['mediaInfo']['time'][0:10]
        else :
            pubt=biliTime.tostr2(c['time'])[0:10]
        fi=True
        jt=False
        if getset(se,'jt')==True :
            jt=True
        if 'jts' in ip :
            pubt=ip['jts']
        while bs :
            if fi and 'jt' in ip:
                fi=False
                at=ip['jt']
            elif jt :
                at='a'
            elif ns:
                at=input(lan['INPUT5'].replace('<value>','1-365').replace('<date>',str(pubt)))#请输入两次抓取之间的天数（有效值为<value>，输入a会启用自动模式（推荐），输入b可手动输入开始抓取的日期，日期目前为<date>）：
            else :
                print(lan['ERROR7'])#请使用"--jt <number>|a|b"来设置两次抓取之间的天数
                return -1
            if at.isnumeric() and int(at)<=365 and int(at)>=1 :
                at=int(at)
                bs=False
            elif len(at)>0 and at[0].lower()=='a' :
                at2=True
                at=1
                bs=False
            elif len(at)>0 and at[0].lower()=='b' :
                if not ns:
                    print(lan['ERROR8'])#请使用"--jts <date>"来修改抓取开始时间。
                    return -1
                at3=input(lan['INPUT6'])#请输入日期（格式为年-月-日，例如1989-02-25）：
                if len(at3)>0 :
                    if biliTime.checktime(at3) :
                        pubt=time.strftime('%Y-%m-%d',time.strptime(at3,'%Y-%m-%d'))
                    else :
                        print(lan['ERROR9'])#输入格式有误或者该日期不存在。
        pubt=biliTime.mkt(time.strptime(pubt,'%Y-%m-%d'))
        da=int(pubt)
        pat=o+file.filtern('%s(SS%s)' % (data['mediaInfo']['title'],data['mediaInfo']['ssId']))
        try :
            if not exists(pat) :
                mkdir(pat)
        except :
            print(lan['ERROR3'].replace('<dirname>',pat))#创建文件夹<dirname>失败。
            return -1
        if c['s']=='e' :
            filen='%s/%s' %(pat,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        else :
            filen='%s/%s' %(pat,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['title'],c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        if exists(filen) :
            fg=False
            bs=True
            if not ns:
                fg=True
                bs=False
            if 'y' in ip:
                if ip['y']:
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)？")#文件"<filename>"已存在，是否覆盖？
                if inp[0].lower()=='y' :
                    bs=False
                    fg=True
                elif inp[0].lower()=='n' :
                    bs=False
            if fg :
                try :
                    remove(filen)
                except :
                    print(lan['ERROR4'])#删除原有文件失败，跳过下载
                    return -2
            else :
                return -2
        zl=0
        zg=0
        zm=0
        now=1
        now2=now
        if ns:
            print(lan['OUTPUT5'])#正在抓取最新弹幕……
        d2=biliDanmuDown.downloadn(c['cid'],r)
        if d2==-1 :
            print(lan['ERROR1'])#网络错误！
            exit()
        filen2="Temp/a_"+str(c['cid'])+".xml"
        if exists(filen2) :
            remove(filen2)
        try :
            f=open(filen2,mode='w',encoding='utf8')
            f.write(d2)
            f.close()
        except :
            print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
            return -3
        d3=biliDanmuXmlParser.loadXML(filen2)
        remove(filen2)
        ma=int(d3['maxlimit'])
        allok=False
        if len(d3['list'])<ma-10 :
            bs=True
            if not ns:
                bs=False
            while bs :
                sts=input(f"{lan['INPUT3'].replace('<number>',str(len(d3['list']))).replace('<limit>',str(ma))}(y/n)")
                if len(sts)>0 :
                    if sts[0].lower()=='y' :
                        bs=False
                    elif sts[0].lower()=='n' :
                        allok=True
                        bs=False
        if not allok :
            d2=d3
            if ns:
                print(lan['OUTPUT6'].replace('<number>',str(len(d2['list']))))#抓取到<number>条弹幕，最新弹幕将在最后处理
        try :
            f2=open(filen,mode='w',encoding='utf8')
        except :
            print(lan['ERROR5'].replace('<filename>',filen))#打开文件"<filename>"失败
            return -3
        if not allok :
            try :
                f2.write('<?xml version="1.0" encoding="UTF-8"?>')
                f2.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d2['chatserver'],d2['chatid'],d2['mission'],d2['maxlimit'],d2['state'],d2['real_name'],d2['source']))
            except :
                print(lan['ERROR6'].replace('<filename>',filen))#保存文件失败
                return -3
        mri=0
        mri2=0
        t1=0
        t2=0
        tem={}
        fir=True
        while not allok and biliTime.equal(biliTime.getDate(da),biliTime.getNowDate())<0 and ((not at2) or (at2 and biliTime.equal(biliTime.getDate(da+now*24*3600),biliTime.getNowDate())<0)) :
            t1=time.time()
            if (not at2) or fir :
                if ns:
                    print(lan['OUTPUT7'].replace('<date>',biliTime.tostr(biliTime.getDate(da))))#正在抓取<date>的弹幕……
                bs=True
                ts=300
                rec=0
                while bs :
                    read=downloadh(filen2,r,c['cid'],da)
                    if read==-1 :
                        return -3
                    elif read==-3:
                        rec=rec+1
                        if rec%5!=0 :
                            time.sleep(5)
                            print(lan['OUTPUT8'].replace('<number>',str(rec)))#正在进行第<number>次重连
                        else :
                            bss=True
                            while bss:
                                inn=input(f"{lan['INPUT4'].replace('<number>',str(rec))}(y/n)")#是否重连？（已经失败<number>次）
                                if len(inn)>0 and inn[0].lower()=='y' :
                                    time.sleep(5)
                                    print(lan['OUTPUT8'].replace('<number>',str(rec)))#正在进行第<number>次重连
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
                                print(lan['OUTPUT9'].replace('<number>',str(ts)))#休眠<number>s
                                time.sleep(ts)
                                ts=ts+300
                        else :
                            print(obj)
                            print(lan['OUTPUT9'].replace('<number>',str(ts)))#休眠<number>s
                            time.sleep(ts)
                            ts=ts+300
                    else :
                        bs=False
                d=read
                l=0
                g=0
                if ns:
                    print(lan['OUTPUT10'])#正在处理弹幕……
                for i in d['list'] :
                    if mri2<int(i['ri']) :
                        mri2=int(i['ri'])
                    if mri<int(i['ri']) :
                        l=l+1
                        if xml==2 :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                return -3
                        elif xml==1 :
                            read=biliDanmuXmlFilter.Filter(i,xmlc)
                            if read :
                                g=g+1
                            else :
                                try :
                                    f2.write(biliDanmuCreate.objtoxml(i))
                                except :
                                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                    return -3
            else :
                rr=False
                rr2=False
                if biliTime.tostr(biliTime.getDate(da+now*24*3600)) in tem :
                    if ns:
                        print(lan['OUTPUT11'].replace('<date>',biliTime.tostr(biliTime.getDate(da+now*24*3600))))#从内存中获取了<date>的弹幕。
                    read=biliDanmuAuto.reload(tem.pop(biliTime.tostr(biliTime.getDate(da+now*24*3600))),mri,ns)
                    rr=True
                    if read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        rr2=True
                if (not rr) or (rr and rr2) :
                    if (not rr) :
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,c['cid'],mri,ip)
                        if read==-1 :
                            return -3
                    while read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        #if ns:
                            #print('尝试抓取了%s的弹幕，获取到%s条有效弹幕，未防止遗漏，间隔时间减半' % (biliTime.tostr(biliTime.getDate(da+now*24*3600)),read['l']))
                        tem[biliTime.tostr(biliTime.getDate(da+now*24*3600))]=read
                        now=now/2
                        if now<1 :
                            now=1
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,c['cid'],mri,ip)
                        if read==-1 :
                            return -3
                        now2=now
                    if read['l']<ma*0.5 :
                        now2=now*2
                        if now2>365 :
                            now2=365
                l=read['l']
                g=0
                mri2=read['m']
                if ns:
                    print(lan['OUTPUT12'])#正在处理……
                for i in read['d']['list'] :
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                    elif xml==1:
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                                return -3
                bs2=True
                while bs2 and biliTime.equal(biliTime.getDate(da+(now2+now)*24*3600),biliTime.getNowDate())>=0 :
                    if allok :
                        read=biliDanmuAuto.getnownumber(d3,mri2)
                    else :
                        read=biliDanmuAuto.getnownumber(d2,mri2)
                    if read['l']==read['m'] :
                        now2=now2/2
                        if now2<1 :
                            now2=1
                    else :
                        bs2=False
            m=l-g
            zl=zl+l
            zm=zm+m
            zg=zg+g
            if ns:
                print(lan['OUTPUT13'].replace('<number>',f"{l}({zl})"))#获取了<number>条弹幕。
            if xml==1 and ns:
                print(lan['OUTPUT14'].replace('<number>',f"{g}({zg})"))#过滤了<number>条弹幕。
                print(lan['OUTPUT15'].replace('<number>',f"{m}({zm})"))#实际输出了<number>条弹幕。
            if t2==0 or t1-t2<2 :
                time.sleep(2)
            t2=t1
            if not at2:
                da=da+at*3600*24
            elif fir:
                fir=False
            else :
                da=da+now*3600*24
                now=now2
            mri=mri2
        if not allok:
            if ns:
                print(lan['OUTPUT16'])#开始处理最新的弹幕……
            l=0
            g=0
            for i in d2['list'] :
                if int(mri)<int(i['ri']) :
                    l=l+1
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                    elif xml==1 :
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                                return -3
            try :
                f2.write('</i>')
                f2.close()
            except :
                print(lan['ERROR2'].replace('<filename>',filen2))#写入到文件"<filename>"时失败！
                return -3
            m=l-g
            zl=zl+l
            zg=zg+g
            zm=zm+m
            if ns:
                print(lan['OUTPUT17'].replace('<number>',str(l)))#在最新弹幕中获取新弹幕<number>条。
            if xml==1 and ns:
                print(lan['OUTPUT14'].replace('<number>',str(g)))#过滤了<number>条弹幕。
                print(lan['OUTPUT15'].replace('<number>',str(m)))#实际输出了<number>条弹幕。
            if ns:
                print(lan['OUTPUT18'].replace('<number>',str(zl)))#总共获取了<number>条弹幕
            if xml==1 and ns:
                print(lan['OUTPUT3'].replace('<number>',str(zg)))#共计过滤<number>条弹幕。
                print(lan['OUTPUT4'].replace('<number>',str(zm)))#实际输出<number>条弹幕。
        else :
            if xml==2 :
                try :
                    f2.write(d2)
                    f2.close()
                except :
                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                    return -3
            if xml==1 :
                z=len(d3['list'])
                g=0
                for i in d3['list'] :
                    read=biliDanmuXmlFilter.Filter(i,xmlc)
                    if read :
                        g=g+1
                    else :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                            return -3
                try :
                    f2.close()
                except :
                    print(lan['ERROR2'].replace('<filename>',filen))#写入到文件"<filename>"时失败！
                    return -3
                m=z-g
                if ns:
                    print(lan['OUTPUT13'].replace('<number>',str(z)))#获取了<number>条弹幕。
                    print(lan['OUTPUT14'].replace('<number>',str(g)))#过滤了<number>条弹幕。
                    print(lan['OUTPUT15'].replace('<number>',str(m)))#实际输出了<number>条弹幕。
        return 0