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
import requests
import JSONParser
import json
import file
import time
import os
from dictcopy import copydict,copylist
from re import search
from requests.structures import CaseInsensitiveDict
from biliTime import tostr2
import bstr
from biliSub import downsub,ffinputstr
from file import mkdir
from dict import delli,dellk
import platform
from command import gopt
from lang import getlan,getdict
import sys
import JSONParser2
#https://api.bilibili.com/x/player/playurl?cid=<cid>&qn=<图质大小>&otype=json&avid=<avid>&fnver=0&fnval=16 番剧也可，但不支持4K
#https://api.bilibili.com/pgc/player/web/playurl?avid=<avid>&cid=<cid>&bvid=&qn=<图质大小>&type=&otype=json&ep_id=<epid>&fourk=1&fnver=0&fnval=16&session= 貌似仅番剧
#result -> dash -> video/audio -> [0-?](list) -> baseUrl/base_url
# session = md5(String((getCookie('buvid3') || Math.floor(Math.random() * 100000).toString(16)) + Date.now()));
#第二个需要带referer，可以解析4K
lan=None
se=JSONParser.loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('videodownload',getlan(se,ip))


def getqualitytrans(t: str) -> str:
    "返回画质的翻译"
    if t in lan:
        return lan[t]
    print(lan['NO_QUA_TRANS'].replace('<value>', t))
    return t


def getqualitytransl(l: list) -> list:
    r = []
    for i in l:
        r.append(getqualitytrans(i))
    return r


def getfps(s:str)->str:
    "解析B站API返回的fps"
    if s.isnumeric() :
        return s+"fps"
    else :
        r=search(r"([0-9]+)/([0-9]+)",s)
        if r!=None :
            r=r.groups()
            return "%.3f(%s)fps"%(int(r[0])/int(r[1]),s)
        else :
            return ""
def getnul():
    "获取不输出stdout的命令行"
    s=platform.system()
    if s=="Windows":
        return " 2>&0 1>&0"
    elif s=="Linux" :
        return " > /dev/null 2>&1"
    else :
        return " 2>&0 1>&0"
def geth(h:CaseInsensitiveDict) :
    s=''
    for i in h.keys() :
        s=s+' --header "'+i+': '+h[i]+'"'
    return s
def dwaria2(r,fn,url,size,d2,ip,se,i=1,n=1,d=False) :
    if d :
        print(lan['OUTPUT1'].replace('<i>',str(i)).replace('<count>',str(n)))#正在开始下载第<i>个文件，共<count>个文件
    else :
        print(lan['OUTPUT2'])#正在开始下载
    (fn1,fn2)=file.spfln(fn)
    cm='aria2c --auto-file-renaming=false'+geth(r.headers)+' -o "'+fn2+'" -d "'+fn1+'"'
    arc=3
    read=JSONParser.getset(se,'ax')
    if read!=None :
        arc=read
    if 'ax' in ip:
        arc=ip['ax']
    ars=5
    read=JSONParser.getset(se,'as')
    if read!=None :
        ars=read
    if 'as' in ip:
        ars=ip['as']
    arfa='prealloc'
    if 'fa' in se:
        arfa=se['fa']
    if 'fa' in ip:
        arfa=ip['fa']
    ark=5
    read=JSONParser.getset(se,'ak')
    if read!=None:
        ark=read
    if 'ak' in ip:
        ark=ip['ak']
    ms="0"
    read=JSONParser.getset(se,'ms')
    if read!=None :
        ms=read
    if 'ms' in ip:
        ms=ip['ms']
    xs=""
    if ms!="0" :
        xs=lan['OUTPUT4'].replace('<value>',ms)#，限速为<value>
    asd=True
    if JSONParser.getset(se,'cad')==True :
        asd=False
    if 'cad' in ip:
        asd=not ip['cad']
    if asd:
        asd="true"
    else :
        asd="false"
    print(lan['OUTPUT3'].replace('<value1>',str(ars)).replace('<value2>',str(arc)).replace('<value3>',str(ark)).replace('<value4>',arfa).replace('<maxspeed>',xs))#单文件最大<value1>个连接，单个服务器最大<value2>个连接，文件分片大小<value3>M，预分配方式为<value4><maxspeed>
    cm=cm+' -x '+str(arc)
    cm=cm+' -s '+str(ars)
    cm=cm+' --file-allocation='+arfa
    cm=cm+' -k %sM'%(ark)
    cm=cm+' --max-overall-download-limit='+ms
    cm=cm+' --async-dns='+asd
    if 'ahttpproxy' in ip:
        cm=cm+' --http-proxy='+ip['ahttpproxy']
    if 'ahttpsproxy' in ip:
        cm=cm+' --https-proxy='+ip['ahttpsproxy']
    if os.path.exists(fn) :
        oa=os.path.exists('%s.aria2'%(fn))
        if oa :
            s=lan['OUTPUT5']#(发现aria2文件，建议覆盖)
        else :
            s=""
        bs=True
        fg=False
        if d2 and not oa :
            print(lan['OUTPUT6'])#未找到aria2文件，跳过下载
            return 0
        if d2 and oa :
            cm=cm+' -c'
        if not d2 and ('y' in ip or 's' in ip):
            if 's' in ip:
                fg=True
                bs=False
            if 'y' in ip:
                if ip['y'] :
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
        while bs and not d2 :
            inp=input(f'{lan["INPUT1"].replace("<filename>",fn)}{s}(y/n)')#"<filename>"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y':
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if not d2 and fg :
            try :
                os.remove(fn)
            except :
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return 0
        elif not d2:
            return 0
    if isinstance(url,str) :
        cm=cm+' "'+url+'"'
    elif isinstance(url,list) :
        for i in url :
            cm=cm+' "'+i+'"'
    re=os.system(cm)
    if re==0 :
        return 0
    elif re==28 :
        return -3
    else :
        return -2
def geturll(d):
    l=[]
    def isp(u,l) :
        for i in l:
            if u==i :
                return False
        return True
    if 'url' in d :
        l.append(d['url'])
    if 'base_url' in d:
        l.append(d['base_url'])
    if 'video_playurl' in d:
        l.append(d['video_playurl'])
    if 'backup_url' in d and d['backup_url']!=None :
        for i in d['backup_url'] :
            if isp(i,l) :
                l.append(i)
    if 'backup_playurl' in d and d['backup_playurl']!=None :
        for i in d['backup_playurl'] :
            if isp(i,l) :
                l.append(i)
    return l
def tim() :
    "返回当前时间（毫秒）"
    return int(time.time()*1000)
def sea(s:str,avq:list) :
    t=search('^[0-9]+',s)
    if t :
        t=int(t.group())
        k=0
        for i in avq :
            if i==t :
                break
            k=k+1
        return k
def sev(s:str) :
    t=search('^[0-9]+(.+)',s)
    if t:
        return t.groups()[0]
    return ""
def avvideodownload(i,url,data,r,c,c3,se,ip,ud) :
    """下载av号视频
    -1 cookies.json读取错误
    -2 API Error
    -3 下载错误
    -4 aria2c参数错误
    -5 文件夹创建失败
    -6 缺少必要参数"""
    ns=True
    if 's' in ip:
        ns=False
    bp=False #删除无用文件时是否保留封面图片
    if JSONParser.getset(se,'bp')==True :
        bp=True
    if 'bp' in ip:
        bp=ip['bp']
    nte=False
    if JSONParser.getset(se,'te')==False :
        nte=True
    if 'te' in ip:
        nte=not ip['te']
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    dmp = False  # 是否为多P视频创建单独文件夹
    if JSONParser.getset(se, 'dmp') == True:
        dmp = True
    if 'dmp' in ip:
        dmp = ip['dmp']
    if data['videos'] == 1:
        dmp = False
    F=False #仅输出视频信息
    if 'F' in ip:
        F=True
    fin=True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    if dmp:
        if not fin:
            o = f"{o}{file.filtern(data['title'])}/"
        else:
            o = "%s%s/" % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']})"))
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败
        return -5
    nbd=True
    if JSONParser.getset(se,'bd')==True :
        nbd=False
    if 'bd' in ip:
        nbd=not ip['bd']
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    if i>1:
        url="%s?p=%s"%(url,i)
    r2.headers.update({'referer':url})
    r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    re=r2.get(url)
    re.encoding='utf8'
    rs=search('__playinfo__=([^<]+)',re.text)
    napi=True #新api
    if rs!=None :
        re=json.loads(rs.groups()[0])
    elif data['videos']>=1 :
        uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=%s&otype=json&bvid=%s&fnver=0&fnval=16"%(data['page'][i-1]['cid'],120,data['bvid'])
        re=r2.get(uri)
        re.encoding="utf8"
        re=re.json()
        if re["code"]!=0 :
            print({"code":re["code"],"message":re["message"]})
            return -2
        napi=False
    else :
        return -2
    rr=r2.get("https://api.bilibili.com/x/player.so?id=cid:%s&aid=%s&bvid=%s&buvid=%s"%(data['page'][i-1]['cid'],data['aid'],data['bvid'],r.cookies.get('buvid3')))
    rr.encoding='utf8'
    rs2=search(r'<subtitle>(.+)</subtitle>',rr.text)
    if F:
        print(f"{lan['OUTPUT8'].replace('<number>',str(i))}{data['page'][i-1]['part']}")#第<number>P：
    if rs2!=None :
        rs2=json.loads(rs2.groups()[0])
        JSONParser2.getsub(rs2,data)
    if "data" in re and "durl" in re['data']:
        vq=re["data"]["quality"]
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq=re["data"]["accept_quality"]
        durl={vq:re["data"]['durl']}
        durz={}
        vqs=""
        if not c or F:
            j=0
            for l in avq :
                if not l in durl :
                    if napi:
                        r2.cookies.set('CURRENT_QUALITY',str(l),domain='.bilibili.com',path='/')
                        re=r2.get(url)
                        re.encoding='utf8'
                        rs=search('__playinfo__=([^<]+)',re.text)
                        if rs!=None :
                            re=json.loads(rs.groups()[0])
                        else :
                            return -2
                    else :
                        uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=%s&otype=json&bvid=%s&fnver=0&fnval=16"%(data['page'][i-1]['cid'],l,data['bvid'])
                        re=r2.get(uri)
                        re.encoding='utf8'
                        re=re.json()
                        if re["code"]!=0 :
                            print({"code":re["code"],"message":re["message"]})
                            return -2
                    durl[re["data"]['quality']]=re['data']['durl']
                if ud['vip']<1 and (l>80 or l==74) :
                    avq,ii=delli(avq,l)
                    if ii>-1 :
                        vqd=dellk(vqd,ii)
                    continue
                if ns or(not ns and F):
                    print(f"{j+1}.{lan['OUTPUT9']}{vqd[j]}")#图质：
                j=j+1
                size=0
                for k in durl[l] :
                    size=size+k['size']
                durz[l]=size
                if ns or(not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(size)}({size}B,{file.cml(size,re['data']['timelength'])})")#大小：
            r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
            if F :
                return 0
            bs=True
            fi=True
            while bs :
                if fi and 'v' in ip :
                    fi=False
                    inp=ip['v']
                elif ns :
                    inp=input(lan['INPUT2'])#请选择画质：
                else :
                    print(lan['ERROR3'])#请使用"-v <id>"选择画质
                    return -6
                if len(inp) > 0 and inp.isnumeric() and int(inp)>0 and int(inp)<len(avq)+1 :
                    durl=durl[avq[int(inp)-1]]
                    durz=durz[avq[int(inp)-1]]
                    vq=avq[int(inp)-1]
                    bs=False
            if ns:
                print(lan['OUTPUT11'].replace('<videoquality>',vqd[int(inp)-1]))#已选择<videoquality>画质
            vqs=vqd[int(inp)-1]
        else :
            j=0
            for l in avq :
                if l==vq :
                    if ns:
                        print(f"{lan['OUTPUT9']}{vqd[j]}")#画质：
                    vqs=vqd[j]
                    break
                j=j+1
            durz=0
            for k in durl[vq] :
                durz=durz+k['size']
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(durz)}({durz}B,{file.cml(durz,re['data']['timelength'])})")#大小：
            durl=durl[vq]
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if data['videos']==1 :
            if not fin:
                filen=f"{o}{file.filtern(data['title'])}"
            elif sv:
                filen='%s%s'%(o,file.filtern('%s(AV%s,%s,P%s,%s,%s)'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'],vqs)))
            else :
                filen='%s%s'%(o,file.filtern('%s(AV%s,%s,P%s,%s)'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'])))
        else :
            if not fin and not dmp:
                filen=f"{o}{file.filtern(data['title'])}-{i}.{file.filtern(data['page'][i-1]['part'])}"
            elif not fin and dmp:
                filen = f"{o}{i}.{file.filtern(data['page'][i - 1]['part'])}"
            elif sv and not dmp:
                filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs})"))
            elif not dmp:
                filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']})"))
            elif sv:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs})"))
            else:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']})"))
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        ma=False
        if JSONParser.getset(se,"ma")==True :
            ma=True
        if 'ma' in ip:
            ma=ip['ma']
        if ff and (len(durl)>1 or ma) and os.path.exists('%s.mkv'%(filen)) and os.system('ffmpeg -h%s'%(getnul()))==0 :
            fg=False
            bs=True
            if not ns:
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
                inp=input(f"{lan['INPUT1'].replace('<filename>','%s.mkv'%(filen))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove('%s.mkv'%(filen))
                except :
                    print(lan['OUTPUT7'])
                    return 0
            else:
                return 0
        if ns:
            print(lan['OUTPUT12'].replace('<number>',str(len(durl))))#共有<number>个文件
        j=1
        hzm=file.geturlfe(durl[0]['url'])
        com=0
        for k in durl :
            if len(durl)==1 :
                fn='%s.%s' % (filen,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab :
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns :
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn) :
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
            else :
                fn='%s_%s.%s' %(filen,j,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3,j,len(durl),True,durz,com)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns:
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn):
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
                com=com+k['size']
            j=j+1
        if 'sub' in data :
            for s in data['sub']:
                downsub(r2, filen + ".mkv", s, ip, se, data, ns, i)
        imgf = file.spfn(filen + ".mkv")[0] + "." + file.geturlfe(data['pic'])  # 图片文件名
        imgs=avpicdownload(data,r,ip,se,imgf)#封面下载状况
        if (len(durl)>1 or ma) and os.system('ffmpeg -h%s'%(getnul()))==0 and ff :
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt=int(time.time())
            sa=""
            sb=""
            nss=""
            imga=""
            if not ns:
                nss=getnul()
            if 'sub' in data:
                sa,sb=ffinputstr(data['sub'],1)
            if imgs==0 :
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            if len(durl) > 1:
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                ml=f"ffmpeg -f concat -safe 0 -i \"Temp/{file.filtern('%s'%(data['aid']))}_{tt}.txt\"{sa} -metadata aid=\"{data['aid']}\" -metadata bvid=\"{data['bvid']}\" -metadata ctime=\"{tostr2(data['ctime'])}\" -metadata description=\"{bstr.f(data['desc'])}\" -metadata p=\"{i}P/{data['videos']}P\" -metadata title=\"{bstr.f(data['title'])}-{bstr.f(data['page'][i-1]['part'])}\" -metadata pubdate=\"{tostr2(data['pubdate'])}\" -metadata uid=\"{data['uid']}\" -metadata author=\"{bstr.f(data['name'])}\" -metadata cid=\"{data['page'][i-1]['cid']}\" -metadata atitle=\"{bstr.f(data['title'])}\" -metadata part=\"{bstr.f(data['page'][i-1]['part'])}\" -metadata vq=\"{vqs}\"{sb}{imga} -c copy \"{filen}.mkv\"{nss}"
            else :
                ml=f"ffmpeg -i \"{filen}.{hzm}\"{sa} -metadata aid=\"{data['aid']}\" -metadata bvid=\"{data['bvid']}\" -metadata ctime=\"{tostr2(data['ctime'])}\" -metadata description=\"{bstr.f(data['desc'])}\" -metadata p=\"{i}P/{data['videos']}P\" -metadata title=\"{bstr.f(data['title'])}-{bstr.f(data['page'][i-1]['part'])}\" -metadata pubdate=\"{tostr2(data['pubdate'])}\" -metadata uid=\"{data['uid']}\" -metadata author=\"{bstr.f(data['name'])}\" -metadata cid=\"{data['page'][i-1]['cid']}\" -metadata atitle=\"{bstr.f(data['title'])}\" -metadata part=\"{bstr.f(data['page'][i-1]['part'])}\" -metadata vq=\"{vqs}\"{sb}{imga} -c copy \"{filen}.mkv\"{nss}"
            re=os.system(ml)
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                bs=True
                if not ns:
                    bs=False
                if JSONParser.getset(se,'ad')==True :
                    de=True
                    bs=False
                elif JSONParser.getset(se,'ad')==False:
                    bs=False
                if 'ad' in ip :
                    if ip['ad'] :
                        de=True
                        bs=False
                    else :
                        de=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                if len(durl)>1 :
                    j=1
                    for k in durl:
                        os.remove("%s_%s.%s"%(filen,j,hzm))
                        j=j+1
                else :
                    os.remove('%s.%s'%(filen,hzm))
                if 'sub' in data and nbd:
                    for j in data['sub'] :
                        os.remove(j['fn'])
                if imgs==0 and not bp :
                    os.remove(imgf)
            if len(durl)>1:
                os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt))
    elif "data" in re and "dash" in re['data'] :
        vq=re["data"]["quality"]
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq2=re['data']["accept_quality"]
        avq3={}
        avq=[]
        aaq=[]
        dash={'video':{},'audio':{}}
        vqs=[]
        for j in re['data']['dash']['video'] :
            dash['video'][str(j['id'])+j['codecs']]=j
            avq.append(str(j['id'])+j['codecs'])
            if j['id'] not in avq3 :
                avq3[j['id']]=0
        bs=True
        while bs:
            bs=False
            for j in avq2 :
                if j not in avq3 :
                    if ud['vip']<1 and j<=80 and j!=74:
                        bs=True #防止非大会员进入无限死循环
                    elif ud['vip']>0 :
                        bs=True #大会员一旦强制获取所有
                    r2.cookies.set('CURRENT_QUALITY',str(j),domain='.bilibili.com',path='/')
                    re=r2.get(url)
                    re.encoding='utf8'
                    rs=search('__playinfo__=([^<]+)',re.text)
                    if rs!=None :
                        re=json.loads(rs.groups()[0])
                    else :
                        return -2
                    if "data" in re and "dash" in re['data'] :
                        for j in re['data']['dash']['video'] :
                            if (str(j['id'])+j['codecs']) not in dash['video'] :
                                dash['video'][str(j['id'])+j['codecs']]=j
                                avq.append(str(j['id'])+j['codecs'])
                                avq3[j['id']]=0
                                bs=True
                        break
                    else :
                        return -2
        r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
        nau=False #不存在音频
        if not 'audio' in re['data']['dash'] or re['data']['dash']['audio']==None :
            nau=True
        if not nau:
            for j in re['data']['dash']['audio']:
                dash['audio'][j['id']]=j
                aaq.append(j['id'])
            aaq.sort(reverse=True)
        if c and not F:
            p=0 #0 第一个 1 avc 2 hev
            read=JSONParser.getset(se,'mpc')
            if read==True :
                p=1
            elif read==False :
                p=2
            if 'mc' in ip:
                if ip['mc']:
                    p=1
                else :
                    p=2
            p=[0,'avc','hev'][p]
            i2=0
            if p!=0:
                if len(avq)>1 :
                    if sea(avq[0],avq2)==sea(avq[1],avq2):
                        for t in range(2) :
                            if sev(avq[t])[0:3]==p :
                                i2=t
                                break
                    else :
                        i2=0
                else :
                    i2=0
            dash['video']=dash['video'][avq[i2]]
            if not nau:
                dash['audio']=dash['audio'][aaq[0]]
            if ns:
                print(lan['OUTPUT15'])#视频轨：
                print(f"{lan['OUTPUT9']}{vqd[0]}({dash['video']['width']}x{dash['video']['height']},{getfps(dash['video']['frame_rate'])})")#图质：
            dash['video']['size']=streamgetlength(r2,dash['video']['base_url'])
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['video']['size'])}({dash['video']['size']}B,{file.cml(dash['video']['size'],re['data']['timelength'])})")#大小：
                if not nau:
                    print(lan['OUTPUT16'])#音频轨：
                    print('ID：%s'%(dash['audio']['id']))
            if not nau:
                dash['audio']['size']=streamgetlength(r2,dash['audio']['base_url'])
                if ns:
                    print(f"{lan['OUTPUT10']}{file.info.size(dash['audio']['size'])}({dash['audio']['size']}B,{file.cml(dash['audio']['size'],re['data']['timelength'])})")#大小：
                vqs=[vqd[0]+","+dash['video']['codecs'],aaq[0]]
            else :
                vqs=[vqd[0]+","+dash['video']['codecs']]
        else :
            if ns or(not ns and F):
                print(lan['OUTPUT15'])#视频轨：
            k=0
            for j in avq:
                if ns or(not ns and F):
                    print(f"{k+1}.{lan['OUTPUT9']}{vqd[sea(j,avq2)]}({dash['video'][j]['width']}x{dash['video'][j]['height']},{sev(j)},{getfps(dash['video'][j]['frame_rate'])})")#图质：
                dash['video'][j]['size']=streamgetlength(r2,dash['video'][j]['base_url'])
                if ns or(not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(dash['video'][j]['size'])}({dash['video'][j]['size']}B,{file.cml(dash['video'][j]['size'],re['data']['timelength'])})")#大小：
                k=k+1
            if len(avq)>1 and not F :
                bs=True
                fi=True
                while bs:
                    if fi and 'v' in ip:
                        fi=False
                        inp=ip['v']
                    elif ns:
                        inp=input(lan['INPUT2'])#请选择画质：
                    else :
                        print(lan['ERROR3'])#请使用-v <id>选择画质
                        return -6
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(avq)+1 :
                            bs=False
                            dash['video']=dash['video'][avq[int(inp)-1]]
                            if ns:
                                print(lan['OUTPUT11'].replace('<videoquality>',f"{vqd[sea(avq[int(inp)-1],avq2)]}({sev(avq[int(inp)-1])})"))#已选择%s(%s)画质
                            vqs.append(vqd[sea(avq[int(inp)-1],avq2)]+","+sev(avq[int(inp)-1]))
            elif not F :
                dash['video']=dash['video'][avq[0]]
                vqs.append(vqd[0]+","+sev(avq[0]))
            if not nau:
                if ns or(not ns and F):
                    print(lan['OUTPUT16'])#音频轨：
                k=0
                for j in aaq:
                    if ns or(not ns and F):
                        print("%s.ID：%s"%(k+1,j))
                    dash['audio'][j]['size']=streamgetlength(r2,dash['audio'][j]['base_url'])
                    if ns or(not ns and F):
                        print(f"{lan['OUTPUT10']}{file.info.size(dash['audio'][j]['size'])}({dash['audio'][j]['size']}B,{file.cml(dash['audio'][j]['size'],re['data']['timelength'])})")#大小：
                    k=k+1
                if F:
                    return 0
                if len(aaq)>1:
                    bs=True
                    fi=True
                    while bs:
                        if fi and 'a' in ip:
                            fi=False
                            inp=ip['a']
                        elif ns :
                            inp=input(lan['INPUT5'])#请选择音质：
                        else :
                            print(lan['ERROR6'])#请使用-a <id>选择音质
                            return -6
                        if len(inp)>0 and inp.isnumeric() :
                            if int(inp)>0 and int(inp)<len(aaq)+1 :
                                bs=False
                                dash['audio']=dash['audio'][aaq[int(inp)-1]]
                                if ns:
                                    print(lan['OUTPUT17'].replace('<audioquality>',str(aaq[int(inp)-1])))#已选择%s音质
                                vqs.append(aaq[int(inp)-1])
                else :
                    dash['audio']=dash['audio'][aaq[0]]
                    vqs.append(aaq[0])
            else :
                if F:
                    return 0
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if data['videos']==1 :
            if not fin:
                filen=f"{o}{file.filtern(data['title'])}.mkv"
            elif sv:
                if not nau:
                    filen='%s%s'%(o,file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]},{vqs[1]}).mkv"))
                else :
                    filen='%s%s'%(o,file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]}).mkv"))
            else :
                filen='%s%s'%(o,file.filtern('%s(AV%s,%s,P%s,%s).mkv'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'])))
        else :
            if not fin and not dmp:
                filen=f"{o}{file.filtern(data['title'])}-{i}.{file.filtern(data['page'][i-1]['part'])}.mkv"
            elif not fin and dmp:
                filen = f"{o}{i}.{file.filtern(data['page'][i - 1]['part'])}.mkv"
            elif sv and not dmp:
                if not nau:
                    filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]},{vqs[1]}).mkv"))
                else :
                    filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]}).mkv"))
            elif not dmp:
                filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']}).mkv"))
            elif sv:
                if not nau:
                    filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs[0]},{vqs[1]}).mkv"))
                else:
                    filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs[0]}).mkv"))
            else:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']}).mkv"))
        hzm=[file.geturlfe(dash['video']['base_url'])]
        if not nau :
            hzm.append(file.geturlfe(dash['audio']['base_url']))
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        if ff and os.path.exists(filen) and os.system('ffmpeg -h%s'%(getnul()))==0:
            fg=False
            bs=True
            if not ns:
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
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)")#"%s"文件已存在，是否覆盖？
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg :
                try :
                    os.remove('%s'%(filen))
                except :
                    print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        durz=dash['video']['size']
        if not nau :
            durz=durz+dash['audio']['size']
        bs2=True
        while bs2:
            bs2=False
            ar=True
            if JSONParser.getset(se,'a')==False :
                ar=False
            if 'ar' in ip :
                if ip['ar']:
                    ar=True
                else :
                    ar=False
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if ab:
                    read = dwaria2(r2, getfn(0, i, data, vqs, hzm, o, fin, dmp), geturll(dash['video']), dash['video']['size'], c3, ip, se, 1, 2, True)
                else :
                    read = dwaria2(r2, getfn(0, i, data, vqs, hzm, o, fin, dmp), dash['video']['base_url'], dash['video']['size'], c3, ip, se, 1, 2, True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                re=r2.get(dash['video']['base_url'],stream=True)
                read = downloadstream(nte, ip, dash['video']['base_url'], r2, re, getfn(0, i, data, vqs, hzm, o, fin, dmp), dash['video']['size'], c3, 1, 2, True, durz, 0)
            if read==-1 :
                return -1
            elif read==-2 :
                bs=True
                rc=False
                if not ns:
                    bs=False
                read=JSONParser.getset(se,'rd')
                if read==True :
                    bs=False
                    rc=True
                elif read==False :
                    bs=False
                if 'r' in ip:
                    if ip['r']:
                        rc=True
                        bs=False
                    else:
                        rc=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            rc=True
                        elif inp[0].lower()=='n' :
                            bs=False
                if rc :
                    if os.path.exists(getfn(0, i, data, vqs, hzm, o, fin,dmp)):
                        os.remove(getfn(0, i, data, vqs, hzm, o, fin,dmp))
                    bs2=True
                else :
                    return -3
        bs2=True
        if nau :
            bs2=False
        while bs2:
            bs2=False
            ar=True
            if JSONParser.getset(se,'a')==False :
                ar=False
            if 'ar' in ip :
                if ip['ar']:
                    ar=True
                else :
                    ar=False
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if ab:
                    read = dwaria2(r2, getfn(1, i, data, vqs, hzm, o, fin, dmp), geturll(dash['audio']), dash['audio']['size'], c3, ip, se, 2, 2, True)
                else :
                    read = dwaria2(r2, getfn(1, i, data, vqs, hzm, o, fin, dmp), dash['audio']['base_url'], dash['audio']['size'], c3, ip, se, 2, 2, True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                re=r2.get(dash['audio']['base_url'],stream=True)
                read = downloadstream(nte, ip, dash['audio']['base_url'], r2, re, getfn(1, i, data, vqs, hzm, o, fin, dmp), dash['audio']['size'], c3, 2, 2, True, durz, dash['video']['size'])
            if read==-1:
                return -1
            elif read==-2 :
                bs=True
                rc=False
                if not ns:
                    bs=False
                read=JSONParser.getset(se,'rd')
                if read==True :
                    bs=False
                    rc=True
                elif read==False :
                    bs=False
                if 'r' in ip:
                    if ip['r']:
                        rc=True
                        bs=False
                    else:
                        rc=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            rc=True
                        elif inp[0].lower()=='n' :
                            bs=False
                if rc :
                    if os.path.exists(getfn(1, i, data, vqs, hzm, o, fin, dmp)):
                        os.remove(getfn(1, i, data, vqs, hzm, o, fin, dmp))
                    bs2=True
                else :
                    return -3
        if 'sub' in data :
            for s in data['sub']:
                downsub(r2, filen, s, ip, se, data, ns, i, dash['video']['width'], dash['video']['height'])
        imgf=file.spfn(filen)[0]+"."+file.geturlfe(data['pic'])#图片文件名
        imgs=avpicdownload(data,r,ip,se,imgf)#封面下载状况
        if os.system('ffmpeg -h%s'%(getnul()))==0 and ff:
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            sa=""
            sb=""
            nss=""
            imga=""
            if not ns:
                nss=getnul()
            if 'sub' in data:
                if not nau:
                    sa,sb=ffinputstr(data['sub'],2)
                else :
                    sa,sb=ffinputstr(data['sub'],1)
            if imgs==0:
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            if not nau :
                re=os.system(f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\" -i \"{getfn(1,i,data,vqs,hzm,o,fin,dmp)}\"{sa} -metadata title=\"{bstr.f(data['title'])}-{bstr.f(data['page'][i-1]['part'])}\" -metadata description=\"{bstr.f(data['desc'])}\" -metadata aid=\"{data['aid']}\" -metadata bvid=\"{data['bvid']}\" -metadata cid=\"{data['page'][i-1]['cid']}\" -metadata atitle=\"{bstr.f(data['title'])}\" -metadata pubdate=\"{tostr2(data['pubdate'])}\" -metadata ctime=\"{tostr2(data['ctime'])}\" -metadata uid=\"{data['uid']}\" -metadata author=\"{bstr.f(data['name'])}\" -metadata p=\"{i}P/{data['videos']}P\" -metadata part=\"{bstr.f(data['page'][i-1]['part'])}\" -metadata vq=\"{vqs[0]}\" -metadata aq=\"{vqs[1]}\"{sb}{imga} -c:s copy -c copy \"{filen}\"{nss}")
            else :
                re=os.system(f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\"{sa} -metadata title=\"{bstr.f(data['title'])}-{bstr.f(data['page'][i-1]['part'])}\" -metadata description=\"{bstr.f(data['desc'])}\" -metadata aid=\"{data['aid']}\" -metadata bvid=\"{data['bvid']}\" -metadata cid=\"{data['page'][i-1]['cid']}\" -metadata atitle=\"{bstr.f(data['title'])}\" -metadata pubdate=\"{tostr2(data['pubdate'])}\" -metadata ctime=\"{tostr2(data['ctime'])}\" -metadata uid=\"{data['uid']}\" -metadata author=\"{bstr.f(data['name'])}\" -metadata p=\"{i}P/{data['videos']}P\" -metadata part=\"{bstr.f(data['page'][i-1]['part'])}\" -metadata vq=\"{vqs[0]}\"{sb}{imga} -c:s copy -c copy \"{filen}\"{nss}")
            de=False
            if re==0 :
                print(lan['OUTPUT14'])#合并完成！
            if re==0:
                bs=True
                if not ns:
                    bs=False
                if JSONParser.getset(se,'ad')==True :
                    de=True
                    bs=False
                elif JSONParser.getset(se,'ad')==False:
                    bs=False
                if 'ad' in ip :
                    if ip['ad'] :
                        de=True
                        bs=False
                    else :
                        de=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                if not nau:
                    for j in[0,1]:
                        os.remove(getfn(j, i, data, vqs, hzm, o, fin, dmp))
                else :
                    os.remove(getfn(0, i, data, vqs, hzm, o, fin, dmp))
                if 'sub' in data and nbd:
                    for j in data['sub'] :
                        os.remove(j['fn'])
                if imgs==0 and not bp :
                    os.remove(imgf)
def avsubdownload(i,url,data,r,se,ip,ud) :
    '''下载普通类视频字幕
    -1 文件夹创建失败'''
    ns=True
    if 's' in ip:
        ns=False
    nte=False
    if JSONParser.getset(se,'te')==False :
        nte=True
    if 'te' in ip:
        nte=not ip['te']
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    if JSONParser.getset(se, 'dmp') == True:
        dmp = True
    if 'dmp' in ip:
        dmp = ip['dmp']
    if data['videos'] == 1:
        dmp = False
    if dmp:
        if not fin:
            o = f"{o}{file.filtern(data['title'])}/"
        else:
            o = "%s%s/" % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']})"))
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -1
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    if i>1:
        url="%s?p=%s"%(url,i)
    r2.headers.update({'referer':url})
    r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    rr=r2.get("https://api.bilibili.com/x/player.so?id=cid:%s&aid=%s&bvid=%s&buvid=%s"%(data['page'][i-1]['cid'],data['aid'],data['bvid'],r.cookies.get('buvid3')))
    rr.encoding='utf8'
    rs2=search(r'<subtitle>(.+)</subtitle>',rr.text)
    if rs2!=None :
        rs2=json.loads(rs2.groups()[0])
        JSONParser2.getsub(rs2,data)
        if data['videos']==1 :
            if fin:
                filen='%s%s'%(o,file.filtern('%s(AV%s,%s,P%s,%s)'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'])))
            else :
                filen=f"{o}{file.filtern(data['title'])}"
        else :
            if fin and not dmp:
                filen='%s%s'%(o,file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']})"))
            elif not dmp:
                filen=f"{o}{file.filtern(data['title'])}-{i}.{file.filtern(data['page'][i-1]['part'])}"
            elif fin:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i-1]['part']}(P{i},{data['page'][i-1]['cid']})"))
            else:
                filen=f"{o}{i}.{file.filtern(data['page'][i-1]['part'])}"
        if 'sub' in data and len(data['sub'])>0:
            for s in data['sub'] :
                downsub(r2, filen + ".mkv", s, ip, se, data, True, i)
        else :
            if ns:
                print(lan['OUTPUT18'].replace('<number>',str(i)))#第%sP没有可以下载的字幕。
    else :
        if ns:
            print(lan['OUTPUT18'].replace('<number>',str(i)))#第%sP没有可以下载的字幕。
    return 0
def avpicdownload(data,r:requests.Session,ip,se,fn:str=None) ->int :
    """下载封面图片
    fn 指定文件名
    -1 文件夹创建失败
    -2 封面文件下载失败
    -3 覆盖文件失败"""
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    dmp = False
    if JSONParser.getset(se, 'dmp') == True:
        dmp = True
    if 'dmp' in ip:
        dmp = ip['dmp']
    if fn is not None or data['videos'] == 1:
        dmp = False
    if dmp:
        if not fin:
            o = f"{o}{file.filtern(data['title'])}/"
        else:
            o = "%s%s/" % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']})"))
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -1
    if fn==None :
        if fin and not dmp:
            te=file.filtern(f'{data["title"]}(AV{data["aid"]},{data["bvid"]}).{file.geturlfe(data["pic"])}')
        elif not dmp:
            te=file.filtern(f"{data['title']}.{file.geturlfe(data['pic'])}")
        else:
            te = file.filtern(f"cover.{file.geturlfe(data['pic'])}")
        fn=f"{o}{te}"
    if os.path.exists(fn) :
        fg=False
        bs=True
        if not ns:
            fg=True
            bs=False
        if 'y' in ip:
            if ip['y'] :
                fg=True
                bs=False
            else :
                fg=False
                bs=False
        while bs:
            inp=input(f"{lan['INPUT1'].replace('<filename>',fn)}(y/n)")#"%s"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg :
            try :
                os.remove(fn)
            except :
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return -3
    re=r.get(data['pic'])
    if re.status_code==200 :
        f=open(fn,'wb')
        f.write(re.content)
        f.close()
        if ns:
            print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        return 0
    else :
        print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
        return -2
def epvideodownload(i,url,data,r,c,c3,se,ip,ud):
    """下载番剧等视频"""
    che=False
    if 'che' in data :
        che=True
    ns=True
    if 's' in ip:
        ns=False
    bp=False #删除无用文件时是否保留封面图片
    if JSONParser.getset(se,'bp')==True :
        bp=True
    if 'bp' in ip:
        bp=ip['bp']
    nte=False
    if JSONParser.getset(se,'te')==False :
        nte=True
    if 'te' in ip:
        nte=not ip['te']
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建%s文件夹失败
        return -5
    F=False
    if 'F' in ip:
        F=True
    if F:
        print("%s:%s"%(i['titleFormat'],i['longTitle']))
    fdir='%s%s'%(o,file.filtern('%s(SS%s)'%(data['mediaInfo']['title'],data['mediaInfo']['ssId'])))
    if che :
        url2=f"https://www.bilibili.com/cheese/play/ep{i['id']}"
    else :
        url2='https://www.bilibili.com/bangumi/play/ep'+str(i['id'])
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    r2.headers.update({'referer':url2})
    r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    if not che :
        re=r2.get(url2)
        re.encoding='utf8'
        rs=search('__playinfo__=([^<]+)',re.text)
        rs2=search('__PGC_USERSTATE__=([^<]+)',re.text)
        if rs!=None :
            re=json.loads(rs.groups()[0])
        elif rs2!=None :
            rs2=json.loads(rs2.groups()[0])
            if 'dialog' in rs2:
                print(rs2['dialog']['title'])
            if rs2['area_limit']:
                print(lan['ERROR7'])#有区域限制，请尝试使用代理。
            return -2
        else :
            return -2
    else :
        re=r2.get(f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn=120&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=16&session=")
        re.encoding='utf8'
        re=re.json()
    if 'data' in re and 'dash' in re['data']:
        dash={'video':{},'audio':{}}
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq=[]
        avq2=re["data"]["accept_quality"]
        avq3={}
        aaq=[]
        vqs=[]
        for j in re['data']['dash']['video']:
            t=str(j['id'])+j['codecs']
            dash['video'][t]=j
            avq.append(t)
            if j['id'] not in avq3 :
                avq3[j['id']]=0
        bs=True
        while bs:
            bs=False
            for j in avq2 :
                if j not in avq3 :
                    if ud['vip']<1 and j<=80 and j!=74:
                        bs=True #防止非大会员进入无限死循环
                    elif ud['vip']>0 :
                        bs=True #大会员一旦强制获取所有
                    if not che:
                        r2.cookies.set('CURRENT_QUALITY',str(j),domain='.bilibili.com',path='/')
                        re=r2.get(url2)
                        re.encoding='utf8'
                        rs=search('__playinfo__=([^<]+)',re.text)
                        if rs!=None :
                            re=json.loads(rs.groups()[0])
                        else :
                            return -2
                    else :
                        re=r2.get(f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=16&session=")
                        re.encoding='utf8'
                        re=re.json()
                    if "data" in re and "dash" in re['data'] :
                        for j in re['data']['dash']['video'] :
                            if (str(j['id'])+j['codecs']) not in dash['video'] :
                                t=str(j['id'])+j['codecs']
                                dash['video'][t]=j
                                avq.append(t)
                                avq3[j['id']]=0
                                bs=True
                        break
                    else :
                        return -2
        if not che:
            r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
        for j in re['data']['dash']['audio']:
            dash['audio'][j['id']]=j
            aaq.append(j['id'])
        aaq.sort(reverse=True)
        if c and not F:
            p=0 #0 第一个 1 avc 2 hev
            read=JSONParser.getset(se,'mpc')
            if read==True :
                p=1
            elif read==False :
                p=2
            if 'mc' in ip:
                if ip['mc']:
                    p=1
                else :
                    p=2
            p=[0,'avc','hev'][p]
            i2=0
            if p!=0:
                if len(avq)>1 :
                    if sea(avq[0],avq2)==sea(avq[1],avq2):
                        for t in range(2) :
                            if sev(avq[t])[0:3]==p :
                                i2=t
                                break
                    else :
                        i2=0
                else :
                    i2=0
            dash['video']=dash['video'][avq[i2]]
            dash['audio']=dash['audio'][aaq[0]]
            if ns:
                print(lan['OUTPUT15'])#视频轨：
                print(f"{lan['OUTPUT9']}{vqd[0]}({dash['video']['width']}x{dash['video']['height']},{getfps(dash['video']['frame_rate'])})")#图质：
            dash['video']['size']=streamgetlength(r2,dash['video']['base_url'])
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['video']['size'])}({dash['video']['size']}B,{file.cml(dash['video']['size'],re['data']['timelength'])})")#大小
                print(lan['OUTPUT16'])#音频轨：
                print('ID：%s'%(dash['audio']['id']))
            dash['audio']['size']=streamgetlength(r2,dash['audio']['base_url'])
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['audio']['size'])}({dash['audio']['size']}B,{file.cml(dash['audio']['size'],re['data']['timelength'])})")#大小：
            vqs=[vqd[0]+","+dash['video']['codecs'],aaq[0]]
        else :
            if ns or(not ns and F):
                print(lan['OUTPUT15'])#视频轨：
            k=0
            for j in avq:
                if ns or(not ns and F):
                    print(f"{k+1}.{lan['OUTPUT9']}{vqd[sea(j,avq2)]}({dash['video'][j]['width']}x{dash['video'][j]['height']},{sev(j)},{getfps(dash['video'][j]['frame_rate'])})")#画质：
                dash['video'][j]['size']=streamgetlength(r2,dash['video'][j]['base_url'])
                if ns or(not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(dash['video'][j]['size'])}({dash['video'][j]['size']}B,{file.cml(dash['video'][j]['size'],re['data']['timelength'])})")#大小：
                k=k+1
            if len(avq)>1 and not F:
                bs=True
                fi=True
                while bs:
                    if fi and 'v' in ip:
                        fi=False
                        inp=ip['v']
                    elif ns:
                        inp=input(lan['INPUT2'])#请选择画质：
                    else :
                        print(lan['ERROR3'])#请使用-v <id>选择画质
                        return -6
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(avq)+1 :
                            bs=False
                            dash['video']=dash['video'][avq[int(inp)-1]]
                            if ns:
                                print(lan['OUTPUT11'].replace('<videoquality>',f"{vqd[sea(avq[int(inp)-1],avq2)]}({sev(avq[int(inp)-1])})"))#已选择%s(%s)画质
                            vqs.append(vqd[sea(avq[int(inp)-1],avq2)]+","+sev(avq[int(inp)-1]))
            elif not F :
                dash['video']=dash['video'][avq[0]]
                vqs.append(vqd[0]+","+sev(avq[0]))
            if ns or(not ns and F):
                print(lan['OUTPUT16'])#音频轨：
            k=0
            for j in aaq:
                if ns or(not ns and F):
                    print("%s.ID：%s"%(k+1,j))
                dash['audio'][j]['size']=streamgetlength(r2,dash['audio'][j]['base_url'])
                if ns or(not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(dash['audio'][j]['size'])}({dash['audio'][j]['size']}B,{file.cml(dash['audio'][j]['size'],re['data']['timelength'])})")#大小：
                k=k+1
            if F:
                return 0
            if len(aaq)>1:
                bs=True
                fi=True
                while bs:
                    if fi and 'a' in ip:
                        fi=False
                        inp=ip['a']
                    elif ns:
                        inp=input(lan['INPUT5'])#请选择音质：
                    else :
                        print(lan['ERROR6'])#请使用-a <id>选择音质
                        return -6
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(aaq)+1 :
                            bs=False
                            dash['audio']=dash['audio'][aaq[int(inp)-1]]
                            if ns:
                                print(lan['OUTPUT17'].replace('<audioquality>',str(aaq[int(inp)-1])))#已选择%s音质
                            vqs.append(aaq[int(inp)-1])
            else :
                dash['audio']=dash['audio'][aaq[0]]
                vqs.append(aaq[0])
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if i['s']=='e' :
            if not fin:
                filen='%s/%s'%(fdir,file.filtern(f"{i['i']+1}.{i['longTitle']}.mkv"))
            elif sv:
                filen='%s/%s'%(fdir,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s,%s,%s).mkv'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[0],vqs[1])))
            else :
                filen='%s/%s'%(fdir,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).mkv'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'])))
        else :
            if not fin:
                filen='%s/%s'%(fdir,file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}.mkv"))
            elif sv:
                filen='%s/%s'%(fdir,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s,%s,%s).mkv'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[0],vqs[1])))
            else :
                filen='%s/%s'%(fdir,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s).mkv'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'])))
        hzm=[file.geturlfe(dash['video']['base_url']),file.geturlfe(dash['audio']['base_url'])]
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        if ff and os.path.exists(filen) and os.system('ffmpeg -h%s'%(getnul()))==0 :
            fg=False
            bs=True
            if not ns:
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
                inp=input(f"{lan['INPUT1'].replace('<filename>',filen)}(y/n)")#"%s"文件已存在，是否覆盖？
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg :
                try :
                    os.remove('%s'%(filen))
                except :
                    print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        durz=dash['video']['size']+dash['audio']['size']
        bs2=True
        while bs2:
            bs2=False
            ar=True
            if JSONParser.getset(se,'a')==False :
                ar=False
            if 'ar' in ip :
                if ip['ar']:
                    ar=True
                else :
                    ar=False
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if ab:
                    read=dwaria2(r2,getfn2(i,0,fdir,vqs,hzm,fin),geturll(dash['video']),dash['video']['size'],c3,ip,se,1,2,True)
                else :
                    read=dwaria2(r2,getfn2(i,0,fdir,vqs,hzm,fin),dash['video']['base_url'],dash['video']['size'],c3,ip,se,1,2,True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                re=r2.get(dash['video']['base_url'],stream=True)
                read=downloadstream(nte,ip,dash['video']['base_url'],r2,re,getfn2(i,0,fdir,vqs,hzm,fin),dash['video']['size'],c3,1,2,True,durz,0)
            if read==-1 :
                return -1
            elif read==-2 :
                bs=True
                rc=False
                if not ns:
                    bs=False
                read=JSONParser.getset(se,'rd')
                if read==True :
                    bs=False
                    rc=True
                elif read==False :
                    bs=False
                if 'r' in ip:
                    if ip['r']:
                        rc=True
                        bs=False
                    else:
                        rc=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            rc=True
                        elif inp[0].lower()=='n' :
                            bs=False
                if rc :
                    if os.path.exists(getfn2(i,0,fdir,vqs,hzm,fin)):
                        os.remove(getfn2(i,0,fdir,vqs,hzm,fin))
                    bs2=True
                else :
                    return -3
        bs2=True
        while bs2:
            bs2=False
            ar=True
            if JSONParser.getset(se,'a')==False :
                ar=False
            if 'ar' in ip :
                if ip['ar']:
                    ar=True
                else :
                    ar=False
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if ab:
                    read=dwaria2(r2,getfn2(i,1,fdir,vqs,hzm,fin),geturll(dash['audio']),dash['audio']['size'],c3,ip,se,2,2,True)
                else :
                    read=dwaria2(r2,getfn2(i,1,fdir,vqs,hzm,fin),dash['audio']['base_url'],dash['audio']['size'],c3,ip,se,2,2,True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                re=r2.get(dash['audio']['base_url'],stream=True)
                read=downloadstream(nte,ip,dash['audio']['base_url'],r2,re,getfn2(i,1,fdir,vqs,hzm,fin),dash['audio']['size'],c3,2,2,True,durz,dash['video']['size'])
            if read==-1 :
                return -1
            elif read==-2 :
                bs=True
                rc=False
                if not ns:
                    bs=False
                read=JSONParser.getset(se,'rd')
                if read==True :
                    bs=False
                    rc=True
                elif read==False :
                    bs=False
                if 'r' in ip:
                    if ip['r']:
                        rc=True
                        bs=False
                    else:
                        rc=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            rc=True
                        elif inp[0].lower()=='n' :
                            bs=False
                if rc :
                    if os.path.exists(getfn2(i,1,fdir,vqs,hzm,fin)):
                        os.remove(getfn2(i,1,fdir,vqs,hzm,fin))
                    bs2=True
                else :
                    return -3
        if not che:
            imgf=f"{file.spfn(filen)[0]}.{file.geturlfe(i['cover'])}"#图片文件名
            imgs=eppicdownload(i,data,r,ip,se,imgf)#封面下载状况
        if os.system('ffmpeg -h%s'%(getnul()))==0 and ff:
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            nss=""
            imga=""
            if not ns:
                nss=getnul()
            if not che and imgs==0:
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            re=os.system(f"ffmpeg -i \"{getfn2(i,0,fdir,vqs,hzm,fin)}\" -i \"{getfn2(i,1,fdir,vqs,hzm,fin)}\" -metadata id=\"{data['mediaInfo']['id']}\" -metadata ssid=\"{data['mediaInfo']['ssId']}\" -metadata title=\"{bstr.f(data['mediaInfo']['title'])}-{bstr.f(i['titleFormat'])} {bstr.f(i['longTitle'])}\" -metadata series=\"{bstr.f(data['mediaInfo']['series'])}\" -metadata description=\"{bstr.f(data['mediaInfo']['evaluate'])}\" -metadata pubtime=\"{data['mediaInfo']['time']}\" -metadata atitle=\"{bstr.f(data['mediaInfo']['title'])}\" -metadata eptitle=\"{bstr.f(i['longTitle'])}\" -metadata titleformat=\"{bstr.f(i['titleFormat'])}\" -metadata epid=\"{i['id']}\" -metadata aid=\"{i['aid']}\" -metadata bvid=\"{i['bvid']}\" -metadata cid=\"{i['cid']}\" -metadata aq=\"{vqs[1]}\" -metadata vq=\"{vqs[0]}\"{imga} -c copy \"{filen}\"{nss}")
            de=False
            if re==0 :
                print(lan['OUTPUT14'])#合并完成！
            if re==0:
                bs=True
                if not ns:
                    bs=False
                if JSONParser.getset(se,'ad')==True :
                    de=True
                    bs=False
                elif JSONParser.getset(se,'ad')==False:
                    bs=False
                if 'ad' in ip:
                    if ip['ad']:
                        de=True
                        bs=False
                    else :
                        de=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                for j in[0,1]:
                    os.remove(getfn2(i,j,fdir,vqs,hzm,fin))
                if not che and imgs==0 and not bp:
                    os.remove(imgf)
    elif 'data' in re and 'durl' in re['data'] :
        vq=re["data"]["quality"]
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq=re["data"]["accept_quality"]
        durl={vq:re["data"]['durl']}
        durz={}
        vqs=""
        if not c or F:
            j=0
            for l in avq :
                if not l in durl :
                    if not che :
                        r2.cookies.set('CURRENT_QUALITY',str(l),domain='.bilibili.com',path='/')
                        re=r2.get(url2)
                        re.encoding='utf8'
                        rs=search('__playinfo__=([^<]+)',re.text)
                        if rs!=None:
                            re=json.loads(rs.groups()[0])
                        else :
                            return -2
                    else :
                        re=r2.get(f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=16&session=")
                        re.encoding='utf8'
                        re=re.json()
                    durl[re["data"]['quality']]=re['data']['durl']
                if ud['vip']<1 and (l>80 or l==74) :
                    avq,ii=delli(avq,l)
                    if ii>-1 :
                        vqd=dellk(vqd,ii)
                    continue
                if ns or(not ns and F):
                    print(f"{j+1}.{lan['OUTPUT9']}{vqd[j]}")#图质：
                j=j+1
                size=0
                for k in durl[l] :
                    size=size+k['size']
                durz[l]=size
                if ns or(not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(size)}({size}B,{file.cml(size,re['data']['timelength'])})")#大小：
            r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
            if F:
                return 0
            bs=True
            fi=True
            while bs :
                if fi and 'v' in ip :
                    fi=False
                    inp=ip['v']
                elif ns:
                    inp=input(lan['INPUT2'])#请选择画质：
                else :
                    print(lan['ERROR3'])#请使用"-v <id>"选择画质
                    return -6
                if len(inp) > 0 and inp.isnumeric() and int(inp)>0 and int(inp)<len(avq)+1 :
                    durl=durl[avq[int(inp)-1]]
                    durz=durz[avq[int(inp)-1]]
                    vq=avq[int(inp)-1]
                    bs=False
            if ns:
                print(lan['OUTPUT11'].replace('<videoquality>',vqd[int(inp)-1]))#已选择<videoquality>画质
            vqs=vqd[int(inp)-1]
        else :
            j=0
            for l in avq :
                if l==vq :
                    if ns:
                        print(f"{lan['OUTPUT9']}{vqd[j]}")#画质：
                    vqs=vqd[j]
                    break
                j=j+1
            durz=0
            for k in durl[vq] :
                durz=durz+k['size']
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(durz)}({durz}B,{file.cml(durz,re['data']['timelength'])})")#大小：
            durl=durl[vq]
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if i['s']=='e' :
            if not fin:
                filen='%s/%s'%(fdir,file.filtern(f"{i['i']+1}{i['longTitle']}"))
            elif sv:
                filen='%s/%s'%(fdir,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s,%s)'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs)))
            else :
                filen='%s/%s'%(fdir,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s)'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'])))
        else :
            if not fin:
                filen='%s/%s'%(fdir,file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}"))
            elif sv:
                filen='%s/%s'%(fdir,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s,%s)'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs)))
            else :
                filen='%s/%s'%(fdir,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s)'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'])))
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        ma=False
        if JSONParser.getset(se,"ma")==True :
            ma=True
        if 'ma' in ip:
            ma=ip['ma']
        if ff and (len(durl)>1 or ma) and os.path.exists('%s.mkv'%(filen)) and os.system('ffmpeg -h%s'%(getnul()))==0 :
            fg=False
            bs=True
            if not ns:
                fg=True
                bs=False
            if 'y' in ip :
                if ip['y'] :
                    fg=True
                    bs=False
                else :
                    fg=True
                    bs=False
            while bs:
                inp=input(f"{lan['INPUT1'].replace('<filename>','%s.mkv'%(filen))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove('%s.mkv'%(filen))
                except :
                    print(lan['OUTPUT7'])
                    return 0
            else:
                return 0
        if ns:
            print(lan['OUTPUT12'].replace('<number>',str(len(durl))))#共有<number>个文件
        j=1
        hzm=file.geturlfe(durl[0]['url'])
        com=0
        for k in durl :
            if len(durl)==1 :
                fn='%s.%s' % (filen,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab :
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns:
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn):
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
            else :
                fn='%s_%s.%s' %(filen,j,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3,j,len(durl),True,durz,com)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns:
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn):
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
                com=com+k['size']
            j=j+1
        if not che:
            imgf = f"{file.spfn(filen + '.mkv')[0]}.{file.geturlfe(i['cover'])}"#图片文件名
            imgs=eppicdownload(i,data,r,ip,se,imgf)#封面下载状况
        if (len(durl)>1 or ma) and os.system('ffmpeg -h%s'%(getnul()))==0 and ff :
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt=int(time.time())
            nss=""
            imga=""
            if not ns:
                nss=getnul()
            if not che and imgs==0:
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            if len(durl)>1 :
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(i['id'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                ml=f"ffmpeg -f concat -safe 0 -i \"Temp/{file.filtern('%s'%(i['id']))}_{tt}.txt\" -metadata id=\"{data['mediaInfo']['id']}\" -metadata ssid=\"{data['mediaInfo']['ssId']}\" -metadata title=\"{bstr.f(data['mediaInfo']['title'])}-{bstr.f(i['titleFormat'])} {bstr.f(i['longTitle'])}\" -metadata series=\"{bstr.f(data['mediaInfo']['series'])}\" -metadata description=\"{bstr.f(data['mediaInfo']['evaluate'])}\" -metadata pubtime=\"{data['mediaInfo']['time']}\" -metadata atitle=\"{bstr.f(data['mediaInfo']['title'])}\" -metadata eptitle=\"{bstr.f(i['longTitle'])}\" -metadata titleformat=\"{bstr.f(i['titleFormat'])}\" -metadata epid=\"{i['id']}\" -metadata aid=\"{i['aid']}\" -metadata bvid=\"{i['bvid']}\" -metadata cid=\"{i['cid']}\" -metadata vq=\"{vqs}\"{imga} -c copy \"{filen}.mkv\"{nss}"
            else :
                ml=f"ffmpeg -i \"{filen}.{hzm}\" -metadata id=\"{data['mediaInfo']['id']}\" -metadata ssid=\"{data['mediaInfo']['ssId']}\" -metadata title=\"{bstr.f(data['mediaInfo']['title'])}-{bstr.f(i['titleFormat'])} {bstr.f(i['longTitle'])}\" -metadata series=\"{bstr.f(data['mediaInfo']['series'])}\" -metadata description=\"{bstr.f(data['mediaInfo']['evaluate'])}\" -metadata pubtime=\"{data['mediaInfo']['time']}\" -metadata atitle=\"{bstr.f(data['mediaInfo']['title'])}\" -metadata eptitle=\"{bstr.f(i['longTitle'])}\" -metadata titleformat=\"{bstr.f(i['titleFormat'])}\" -metadata epid=\"{i['id']}\" -metadata aid=\"{i['aid']}\" -metadata bvid=\"{i['bvid']}\" -metadata cid=\"{i['cid']}\" -metadata vq=\"{vqs}\"{imga} -c copy \"{filen}.mkv\"{nss}"
            re=os.system(ml)
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                bs=True
                if not ns:
                    bs=False
                if JSONParser.getset(se,'ad')==True :
                    de=True
                    bs=False
                elif JSONParser.getset(se,'ad')==False:
                    bs=False
                if 'ad' in ip :
                    if ip['ad'] :
                        de=True
                        bs=False
                    else :
                        de=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                if len(durl)>1 :
                    j=1
                    for k in durl:
                        os.remove("%s_%s.%s"%(filen,j,hzm))
                        j=j+1
                else :
                    os.remove('%s.%s'%(filen,hzm))
                if not che and imgs==0 and not bp :
                    os.remove(imgf)
            if len(durl)>1:
                os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(i['id'])),tt))
def eppicdownload(i,data,r:requests.Session,ip,se,fn:str=None)->int :
    """下载封面图片
    fn 指定文件名
    -1 文件夹创建失败
    -2 封面文件下载失败
    -3 覆盖文件失败"""
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -1
    fdir=f"{o}{file.filtern('%s(SS%s)'%(data['mediaInfo']['title'],data['mediaInfo']['ssId']))}"#SS文件夹
    try :
        if not os.path.exists(fdir) :
            mkdir(fdir)
    except :
        print(lan['ERROR1'].replace('<dirname>',fdir))#创建文件夹"<dirname>"失败。
        return -1
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    cf2=data['mediaInfo']['cover']
    fn2=f"{fdir}/cover.{file.geturlfe(cf2)}"
    if not os.path.exists(fn2) :
        re=r.get(cf2)
        if re.status_code==200 :
            f=open(fn2,'wb')
            f.write(re.content)
            f.close()
            if ns:
                print(lan['OUTPUT23'].replace('<filename>',fn2))#封面图片下载完成。
        else :
            print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
    if 'che' in  data :
        if 'brief' in data :
            ii=1
            for uri in data['brief'] :
                chepicdownload(uri,r,fdir,ii,ns)
                ii=ii+1
        return 0
    cf=i['cover']
    if fn==None :
        if fin:
            fn=f"{fdir}/{file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).%s'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],file.geturlfe(cf)))}"
        else :
            fn=f"{fdir}/{file.filtern('%s.%s.%s'%(i['i']+1,i['longTitle'],file.geturlfe(cf)))}"
    if os.path.exists(fn) :
        fg=False
        bs=True
        if not ns:
            fg=True
            bs=False
        if 'y' in ip:
            if ip['y'] :
                fg=True
                bs=False
            else :
                fg=False
                bs=False
        while bs:
            inp=input(f"{lan['INPUT1'].replace('<filename>',fn)}(y/n)")#"%s"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg :
            try :
                os.remove(fn)
            except :
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return -3
    re=r.get(cf)
    if re.status_code==200 :
        f=open(fn,'wb')
        f.write(re.content)
        f.close()
        if ns:
            print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        return 0
    else :
        print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
        return -2
def chepicdownload(url:str,r:requests.session,fdir:str,i:int,ns:bool) :
    fn=f"{fdir}/des{i}.{file.geturlfe(url)}"
    if not os.path.exists(fn) :
        re=r.get(url)
        if re.status_code==200 :
            f=open(fn,'wb')
            f.write(re.content)
            f.close()
            if ns:
                print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        else :
            print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
def smdownload(r:requests.Session,i:dict,c:bool,se:dict,ip:dict) :
    """下载小视频
    c 继续下载"""
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    nte=False
    if JSONParser.getset(se,'te')==False :
        nte=True
    if 'te' in ip:
        nte=not ip['te']
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -5
    F=False
    if 'F' in ip:
        F=True
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    r2=requests.session()
    r2.headers=copydict(r.headers)
    r2.proxies=r.proxies
    if nte:
        r2.trust_env=False
    r2.headers.update({'referer':'https://vc.bilibili.com/video/%s'%(i['id'])})
    fz=streamgetlength(r2,i['video_playurl'])
    if ns or(not ns and F):
        print(lan['OUTPUT15'])#画质：
        print('%sx%s,%s(%sB,%s)'%(i['width'],i['height'],file.info.size(fz),fz,file.cml(fz,i['video_time']*1000)))
    if F:
        return 0
    sv=True
    if JSONParser.getset(se,'sv')==False :
        sv=False
    if 'sv' in ip:
        sv=ip['sv']
    slt=False
    if JSONParser.getset(se,'slt')==True :
        slt=True
    if 'slt' in ip :
        slt=ip['slt']
    if slt :
        sn=i['description']
    else :
        if len(i['description']) >20 :
            sn=i['description'][0:20]
        else :
            sn=i['description']
    if not fin:
        filen=f"{o}{file.filtern(i['name'])}-{file.filtern(sn)}(小视频)"
    elif sv:
        filen='%s%s'%(o,file.filtern('%s-%s(小视频,ID%s,UID%s,%sx%s)'%(i['name'],sn,i['id'],i['uid'],i['width'],i['height'])))
    else :
        filen='%s%s'%(o,file.filtern('%s-%s(小视频,ID%s,UID%s)'%(i['name'],sn,i['id'],i['uid'])))
    ff=True
    if JSONParser.getset(se,'nf')==True :
        ff=False
    if 'yf' in ip :
        if ip['yf']:
            ff=True
        else :
            ff=False
    ma=False
    if JSONParser.getset(se,"ma")==True :
        ma=True
    if 'ma' in ip:
        ma=ip['ma']
    if ff and ma and os.path.exists('%s.mkv'%(filen)) and os.system('ffmpeg -h%s'%(getnul()))==0 :
        fg=False
        bs=True
        if not ns:
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
            inp=input(f"{lan['INPUT1'].replace('<filename>','%s.mkv'%(filen))}(y/n)")
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            try :
                os.remove('%s.mkv'%(filen))
            except :
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return 0
        else:
            return 0
    hzm=file.geturlfe(i['video_playurl'])
    fn='%s.%s'%(filen,hzm)
    bs2=True
    while bs2:
        bs2=False
        ar=True
        if JSONParser.getset(se,'a')==False :
            ar=False
        if 'ar' in ip :
            if ip['ar']:
                ar=True
            else :
                ar=False
        if os.system('aria2c -h%s'%(getnul()))==0 and ar :
            ab=True
            if JSONParser.getset(se,'ab')==False :
                ab=False
            if 'ab' in ip:
                if ip['ab']:
                    ab=True
                else :
                    ab=False
            if ab:
                read=dwaria2(r2,fn,geturll(i),fz,c,ip,se)
            else :
                read=dwaria2(r2,fn,i['video_playurl'],fz,c,ip,se)
            if read==-3 :
                print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                return -4
        else :
            re=r2.get(i['video_playurl'],stream=True)
            read=downloadstream(nte,ip,i['video_playurl'],r2,re,fn,fz,c)
        if read==-1 :
            return -1
        elif read==-2 :
            bs=True
            rc=False
            if not ns:
                bs=False
            read=JSONParser.getset(se,'rd')
            if read==True :
                bs=False
                rc=True
            elif read==False :
                bs=False
            if 'r' in ip:
                if ip['r']:
                    rc=True
                    bs=False
                else:
                    rc=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        rc=True
                    elif inp[0].lower()=='n' :
                        bs=False
            if rc :
                if os.path.exists(fn):
                    os.remove(fn)
                bs2=True
            else :
                return -3
    if ma and ff and os.system('ffmpeg -h%s'%(getnul()))==0 :
        print(lan['OUTPUT13'])#将用ffmpeg自动合成
        nss=""
        if not ns:
            nss=getnul()
        ml='ffmpeg -i "%s.%s" -metadata title="%s-%s" -metadata description="%s" -metadata id="%s" -metadata pubtime="%s" -metadata author="%s" -metadata uid="%s" -metadata vq="%sx%s" -metadata tags="%s" -metadata purl="https://vc.bilibili.com/video/%s" -c copy "%s.mkv"%s'%(filen,hzm,bstr.f(i['name']),bstr.f(sn),bstr.f(i['description']),i['id'],i['upload_time'],bstr.f(i['name']),i['uid'],i['width'],i['height'],bstr.f(bstr.gettags(i['tags'])),i['id'],filen,nss)
        re=os.system(ml)
        if re==0:
            print(lan['OUTPUT14'])#合并完成！
        de=False
        if re==0:
            bs=True
            if not ns:
                bs=False
            if JSONParser.getset(se,'ad')==True :
                de=True
                bs=False
            elif JSONParser.getset(se,'ad')==False:
                bs=False
            if 'ad' in ip :
                if ip['ad'] :
                    de=True
                    bs=False
                else :
                    de=False
                    bs=False
            while bs :
                inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        de=True
                    elif inp[0].lower()=='n' :
                        bs=False
        if re==0 and de:
            os.remove('%s.%s'%(filen,hzm))
    return 0
def lrvideodownload(data,r,c,c3,se,ip):
    """下载直播回放视频
    -1 cookies.json读取错误
    -2 API Error
    -3 下载错误
    -4 aria2c参数错误
    -5 文件夹创建失败"""
    ns=True
    if 's' in ip:
        ns=False
    nte=False
    if JSONParser.getset(se,'te')==False :
        nte=True
    if 'te' in ip:
        nte=not ip['te']
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    F=False #仅输出视频信息
    if 'F' in ip:
        F=True
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -5
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    r2.headers.update({'referer':'https://live.bilibili.com/record/%s'%(data['rid'])})
    r2.cookies.set('CURRENT_QUALITY','120',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    re=r2.get('https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?rid=%s&platform=html5'%(data['rid']))
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -2
    if 'data' in re and 'list' in re['data'] :
        #vq=re['data']['current_qn'] #暂时不需要
        avq,vqd=bstr.getv(re['data']['qn_desc'])
        vqd = getqualitytransl(vqd)
        if len(avq) >1 :
            print(f"{lan['ERROR8']}\n{lan['ERROR5']}")#不支持画质选择
            input(lan['INPUT6'])#请按回车键继续下载
        durl=re['data']['list'] #暂时只有原画质
        durz=0
        for k in durl :
            durz=durz+k['size']
        vqs=vqd[0]
        if ns or (not ns and F) :
            print(f"{lan['OUTPUT9']}{vqs}")#画质：
            print(f"{lan['OUTPUT10']}{file.info.size(durz)}({durz}B,{file.cml(durz,re['data']['length'])})")#大小：
        if F :
            return 0
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if not fin:
            filen=f"{o}{file.filtern(data['title'])}"
        elif sv:
            filen='%s%s'%(o,file.filtern('%s(%s,%s,%s)'%(data['title'],data['rid'],data['roomid'],vqs)))
        else :
            filen='%s%s'%(o,file.filtern('%s(%s,%s)'%(data['title'],data['rid'],data['roomid'])))
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        ma=False
        if JSONParser.getset(se,"ma")==True :
            ma=True
        if 'ma' in ip:
            ma=ip['ma']
        if ff and (len(durl)>1 or ma) and os.path.exists('%s.mkv'%(filen)) and os.system('ffmpeg -h%s'%(getnul()))==0 :
            fg=False
            bs=True
            if not ns:
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
                inp=input(f"{lan['INPUT1'].replace('<filename>','%s.mkv'%(filen))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove('%s.mkv'%(filen))
                except :
                    print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        if ns:
            print(lan['OUTPUT12'].replace('<number>',str(len(durl))))#共有<number>个文件
        j=1
        hzm=file.geturlfe(durl[0]['url'])
        com=0
        for k in durl :
            if len(durl)==1 :
                fn='%s.%s' % (filen,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab :
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns :
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn) :
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
            else :
                fn='%s_%s.%s' %(filen,j,hzm)
                bs2=True
                while bs2:
                    bs2=False
                    ar=True
                    if JSONParser.getset(se,'a')==False :
                        ar=False
                    if 'ar' in ip :
                        if ip['ar']:
                            ar=True
                        else :
                            ar=False
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3,j,len(durl),True,durz,com)
                    if read==-1 :
                        return -1
                    elif read==-2 :
                        bs=True
                        rc=False
                        if not ns:
                            bs=False
                        read=JSONParser.getset(se,'rd')
                        if read==True :
                            bs=False
                            rc=True
                        elif read==False :
                            bs=False
                        if 'r' in ip:
                            if ip['r']:
                                rc=True
                                bs=False
                            else:
                                rc=False
                                bs=False
                        while bs :
                            inp=input(f"{lan['INPUT3']}(y/n)")#文件下载失败，是否重新下载？
                            if len(inp)>0 :
                                if inp[0].lower()=='y' :
                                    bs=False
                                    rc=True
                                elif inp[0].lower()=='n' :
                                    bs=False
                        if rc :
                            if os.path.exists(fn):
                                os.remove(fn)
                            bs2=True
                        else :
                            return -3
                com=com+k['size']
            j=j+1
        if (len(durl)>1 or ma) and os.system('ffmpeg -h%s'%(getnul()))==0 and ff :
            lrh=True #是否进行去HTML化
            if JSONParser.getset(se,'lrh')==False :
                lrh=False
            if 'lrh' in ip:
                lrh=ip['lrh']
            if lrh:
                data['des']=bstr.rhtml(data['des'])
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt=int(time.time())
            nss=""
            if not ns:
                nss=getnul()
            if len(durl) > 1:
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['rid'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                ml='ffmpeg -f concat -safe 0 -i "Temp/%s_%s.txt" -metadata rid="%s" -metadata room_id="%s" -metadata uid="%s" -metadata title="%s" -metadata area_id="%s" -metadata parent_area_id="%s" -metadata starttime="%s" -metadata endtime="%s" -metadata description="%s" -metadata area_name="%s" -metadata parent_area_name="%s" -metadata tags="%s" -metadata hot_words="%s" -metadata author="%s" -metadata sex="%s" -metadata sign="%s" -metadata vq="%s" -c copy "%s.mkv"%s' %(file.filtern('%s'%(data['rid'])),tt,data['rid'],data['roomid'],data['uid'],bstr.f(data['title']),data['areaid'],data['pareaid'],tostr2(data['st']),tostr2(data['et']),bstr.f(data['des']),bstr.f(data['arean']),bstr.f(data['parean']),bstr.f(data['tags']),bstr.f(bstr.gettags(data['hotwords'])),bstr.f(data['name']),bstr.f(data['sex']),bstr.f(data['sign']),vqs,filen,nss)
            else :
                ml='ffmpeg -i "%s.%s" -metadata rid="%s" -metadata room_id="%s" -metadata uid="%s" -metadata title="%s" -metadata area_id="%s" -metadata parent_area_id="%s" -metadata starttime="%s" -metadata endtime="%s" -metadata description="%s" -metadata area_name="%s" -metadata parent_area_name="%s" -metadata tags="%s" -metadata hot_words="%s" -metadata author="%s" -metadata sex="%s" -metadata sign="%s" -metadata vq="%s" -c copy "%s.mkv"%s'%(filen,hzm,data['rid'],data['roomid'],data['uid'],bstr.f(data['title']),data['areaid'],data['pareaid'],tostr2(data['st']),tostr2(data['et']),bstr.f(data['des']),bstr.f(data['arean']),bstr.f(data['parean']),bstr.f(data['tags']),bstr.f(bstr.gettags(data['hotwords'])),bstr.f(data['name']),bstr.f(data['sex']),bstr.f(data['sign']),vqs,filen,nss)
            re=os.system(ml)
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                bs=True
                if not ns:
                    bs=False
                if JSONParser.getset(se,'ad')==True :
                    de=True
                    bs=False
                elif JSONParser.getset(se,'ad')==False:
                    bs=False
                if 'ad' in ip :
                    if ip['ad'] :
                        de=True
                        bs=False
                    else :
                        de=False
                        bs=False
                while bs :
                    inp=input(f"{lan['INPUT4']}(y/n)")#是否删除中间文件？
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                if len(durl)>1 :
                    j=1
                    for k in durl:
                        os.remove("%s_%s.%s"%(filen,j,hzm))
                        j=j+1
                else :
                    os.remove('%s.%s'%(filen,hzm))
            if len(durl)>1:
                os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(data['rid'])),tt))


def livevideodownload(data: dict, data2: dict, r: requests.session, c: bool, se: dict, ip: dict):
    """下载直播视频
    -2 API Error
    -4 aria2c 参数错误
    -5 文件夹创建失败
    -6 缺少必要参数
    -7 参数错误"""
    ns = True
    if 's' in ip:
        ns = False
    o = 'Download/'
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    F = False  # 仅输出视频信息
    if 'F' in ip:
        F = True
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建文件夹"<dirname>"失败。
        return -5
    nte = False  # requests是否信任环境变量
    if JSONParser.getset(se, 'te') == False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    fin = True  # 是否把AV号等信息放入文件名
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    sv = True  # 是否将画质信息写入文件
    if JSONParser.getset(se, 'sv') == False:
        sv = False
    if 'sv' in ip:
        sv = ip['sv']
    if 'play_url' in data2 and data2['play_url'] is not None:
        play_url = data2['play_url']
    else:
        uri = f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={data['roomid']}&qn=10000&platform=web&https_url_req=1&ptype=16"
        re = r.get(uri)
        re.encoding = 'utf8'
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            return -2
        play_url = re['data']
    quality_description = play_url['quality_description']
    accept_quality_list = []
    quality_des_dict = {}
    for i in quality_description:
        accept_quality_list.append(i['qn'])
        quality_des_dict[i['qn']] = getqualitytrans(i['desc'])
    current_qn = play_url['current_qn']
    if 'durl' in play_url:
        durl = {}
        durl[current_qn] = play_url['durl']
        if not c or F:
            for quality in accept_quality_list:
                if quality not in durl:
                    uri = f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={data['roomid']}&qn={quality}&platform=web&https_url_req=1&ptype=16"
                    re = r.get(uri)
                    re.encoding = 'utf8'
                    re = re.json()
                    if re['code'] != 0:
                        print(f"{re['code']} {re['message']}")
                        return -2
                    play_url = re['data']
                    current_qn = play_url['current_qn']
                    if quality == current_qn:
                        if 'durl' in play_url:
                            durl[quality] = play_url['durl']
                    else:
                        accept_quality_list.remove(quality)
                        print(lan['NOT_GET_QUA'].replace('<quality>', str(quality)))  # 无法获取画质为<quality>的播放地址。
            if ns or (not ns and F):
                ii = 1
                for quality in accept_quality_list:
                    print(f"{ii}.{lan['OUTPUT9']}{quality},{quality_des_dict[quality]}{lan['ALL_URL_COUNT'].replace('<number>', str(len(durl[quality])))}")
                    ii = ii + 1
            if F:
                return 0
            bs = True
            first = True
            while bs:
                if len(accept_quality_list) == 1:
                    inp = '1'
                elif first and 'v' in ip:
                    first = False
                    inp = ip['v']
                elif ns:
                    inp = input(lan['INPUT2'])  # 请选择画质：
                else:
                    print(lan['ERROR3'])  # 请使用"-v <id>"选择画质
                    return -6
                if len(inp) > 0 and inp.isnumeric() and int(inp) > 0 and int(inp) < len(accept_quality_list) + 1:
                    video_quality = accept_quality_list[int(inp) - 1]
                    durl = durl[video_quality]
                    bs = False
            if ns:
                print(lan['OUTPUT11'].replace('<videoquality>', f"{video_quality},{quality_des_dict[video_quality]}"))#已选择<videoquality>画质
        else:
            quality = accept_quality_list[0]
            if quality != current_qn:
                uri = f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={data['roomid']}&qn={quality}&platform=web&https_url_req=1&ptype=16"
                re = r.get(uri)
                re.encoding = 'utf8'
                re = re.json()
                if re['code'] != 0:
                    print(f"{re['code']} {re['message']}")
                    return -2
                play_url = re['data']
                if play_url['current_qn'] == quality and 'durl' in play_url:
                    durl[quality] = play_url['durl']
            durl = durl[quality]
            if ns:
                print(f"{lan['OUTPUT9']}{quality},{quality_des_dict[quality]}{lan['ALL_URL_COUNT'].replace('<number>', str(len(durl)))}")
            video_quality = quality
        link_index = 0
        if 'vi' in ip:
            if ip['vi'] < len(durl):
                link_index = ip['vi']
                print(lan['URL_SELECTED'].replace('<index>', str(ip['vi'])))
            else:
                print(lan['INDEX_OUT_OF_RANGE'].replace('<max>', str(len(durl)-1)))
                return -7
        link = durl[link_index]
        url = link['url']
        ffmpeg = True  # 是否使用ffmpeg
        if JSONParser.getset(se, 'nf') == True:
            ffmpeg = False
        if 'yf' in ip:
            ffmpeg = ip['yf']
        if ffmpeg and os.system(f'ffmpeg -h{getnul()}') == 0:
            pass
        else:
            ffmpeg = False
        aria2c = True  # 是否使用aria2c
        if JSONParser.getset(se, 'a') == False:
            aria2c = False
        if 'ar' in ip:
            aria2c = ip['ar']
        if aria2c and os.system(f"aria2c -h{getnul()}") == 0:
            pass
        else:
            aria2c = False
        now = int(time.time())
        if not fin:
            fn = file.filtern(f"{data['title']}({tostr2(now)})")
        elif sv:
            fn = file.filtern(f"{data['title']}({data['roomid']},UID{data['uid']},{tostr2(now)},{quality_des_dict[video_quality]}).flv")
        else:
            fn = file.filtern(f"{data['title']}({data['roomid']},UID{data['uid']},{tostr2(now)}).flv")
        filen = f"{o}{fn}"
        if ffmpeg:
            lrh = True  # 是否进行去HTML化
            if JSONParser.getset(se, 'lrh') == False:
                lrh = False
            if 'lrh' in ip:
                lrh = ip['lrh']
            if lrh:
                data['des'] = bstr.rhtml(data['des'])
            cml = f"ffmpeg -user_agent \"{r.headers['User-Agent']}\" -referer \"{r.headers['referer']}\" -i \"{url}\""
            metadata = f" -metadata roomid=\"{data['roomid']}\" -metadata livetime=\"{data['livetime']}\" -metadata description=\"{bstr.f(data['des'])}\" -metadata title=\"{bstr.f(data['title'])}\" -metadata uid=\"{data['uid']}\" -metadata author=\"{bstr.f(data['name'])}\" -metadata authorsex=\"{data['sex']}\" -metadata sign=\"{bstr.f(data['sign'])}\" -metadata areaid=\"{data['areaid']}\" -metadata areaname=\"{bstr.f(data['areaname'])}\" -metadata pareaid=\"{data['pareaid']}\" -metadata pareaname=\"{bstr.f(data['pareaname'])}\" -metadata tags=\"{bstr.f(data['tags'])}\" -metadata hotwords=\"{bstr.f(bstr.gettags(data['hotwords']))}\""
            fileo = f"{metadata} -c copy \"{filen}\""
            nss = ""
            if not ns:
                nss = getnul()
            cm = f"{cml}{fileo}{nss}"
            os.system(cm)
        elif aria2c:
            read = dwaria2(r, filen, url, -1, False, ip, se)
            if read == -3:
                print(f"{lan['ERROR4']}{lan['ERROR5']}")  # aria2c 参数错误
                return -4
        else:
            re = r.get(url, stream=True)
            read = downloadstream(nte, ip, url, r, re, filen, -1, False)
    return 0


def downloadstream(nte,ip,uri,r,re,fn,size,d2,i=1,n=1,d=False,durz=-1,pre=-1) :
    if d :
        print(lan['OUTPUT1'].replace('<i>',str(i)).replace('<count>',str(n)))#正在开始下载第<i>个文件，共<count>个文件
    else :
        print(lan['OUTPUT2'])#正在开始下载
    if os.path.exists(fn) :
        fsize=file.getinfo({'a':fn,'f':''})['s']
        if fsize!=size and size!=-1:
            s=lan['OUTPUT19']#(文件大小不一致，建议覆盖)
        else :
            s=""
        bs=True
        fg=False
        if d2 and fsize==size and size!=-1 :
            print(lan['OUTPUT20'])#文件大小一致，跳过下载
            return 0
        if d2 and fsize!=size and size!=-1 :
            re.close()
            r2=requests.session()
            r2.headers=copydict(r.headers)
            if nte:
                r2.trust_env=False
            r2.proxies=r.proxies
            r2.headers.update({'Range':'bytes=%s-%s'%(fsize,size-1)})
            read=JSONParser.loadcookie(r2)
            if read!=0 :
                print(lan['ERROR2'])#读取cookies.json出现错误
                return -1
            re=r2.get(uri,stream=True)
            s=fsize
        if not d2 and ('y' in ip or 's' in ip):
            if 's' in ip:
                fg=True
                bs=False
            if 'y' in ip:
                if ip['y'] :
                    fg=True
                    bs=False
                else :
                    fg=False
                    bs=False
        if size==-1 :
            fg=True
            bs=False
        while bs and not d2 :
            inp=input(f"{lan['INPUT1'].replace('<filename>',fn)}{s}(y/n)")#"%s"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y':
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if (not d2 or size==-1 )and fg :
            try :
                os.remove(fn)
            except :
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                re.close()
                return 0
        elif not d2 :
            re.close()
            return 0
    t1=time.time()
    t2=time.time()
    s=0
    with open(fn,'ab') as f :
        for c in re.iter_content(chunk_size=1024) :
            if c :
                s=s+f.write(c)
                t1=time.time()
                if t1 - t2 > 1 and size == -1:
                    print(f"\r {file.info.size(s)}({s}B)", end = '', flush = True)
                    t2 = t1
                elif t1 - t2 > 1 and durz == -1:
                    if d :
                        print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    else :
                        print('\r %s(%sB)/%s(%sB)\t%.2f%%'%(file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    t2=t1
                elif t1-t2>1 and d:
                    print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%\t%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100,file.info.size(s+pre),s+pre,file.info.size(durz),durz,(s+pre)/durz*100),end='',flush=True)
                    t2=t1
    print()
    if s!= size and size!=-1 :
        print(lan['ERROR9'])#文件大小不匹配
        return -2
    f.close()
    return 0
def getfn(i, i2, data, vqs, hzm, o, fin, dmp: bool):
    if data['videos']==1 :
        if fin:
            return '%s%s'%(o,file.filtern('%s(AV%s,%s,P%s,%s,%s).%s'%(data['title'],data['aid'],data['bvid'],i2,data['page'][i2-1]['cid'],vqs[i],hzm[i])))
        else :
            return f"{o}{file.filtern(data['title'])}({file.filtern(vqs[i])}).{hzm[i]}"
    else :
        if fin and not dmp:
            return '%s%s'%(o,file.filtern(f"{data['title']}-{i2}.{data['page'][i2-1]['part']}(AV{data['aid']},{data['bvid']},P{i2},{data['page'][i2-1]['cid']},{vqs[i]}).{hzm[i]}"))
        elif not dmp:
            return f"{o}{file.filtern(data['title'])}-{i2}.{file.filtern(data['page'][i2-1]['part'])}({file.filtern(vqs[i])}).{hzm[i]}"
        elif fin:
            return '%s%s' % (o, file.filtern(f"{i2}.{data['page'][i2 - 1]['part']}(P{i2},{data['page'][i2 - 1]['cid']},{vqs[i]}).{hzm[i]}"))
        else:
            return f"{o}{i2}.{file.filtern(data['page'][i2 - 1]['part'])}({file.filtern(vqs[i])}).{hzm[i]}"
def getfn2(i,i2,f,vqs,hzm,fin) :
    if i['s']=='e' :
        if fin:
            return '%s/%s'%(f,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s,%s).%s'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[i2],hzm[i2])))
        else :
            return f"{f}/{i['i']+1}.{file.filtern(i['longTitle'])}({file.filtern(vqs[i2])}).{hzm[i2]}"
    else :
        if fin:
            return '%s/%s'%(f,file.filtern('%s.%s(%s%s,AV%s,%s,ID%s,%s,%s).%s'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[i2],hzm[i2])))
        else :
            return f"{f}/{file.filtern(i['title'])}{i['i']+1}.{file.filtern(i['longTitle'])}({file.filtern(vqs[i2])}).{hzm[i2]}"
def streamgetlength(r:requests.Session,uri):
    bs=True
    while bs:
        bs=False
        try :
            re=r.get(uri,stream=True)
            if re.headers.get('Content-Length')!=None :
                a=int(re.headers.get('Content-Length'))
            else :
                a=-1#无法获取长度，什么神必服务器
            re.close()
            return a
        except :
            print(lan['OUTPUT21'])#获取文件大小失败。尝试重新获取……
            bs=True
if __name__=="__main__" :
    print(lan['OUTPUT22'])#请使用start.py
