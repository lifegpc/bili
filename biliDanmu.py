import biliDanmuDown
from os.path import exists
from os import mkdir,remove
import biliDanmuXmlParser
import biliDanmuCreate
import biliDanmuXmlFilter
import biliTime
import time
import json
import biliLogin
import biliDanmuAuto
import file
def downloadh(filen,r,pos,da) :
    d=biliDanmuDown.downloadh(pos,r,biliTime.tostr(biliTime.getDate(da)))
    if d==-1 :
        print('网络错误！')
        return -3
    if exists(filen) :
        remove(filen)
    try :
        f=open(filen,mode='w',encoding='utf8')
        f.write(d)
        f.close()
    except:
        print('保存内容至文件失败'+filen)
        return -1
    try :
        d=biliDanmuXmlParser.loadXML(filen)
        remove(filen)
        return d
    except :
        return {'status':-2,'d':d}
def DanmuGetn(c,data,r,t,xml,xmlc) :
    "处理现在的弹幕"
    try :
        if not exists('Download') :
            mkdir('Download')
    except:
        print("创建Download文件夹失败")
        return -3
    try :
        if not exists('Temp') :
            mkdir('Temp')
    except:
        print("创建Temp文件夹失败")
        return -3
    if t=='av' :
        d=biliDanmuDown.downloadn(data['page'][c-1]['cid'],r)
        if data['videos'] ==1 :
            filen='Download/'+file.filtern(data['title']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        else :
            filen='Download/'+file.filtern(data['title']+'-'+data['page'][c-1]['part']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        if d==-1 :
            print("网络错误")
            exit()
        if exists(filen) :
            bs=True
            while bs :
                inp=input('已经有'+filen+'文件了，是否覆盖(y/n)？')
                if inp[0].lower()=='y' :
                    bs=False
                    try :
                        remove(filen)
                    except :
                        print('删除原有文件失败，跳过下载')
                        return -1
                elif inp[0].lower()=='n' :
                    bs=False
                    return -1
        if xml==2 :
            try :
                f=open(filen,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print('保存内容至文件失败'+filen)
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
                print('保存内容至文件失败'+filen2)
                return -2
            d=biliDanmuXmlParser.loadXML(filen2)
            remove(filen2)
            try :
                f=open(filen,mode='w',encoding='utf8')
            except:
                print('打开文件失败'+filen)
                return -2
            try :
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d['chatserver'],d['chatid'],d['mission'],d['maxlimit'],d['state'],d['real_name'],d['source']))
            except :
                print('保存文件失败'+filen)
                return -2
            print('总计：%s' % (len(d['list'])))
            print('正在过滤......')
            l=0
            for i in d['list'] :
                read=biliDanmuXmlFilter.Filter(i,xmlc)
                if read :
                    l=l+1
                else :
                    try :
                        f.write(biliDanmuCreate.objtoxml(i))
                    except :
                        print('保存文件失败'+filen)
                        return -2
            print('共计过滤%s条' % (l))
            print('实际输出%s条' % (len(d['list'])-l))
            try :
                f.write('</i>')
                f.close()
            except :
                print('保存文件失败'+filen)
                return -2
            return 0
    elif t=='ss' :
        d=biliDanmuDown.downloadn(c['cid'],r)
        pat='Download/'+file.filtern('%s(SS%s)' % (data['mediaInfo']['title'],data['mediaInfo']['ssId']))
        try :
            if not exists(pat) :
                mkdir(pat)
        except :
            print('创建%s失败！'%(pat))
            return -3
        if c['s']=='e' :
            filen='%s/%s' %(pat,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        else :
            filen='%s/%s' %(pat,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['title'],c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        if d==-1 :
            print('网络错误！')
            exit()
        if exists(filen) :
            bs=True
            while bs :
                inp=input('已经有'+filen+'文件了，是否覆盖(y/n)？')
                if inp[0].lower()=='y' :
                    bs=False
                    try :
                        remove(filen)
                    except :
                        print('删除原有文件失败，跳过下载')
                        return -1
                elif inp[0].lower()=='n' :
                    bs=False
                    return -1
        if xml==2 :
            try :
                f=open(filen,mode='w',encoding='utf8')
                f.write(d)
                f.close()
            except :
                print('保存内容至文件失败'+filen)
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
                print('保存内容至文件失败'+filen2)
                return -2
            d=biliDanmuXmlParser.loadXML(filen2)
            remove(filen2)
            try :
                f=open(filen,mode='w',encoding='utf8')
            except:
                print('打开文件失败'+filen)
                return -2
            try :
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d['chatserver'],d['chatid'],d['mission'],d['maxlimit'],d['state'],d['real_name'],d['source']))
            except :
                print('保存文件失败'+filen)
                return -2
            print('总计：%s' % (len(d['list'])))
            print('正在过滤......')
            l=0
            for i in d['list'] :
                read=biliDanmuXmlFilter.Filter(i,xmlc)
                if read :
                    l=l+1
                else :
                    try :
                        f.write(biliDanmuCreate.objtoxml(i))
                    except :
                        print('保存文件失败'+filen)
                        return -2
            print('共计过滤%s条' % (l))
            print('实际输出%s条' % (len(d['list'])-l))
            try :
                f.write('</i>')
                f.close()
            except :
                print('保存文件失败'+filen)
                return -2
            return 0
def DanmuGeta(c,data,r,t,xml,xmlc) :
    "全弹幕处理"
    try :
        if not exists('Download') :
            mkdir('Download')
    except:
        print("创建Download文件夹失败")
        return -1
    try :
        if not exists('Temp') :
            mkdir('Temp')
    except:
        print("创建Temp文件夹失败")
        return -1
    if t=='av' :
        bs=True
        at2=False
        while bs :
            at=input('请输入两次抓取之间的天数（1-365)，输入a启动自动模式（可能有点傻）')
            if at.isnumeric() and int(at)<=365 and int(at)>=1 :
                at=int(at)
                bs=False
            elif len(at)>0 and at[0].lower()=='a' :
                at2=True
                at=1
                bs=False
        if data['videos'] ==1 :
            filen='Download/'+file.filtern(data['title']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        else :
            filen='Download/'+file.filtern(data['title']+'-'+data['page'][c-1]['part']+"(AV"+str(data['aid'])+','+data['bvid']+',P'+str(c)+','+str(data['page'][c-1]['cid'])+").xml")
        if exists(filen) :
            bs=True
            while bs :
                inp=input('已经有'+filen+'文件了，是否覆盖(y/n)？')
                if inp[0].lower()=='y' :
                    bs=False
                    try :
                        remove(filen)
                    except :
                        print('删除原有文件失败，跳过下载')
                        return -2
                elif inp[0].lower()=='n' :
                    bs=False
                    return -2
        da=int(data['pubdate'])
        zl=0
        zg=0
        zm=0
        now=1
        now2=now
        print('正在抓取最新弹幕......')
        d2=biliDanmuDown.downloadn(data['page'][c-1]['cid'],r)
        if d2==-1 :
            print('网络错误！')
            exit()
        filen2="Temp/a_"+str(data['page'][c-1]['cid'])+".xml"
        if exists(filen2) :
            remove(filen2)
        try :
            f=open(filen2,mode='w',encoding='utf8')
            f.write(d2)
            f.close()
        except :
            print('保存内容至文件失败'+filen2)
            return -3
        d3=biliDanmuXmlParser.loadXML(filen2)
        remove(filen2)
        ma=int(d3['maxlimit'])
        allok=False
        if len(d3['list'])<ma-10 :
            bs=True
            while bs :
                sts=input('抓取到了%s条弹幕，距离限制（%s条）较远，是否继续抓取？(y/n)' % (len(d3['list']),ma))
                if len(sts)>0 :
                    if sts[0].lower()=='y' :
                        bs=False
                    elif sts[0].lower()=='n' :
                        allok=True
                        bs=False
        if not allok :
            d2=d3
            print('抓取到%s条弹幕，最新弹幕将在最后处理' % (len(d2['list'])))
        try :
            f2=open(filen,mode='w',encoding='utf8')
        except :
            print('打开文件失败'+filen)
            return -3
        if not allok :
            try :
                f2.write('<?xml version="1.0" encoding="UTF-8"?>')
                f2.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d2['chatserver'],d2['chatid'],d2['mission'],d2['maxlimit'],d2['state'],d2['real_name'],d2['source']))
            except :
                print('保存文件失败'+filen)
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
                print('正在抓取%s的弹幕......' % (biliTime.tostr(biliTime.getDate(da))))
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
                            print('5秒后将进行第%s次重连' % (rec))
                            time.sleep(5)
                        else :
                            bss=True
                            while bss:
                                inn=input('已经第%s次失败了，是否继续重连？(y/n)' % (rec))
                                if len(inn)>0 and inn[0].lower()=='y' :
                                    print('5秒后将进行第%s次重连' % (rec))
                                    time.sleep(5)
                                elif len(inn)>0 and inn[0].lower()=='n' :
                                    exit()
                    elif 'status' in read and read['status']==-2 :
                        obj=json.loads(read['d'])
                        if obj['code']==-101 :
                            if obj['message']=='账户未登录' :
                                read=biliLogin.login(r)
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
                g=0
                print('正在处理弹幕......')
                for i in d['list'] :
                    if mri2<int(i['ri']) :
                        mri2=int(i['ri'])
                    if mri<int(i['ri']) :
                        l=l+1
                        if xml==2 :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen)
                                return -3
                        elif xml==1 :
                            read=biliDanmuXmlFilter.Filter(i,xmlc)
                            if read :
                                g=g+1
                            else :
                                try :
                                    f2.write(biliDanmuCreate.objtoxml(i))
                                except :
                                    print('保存内容至文件失败'+filen)
                                    return -3
            else :
                rr=False
                rr2=False
                if biliTime.tostr(biliTime.getDate(da+now*24*3600)) in tem :
                    print('从内存中获取了%s的弹幕内容' % (biliTime.tostr(biliTime.getDate(da+now*24*3600))))
                    read=biliDanmuAuto.reload(tem.pop(biliTime.tostr(biliTime.getDate(da+now*24*3600))),mri)
                    rr=True
                    if read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        rr2=True
                if (not rr) or (rr and rr2) :
                    if (not rr) :
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,data['page'][c-1]['cid'],mri)
                        if read==-1 :
                            return -3
                    while read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        print('尝试抓取了%s的弹幕，获取到%s条有效弹幕，未防止遗漏，间隔时间减半' % (biliTime.tostr(biliTime.getDate(da+now*24*3600)),read['l']))
                        tem[biliTime.tostr(biliTime.getDate(da+now*24*3600))]=read
                        now=now/2
                        if now<1 :
                            now=1
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,data['page'][c-1]['cid'],mri)
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
                print('正在处理......')
                for i in read['d']['list'] :
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print('保存内容至文件失败'+filen)
                            return -3
                    elif xml==1:
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen2)
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
            print('获取了%s(%s)条弹幕' % (l,zl))
            if xml==1 :
                print('过滤了%s(%s)条弹幕' % (g,zg))
                print('实际输出了%s(%s)条弹幕' % (m,zm))
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
            print('开始处理当前弹幕文件......')
            l=0
            g=0
            for i in d2['list'] :
                if int(mri)<int(i['ri']) :
                    l=l+1
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print('保存内容至文件失败'+filen)
                            return -3
                    elif xml==1 :
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen)
                                return -3
            try :
                f2.write('</i>')
                f2.close()
            except :
                print('保存内容至文件失败'+filen2)
                return -3
            m=l-g
            zl=zl+l
            zg=zg+g
            zm=zm+m
            print('在当前弹幕中获取有效弹幕%s条' % (l))
            if xml==1 :
                print('过滤了%s条弹幕' % (g))
                print('实际输出了%s条弹幕' % (m))
            print('总共获取了%s条弹幕' % (zl))
            if xml==1 :
                print('这个过滤了%s条弹幕' % (zg))
                print('实际输出了%s条弹幕' % (zm))
        else :
            if xml==2 :
                try :
                    f2.write(d2)
                    f2.close()
                except :
                    print('保存内容至文件失败'+filen)
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
                            print('保存内容至文件失败'+filen)
                            return -3
                try :
                    f2.close()
                except :
                    print('保存内容至文件失败'+filen)
                    return -3
                m=z-g
                print('获取了%s条弹幕' % (z))
                print('过滤了%s条弹幕' % (g))
                print('实际输出了%s条弹幕' % (m))
        return 0
    elif t=='ss' :
        bs=True
        at2=False
        pubt=data['mediaInfo']['time'][0:10]
        while bs :
            at=input('请输入两次抓取之间的天数（1-365)，输入a启动自动模式（可能有点傻），输入b手动输入日期(当前日期：%s)' % (pubt))
            if at.isnumeric() and int(at)<=365 and int(at)>=1 :
                at=int(at)
                bs=False
            elif len(at)>0 and at[0].lower()=='a' :
                at2=True
                at=1
                bs=False
            elif len(at)>0 and at[0].lower()=='b' :
                at3=input('请按1989-02-25这样的格式输入开始日期：')
                if len(at3)>0 :
                    if biliTime.checktime(at3) :
                        pubt=time.strftime('%Y-%m-%d',time.strptime(at3,'%Y-%m-%d'))
                    else :
                        print('输入格式有误或者该日期不存在')
        pubt=biliTime.mkt(time.strptime(pubt,'%Y-%m-%d'))
        da=int(pubt)
        pat='Download/'+file.filtern('%s(SS%s)' % (data['mediaInfo']['title'],data['mediaInfo']['ssId']))
        try :
            if not exists(pat) :
                mkdir(pat)
        except :
            print('创建%s失败！'%(pat))
            return -1
        if c['s']=='e' :
            filen='%s/%s' %(pat,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        else :
            filen='%s/%s' %(pat,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s).xml' %(c['title'],c['i']+1,c['longTitle'],c['titleFormat'],c['aid'],c['bvid'],c['id'],c['cid'])))
        if exists(filen) :
            bs=True
            while bs :
                inp=input('已经有'+filen+'文件了，是否覆盖(y/n)？')
                if inp[0].lower()=='y' :
                    bs=False
                    try :
                        remove(filen)
                    except :
                        print('删除原有文件失败，跳过下载')
                        return -2
                elif inp[0].lower()=='n' :
                    bs=False
                    return -2
        zl=0
        zg=0
        zm=0
        now=1
        now2=now
        print('正在抓取最新弹幕......')
        d2=biliDanmuDown.downloadn(c['cid'],r)
        if d2==-1 :
            print('网络错误！')
            exit()
        filen2="Temp/a_"+str(c['cid'])+".xml"
        if exists(filen2) :
            remove(filen2)
        try :
            f=open(filen2,mode='w',encoding='utf8')
            f.write(d2)
            f.close()
        except :
            print('保存内容至文件失败'+filen2)
            return -3
        d3=biliDanmuXmlParser.loadXML(filen2)
        remove(filen2)
        ma=int(d3['maxlimit'])
        allok=False
        if len(d3['list'])<ma-10 :
            bs=True
            while bs :
                sts=input('抓取到了%s条弹幕，距离限制（%s条）较远，是否继续抓取？(y/n)' % (len(d3['list']),ma))
                if len(sts)>0 :
                    if sts[0].lower()=='y' :
                        bs=False
                    elif sts[0].lower()=='n' :
                        allok=True
                        bs=False
        if not allok :
            d2=d3
            print('抓取到%s条弹幕，最新弹幕将在最后处理' % (len(d2['list'])))
        try :
            f2=open(filen,mode='w',encoding='utf8')
        except :
            print('打开文件失败'+filen)
            return -3
        if not allok :
            try :
                f2.write('<?xml version="1.0" encoding="UTF-8"?>')
                f2.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (d2['chatserver'],d2['chatid'],d2['mission'],d2['maxlimit'],d2['state'],d2['real_name'],d2['source']))
            except :
                print('保存文件失败'+filen)
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
                print('正在抓取%s的弹幕......' % (biliTime.tostr(biliTime.getDate(da))))
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
                            print('5秒后将进行第%s次重连' % (rec))
                            time.sleep(5)
                        else :
                            bss=True
                            while bss:
                                inn=input('已经第%s次失败了，是否继续重连？(y/n)' % (rec))
                                if len(inn)>0 and inn[0].lower()=='y' :
                                    print('5秒后将进行第%s次重连' % (rec))
                                    time.sleep(5)
                                elif len(inn)>0 and inn[0].lower()=='n' :
                                    exit()
                    elif 'status' in read and read['status']==-2 :
                        obj=json.loads(read['d'])
                        if obj['code']==-101 :
                            if obj['message']=='账户未登录' :
                                read=biliLogin.login(r)
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
                g=0
                print('正在处理弹幕......')
                for i in d['list'] :
                    if mri2<int(i['ri']) :
                        mri2=int(i['ri'])
                    if mri<int(i['ri']) :
                        l=l+1
                        if xml==2 :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen)
                                return -3
                        elif xml==1 :
                            read=biliDanmuXmlFilter.Filter(i,xmlc)
                            if read :
                                g=g+1
                            else :
                                try :
                                    f2.write(biliDanmuCreate.objtoxml(i))
                                except :
                                    print('保存内容至文件失败'+filen)
                                    return -3
            else :
                rr=False
                rr2=False
                if biliTime.tostr(biliTime.getDate(da+now*24*3600)) in tem :
                    print('从内存中获取了%s的弹幕内容' % (biliTime.tostr(biliTime.getDate(da+now*24*3600))))
                    read=biliDanmuAuto.reload(tem.pop(biliTime.tostr(biliTime.getDate(da+now*24*3600))),mri)
                    rr=True
                    if read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        rr2=True
                if (not rr) or (rr and rr2) :
                    if (not rr) :
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,c['cid'],mri)
                        if read==-1 :
                            return -3
                    while read['z']==read['l'] and read['z']>ma-10 and now>1 :
                        print('尝试抓取了%s的弹幕，获取到%s条有效弹幕，未防止遗漏，间隔时间减半' % (biliTime.tostr(biliTime.getDate(da+now*24*3600)),read['l']))
                        tem[biliTime.tostr(biliTime.getDate(da+now*24*3600))]=read
                        now=now/2
                        if now<1 :
                            now=1
                        read=biliDanmuAuto.getMembers(filen2,r,da+now*24*3600,c['cid'],mri)
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
                print('正在处理......')
                for i in read['d']['list'] :
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print('保存内容至文件失败'+filen)
                            return -3
                    elif xml==1:
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen2)
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
            print('获取了%s(%s)条弹幕' % (l,zl))
            if xml==1 :
                print('过滤了%s(%s)条弹幕' % (g,zg))
                print('实际输出了%s(%s)条弹幕' % (m,zm))
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
            print('开始处理当前弹幕文件......')
            l=0
            g=0
            for i in d2['list'] :
                if int(mri)<int(i['ri']) :
                    l=l+1
                    if xml==2 :
                        try :
                            f2.write(biliDanmuCreate.objtoxml(i))
                        except :
                            print('保存内容至文件失败'+filen)
                            return -3
                    elif xml==1 :
                        read=biliDanmuXmlFilter.Filter(i,xmlc)
                        if read :
                            g=g+1
                        else :
                            try :
                                f2.write(biliDanmuCreate.objtoxml(i))
                            except :
                                print('保存内容至文件失败'+filen)
                                return -3
            try :
                f2.write('</i>')
                f2.close()
            except :
                print('保存内容至文件失败'+filen2)
                return -3
            m=l-g
            zl=zl+l
            zg=zg+g
            zm=zm+m
            print('在当前弹幕中获取有效弹幕%s条' % (l))
            if xml==1 :
                print('过滤了%s条弹幕' % (g))
                print('实际输出了%s条弹幕' % (m))
            print('总共获取了%s条弹幕' % (zl))
            if xml==1 :
                print('这个过滤了%s条弹幕' % (zg))
                print('实际输出了%s条弹幕' % (zm))
        else :
            if xml==2 :
                try :
                    f2.write(d2)
                    f2.close()
                except :
                    print('保存内容至文件失败'+filen)
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
                            print('保存内容至文件失败'+filen)
                            return -3
                try :
                    f2.close()
                except :
                    print('保存内容至文件失败'+filen)
                    return -3
                m=z-g
                print('获取了%s条弹幕' % (z))
                print('过滤了%s条弹幕' % (g))
                print('实际输出了%s条弹幕' % (m))
        return 0