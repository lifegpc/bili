import requests
import HTMLParser
import JSONParser
import PrintInfo
import biliLogin
import biliPlayerXmlParser
import biliDanmu
import biliTime
import chon
import videodownload
import biliBv
from re import search,I
import os 
import sys
from command import gopt
import json
from math import ceil
from dictcopy import copyip,copydict
from biliHdVideo import getninfo
def main(ip={}):
    se=JSONParser.loadset()
    if not isinstance(se,dict) :
        se=None
    if 'i' in ip :
        inp=ip['i']
    else :
        inp=input("请输入av号（支持SS、EP号，BV号请以BV开头，现在已支持链接，支持收藏夹链接）：")
    av=False
    ss=False
    ep=False
    pl=False #收藏夹
    hd=False #互动视频
    uid=-1 #收藏夹主人id
    fid=-1 #收藏夹id
    if inp[0:2].lower()=='ss' and inp[2:].isnumeric() :
        s="https://www.bilibili.com/bangumi/play/ss"+inp[2:]
        ss=True
    elif inp[0:2].lower()=='ep' and inp[2:].isnumeric() :
        s="https://www.bilibili.com/bangumi/play/ep"+inp[2:]
        ep=True
    elif inp[0:2].lower()=='av' and inp[2:].isnumeric() :
        s="https://www.bilibili.com/video/av"+inp[2:]
        av=True
    elif inp[0:2].lower()=='bv' :
        inp=str(biliBv.debv(inp))
        s="https://www.bilibili.com/video/av"+inp
        av=True
    elif inp.isnumeric() :
        s="https://www.bilibili.com/video/av"+inp
        av=True
    else :
        re=search(r'([^:]+://)?(www.)?(space.)?bilibili.com/(video/av([0-9]+))?(video/(bv[0-9A-Z]+))?(bangumi/play/(ss[0-9]+))?(bangumi/play/(ep[0-9]+))?(([0-9]+)/favlist(\?fid=([0-9]+))?)?',inp,I)
        if re==None :
            re=search(r'([^:]+://)?(www.)?b23.tv/(av([0-9]+))?(bv[0-9A-Z]+)?(ss[0-9]+)?(ep[0-9]+)?',inp,I)
            if re==None :
                print('输入有误')
                exit()
            else :
                re=re.groups()
                if re[3] :
                    inp=re[3]
                    s="https://www.bilibili.com/video/av"+inp
                    av=True
                elif re[4] :
                    inp=str(biliBv.debv(re[4]))
                    s="https://www.bilibili.com/video/av"+inp
                    av=True
                elif re[5] :
                    inp=re[5]
                    s="https://www.bilibili.com/bangumi/play/"+inp
                    ss=True
                elif re[6] :
                    inp=re[6]
                    s="https://www.bilibili.com/bangumi/play/"+inp
                    ep=True
                else :
                    print('输入有误')
                    exit()
        else :
            re=re.groups()
            if re[4] :
                inp=re[4]
                s="https://www.bilibili.com/video/av"+inp
                av=True
            elif re[6] :
                inp=str(biliBv.debv(re[6]))
                s="https://www.bilibili.com/video/av"+inp
                av=True
            elif re[8] :
                inp=re[8]
                s="https://www.bilibili.com/bangumi/play/"+inp
                ss=True
            elif re[10] :
                inp=re[10]
                s="https://www.bilibili.com/bangumi/play/"+inp
                ep=True
            elif re[12] :
                pl=True
                uid=int(re[12])
                if re[14] :
                    fid=int(re[14])
                print()
            else :
                print('输入有误')
                exit()
    section=requests.session()
    section.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36","Connection": "keep-alive","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Language": "zh-CN,zh;q=0.8"})
    read=JSONParser.loadcookie(section)
    login=0
    if read==0 :
        read=biliLogin.tryok(section)
        if read==True :
            print("登录校验成功！")
            login=1
        elif read==False :
            print('网络错误！校验失败！')
            exit()
        else :
            print("登录信息已过期！")
            login=2
    elif read==-1 :
        login=2
    else :
        print("文件读取错误！")
        login=2
    if login==2 :
        if os.path.exists('cookies.json') :
            os.remove('cookies.json')
        read=biliLogin.login(section)
        if read==0 :
            login=1
        elif read==1 :
            exit()
        else :
            exit()
    if pl :
        if fid==-1 :
            re=section.get('https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=%s&jsonp=jsonp'%(uid))
            re.encoding='utf8'
            re=re.json()
            if re['code']!=0 :
                print('%s %s'%(re['code'],re['message']))
                return -1
            else :
                if 'data' in re and 'list' in re['data'] and re['data']['count']>0:
                    fid=re['data']['list'][0]['fid']
                else :
                    print('获取收藏夹列表失败')
                    return -1
        i=1
        re=JSONParser.getpli(section,fid,i)
        if re==-1 :
            return -1
        pli=JSONParser.getplinfo(re)
        PrintInfo.printInfo3(pli)
        n=ceil(pli['count']/20)
        plv=[]
        JSONParser.getpliv(plv,re)
        while i<n :
            i=i+1
            re=JSONParser.getpli(section,fid,i)
            if re==-1 :
                return -1
            JSONParser.getpliv(plv,re)
        if len(plv)!=pli['count'] :
            print('视频数量不符，貌似BUG了？')
            return -1
        PrintInfo.printInfo4(plv)
        bs=True
        f=True
        while bs:
            if f and 'p' in ip:
                f=False
                inp=ip['p']
            else :
                inp=input('请输入你想下载的视频编号，每两个编号间用,隔开，全部下载可输入a')
            cho=[]
            if inp[0]=='a' :
                print('您全选了所有视频')
                for i in range(1,pli['count']+1) :
                    cho.append(i)
                bs=False
            else :
                inp=inp.split(',')
                bb=True
                for i in inp :
                    if i.isnumeric() and int(i)>0 and int(i)<=pli['count'] and (not (int(i) in cho)) :
                        cho.append(int(i))
                    else :
                        bb=False
                if bb :
                    bs=False
                    for i in cho :
                        print("您选中了第"+str(i)+"个视频："+plv[i-1]['title'])
        bs=True
        c1=False
        read=JSONParser.getset(se,'da')
        if read!=None :
            c1=read
            bs=False
        if 'da' in ip :
            c1=ip['da']
            bs=False
        while bs :
            inp=input("是否自动下载每一个视频的所有分P？(y/n)")
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    c1=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        for i in cho:
            ip2=copyip(ip)
            ip2['i']=str(plv[i-1]['id'])
            if c1:
                ip2['p']='a'
            main(ip2)
        return 0
    xml=0
    xmlc=[]
    read=biliPlayerXmlParser.loadXML()
    if read==-1 :
        xml=2
    else :
        xml=1
        xmlc=read
    if xml==1 :
        bs=True
        read=JSONParser.getset(se,'dmgl')
        if read==True :
            bs=False
        elif read==False :
            bs=False
            xml=2
        if 'dm' in ip :
            if ip['dm']:
                bs=False
                xml=1
            else :
                bs=False
                xml=2
        while bs:
            yn=input("是否启用弹幕过滤(y/n)？")
            if yn[0].lower() =='y' :
                bs=False
            if yn[0].lower() =='n' :
                bs=False
                xml=2
    re=section.get(s)
    parser=HTMLParser.Myparser()
    parser.feed(re.text)
    vd=json.loads(parser.videodata)
    if 'error' in vd and 'code' in vd['error'] and 'message' in vd['error'] :
        print('%s %s'%(vd['error']['code'],vd['error']['message']))
        return -1
    if av :
        data=JSONParser.Myparser(parser.videodata)
        if data['videos']!=len(data['page']) :
            r=requests.Session()
            r.headers=copydict(section.headers)
            read=JSONParser.loadcookie(r)
            if read!=0 :
                print("读取cookies.json出现错误")
                return -1
            r.headers.update({'referer':"https://www.bilibili.com/video/%s"%(data['bvid'])})
            r.cookies.set('CURRENT_QUALITY','116',domain='.bilibili.com',path='/')
            r.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
            r.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
            r.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
            re=r.get("https://api.bilibili.com/x/player.so?id=cid:%s&aid=%s&bvid=%s&buvid=%s"%(data['page'][0]['cid'],data['aid'],data['bvid'],r.cookies.get('buvid3')))
            re.encoding='utf8'
            rs=search(r"<interaction>(.+)</interaction>",re.text,I)
            if rs!=None :
                rs=rs.groups()[0]
                if rs!="" :
                    rs=json.loads(rs)
                    data['gv']=rs['graph_version']
                    hd=True
        if hd:
            read=getninfo(r,data)
            if read==-1 :
                return -1
        PrintInfo.printInfo(data)
        cho=[]
        if data['videos']==1 :
            cho.append(1)
        else :
            bs=True
            f=True
            while bs :
                if f and 'p' in ip :
                    f=False
                    inp=ip['p']
                else :
                    inp=input('请输入你想下载弹幕的视频编号，每两个编号间用,隔开，全部下载可输入a')
                cho=[]
                if inp[0]=='a' :
                    print('您全选了所有视频')
                    for i in range(1,data['videos']+1) :
                        cho.append(i)
                    bs=False
                else :
                    inp=inp.split(',')
                    bb=True
                    for i in inp :
                        if i.isnumeric() and int(i)>0 and int(i)<=data['videos'] and (not (int(i) in cho)) :
                            cho.append(int(i))
                        else :
                            bb=False
                    if bb :
                        bs=False
                        for i in cho :
                            print("您选中了第"+str(i)+"P："+data['page'][i-1]['part'])
        cho2=0
        bs=True
        if 'd' in ip :
            bs=False
            cho2=ip['d']
        while bs :
            inp=input('请输入你要下载的方式：\n1.当前弹幕下载\n2.全弹幕下载\n3.视频下载\n4.当前弹幕+视频下载\n5.全弹幕+视频下载')
            if inp[0].isnumeric() and int(inp[0])>0 and int(inp[0])<6 :
            	cho2=int(inp[0])
            	bs=False
        if cho2==1 or cho2==4 :
            for i in cho :
                read=biliDanmu.DanmuGetn(i,data,section,'av',xml,xmlc,ip)
                if read==-1 or read==-4 :
                    pass
                elif read==0 :
                    print('第'+str(i)+"P下载完成")
                else :
                    exit()
        if cho2==2 or cho2==5 :
            read=biliTime.equal(biliTime.getDate(data['pubdate']),biliTime.getNowDate())
            if read==0 or read==1 :
                print('不能下载该视频全弹幕！')
                exit()
            for i in cho :
                read=biliDanmu.DanmuGeta(i,data,section,'av',xml,xmlc,ip)
                if read==-2 :
                    pass
                elif read==0 :
                    print("第"+str(i)+"P下载完成")
                else :
                    exit()
        if cho2>2:
            bs=True
            cho3=False
            read=JSONParser.getset(se,'mp')
            if read==True :
                bs=False
                cho3=True
            elif read==False :
                bs=False
            if 'm' in ip :
                if ip['m'] :
                    bs=False
                    cho3=True
                else :
                    bs=False
                    cho3=False
            while bs :
                inp=input('是否要默认下载最高画质（这样将不会询问具体画质）？(y/n)')
                if len(inp) > 0:
                    if inp[0].lower()=='y' :
                        cho3=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            cho5=False
            bs=True
            read=JSONParser.getset(se,'cd')
            if read==True :
                bs=False
                cho5=True
            elif read==False:
                bs=False
            if 'ac' in ip :
                if ip['ac'] :
                    bs=False
                    cho5=True
                else :
                    bs=False
                    cho5=False
            while bs:
                inp=input('是否开启继续下载功能？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        cho5=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            for i in cho :
                read=videodownload.avvideodownload(i,s,data,section,cho3,cho5,se,ip)
    if ss or ep :
        if ep :
            epl='，仅下载输入的ep号可输入b'
        else :
            epl=''
        data=JSONParser.Myparser2(parser.videodata)
        le=PrintInfo.printInfo2(data)
        cho=[]
        if le==1:
            cho.append(1)
            cho=chon.getcho(cho,data)
        else :
            bs=True
            f=True
            while bs :
                if f and 'p' in ip :
                    inp=ip['p']
                    f=False
                else :
                    inp=input('请输入你想下载弹幕的视频编号，每两个编号间用,隔开，全部下载可输入a%s'%(epl))
                cho=[]
                if len(inp)>0:
                    if inp[0]=='a' :
                        print('你全选了所有视频')
                        for j in range(1,le+1) :
                            cho.append(j)
                        bs=False
                    elif ep and inp[0]=='b':
                        iii=1
                        co=True
                        if 'epList' in data:
                            for i in data['epList'] :
                                if i['loaded']:
                                    co=False
                                    break
                                iii=iii+1
                        if co and 'sections' in data :
                            for i in data['sections'] :
                                for j in i['epList'] :
                                    if j['loaded']:
                                        co=False
                                        break
                                    iii=iii+1
                        print(iii)
                        if not co:
                            cho.append(iii)
                            bs=False
                    else :
                        inp=inp.split(',')
                        bb=True
                        for i in inp :
                            if i.isnumeric() and int(i)<=le and int(i)>0 and (not (int(i) in cho)) :
                                cho.append(int(i))
                            else :
                                bb=False
                        if bb:
                            bs=False
                cho=chon.getcho(cho,data)
                PrintInfo.printcho(cho)
        cho2=0
        bs=True
        if 'd' in ip :
            bs=False
            cho2=ip['d']
        while bs :
            inp=input('请输入你要下载的方式：\n1.当前弹幕下载\n2.全弹幕下载\n3.视频下载\n4.当前弹幕+视频下载\n5.全弹幕+视频下载')
            if inp[0].isnumeric() and int(inp[0])>0 and int(inp[0])<6:
            	cho2=int(inp[0])
            	bs=False
        if cho2==1 or cho2==4 :
            for i in cho:
                read=biliDanmu.DanmuGetn(i,data,section,'ss',xml,xmlc,ip)
                if read==-1 or read==-4 :
                    pass
                elif read==0 :
                    print('%s下载完成' % (i['titleFormat']))
                else :
                    exit()
        if cho2==2 or cho2==5 :
            for i in cho :
                read=biliDanmu.DanmuGeta(i,data,section,'ss',xml,xmlc,ip)
        if cho2>2 :
            bs=True
            cho3=False
            read=JSONParser.getset(se,'mp')
            if read==True :
                bs=False
                cho3=True
            elif read==False :
                bs=False
            if 'm' in ip :
                if ip['m'] :
                    bs=False
                    cho3=True
                else :
                    bs=False
                    cho3=False
            while bs :
                inp=input('是否要默认下载最高画质（这样将不会询问具体画质）？(y/n)')
                if len(inp) > 0:
                    if inp[0].lower()=='y' :
                        cho3=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            cho5=False
            bs=True
            read=JSONParser.getset(se,'cd')
            if read==True :
                bs=False
                cho5=True
            elif read==False:
                bs=False
            if 'ac' in ip :
                if ip['ac'] :
                    bs=False
                    cho5=True
                else :
                    bs=False
                    cho5=False
            while bs:
                inp=input('是否开启继续下载功能？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        cho5=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            for i in cho:
                read=videodownload.epvideodownload(i,"https://bilibili.com/bangumi/play/ss%s"%(data['mediaInfo']['ssId']),data,section,cho3,cho5,se,ip)
if __name__=="__main__" :
    if len(sys.argv)==1 :
        main()
    else :
        main(gopt(sys.argv[1:]))
else :
    print("请运行根目录下的start.py")
