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
import requests
import JSONParser
import json
import file
import time
import os
from dictcopy import copydict,copylist
from re import search
from requests.structures import CaseInsensitiveDict
from biliTime import tostr2, tostr4
import bstr
from biliSub import downsub, ffinputstr, downlrc
from file import mkdir
from dict import delli,dellk
import platform
from command import gopt
from lang import getlan,getdict
import sys
import JSONParser2
from inspect import currentframe
from traceback import format_exc
from biliLRC import filterLRC
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
def dwaria2(r, fn, url, size, d2, ip, se, i=1, n=1, d=False):
    logg = None
    if 'logg' in ip:
        logg = ip['logg']
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
        if logg is not None:
            logg.write(f"d2 = {d2}\noa = {oa}", currentframe(), "DWARIA2 ARIA2")
        if d2 and not oa :
            print(lan['OUTPUT6'])#未找到aria2文件，跳过下载
            return 0
        if d2 and oa :
            cm=cm+' -c'
        if not d2 and ('y' in ip or 's' in ip):
            if 's' in ip:
                fg=True
                bs=False
            if 'y' in se:
                fg = se['y']
                bs = False
            if 'y' in ip:
                fg = ip['y']
                bs = False
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
                if logg is not None:
                    logg.write(format_exc(), currentframe(), "DWARIA2 REMOVE FILE FAILED")
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return 0
        elif not d2:
            return 0
    if isinstance(url,str) :
        cm=cm+' "'+url+'"'
    elif isinstance(url,list) :
        for i in url :
            cm=cm+' "'+i+'"'
    if logg is not None:
        logg.write(f"cm = {cm}", currentframe(), "DWARIA2 COMMAND LINE")
    re=os.system(cm)
    if logg is not None:
        logg.write(f"re = {re}", currentframe(), "DWARIA2 RESULT")
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
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
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
    if log:
        logg.write(f"ns = {ns}\nbp = {bp}\nnte = {nte}\no = '{o}'\ndmp = {dmp}\nF = {F}\nfin = {fin}", currentframe(), "Normal Video Download Var1")
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Normal Video Download Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败
        return -5
    nbd=True
    if JSONParser.getset(se,'bd')==True :
        nbd=False
    if 'bd' in ip:
        nbd=not ip['bd']
    vf = 'mkv'
    if 'vf' in se:
        vf = se['vf']
    if 'vf' in ip:
        vf = ip['vf']
    if log:
        logg.write(f"nbd = {nbd}\nvf = {vf}", currentframe(), "Normal Video Download Var2")
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    if i>1:
        url="%s?p=%s"%(url,i)
    r2.headers.update({'referer':url})
    r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','80',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    if log:
        logg.write(f"GET {url}", currentframe(), "Get Normal Video Webpage")
    re=r2.get(url)
    re.encoding='utf8'
    if log:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Normal Video Webpage Result")
    rs=search('__playinfo__=([^<]+)',re.text)
    napi=True #新api
    if rs!=None :
        re=json.loads(rs.groups()[0])
        if log:
            logg.write(f"re = {re}", currentframe(), "Get Normal Video Webpage Regex")
    elif data['videos']>=1 :
        uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=%s&otype=json&bvid=%s&fnver=0&fnval=80&session="%(data['page'][i-1]['cid'],125,data['bvid'])
        if log:
            logg.write(f"GET {uri}", currentframe(), "Get Normal Video Playurl")
        re=r2.get(uri)
        re.encoding="utf8"
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Normal Video Playurl Result")
        re=re.json()
        if re["code"]!=0 :
            print({"code":re["code"],"message":re["message"]})
            return -2
        napi=False
    else :
        return -2
    uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['page'][i-1]['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={r.cookies.get('buvid3')}"
    if log:
        logg.write(f"GET {uri}", currentframe(), "Get Normal Video Player.so")
    rr = r2.get(uri)
    rr.encoding='utf8'
    if log:
        logg.write(f"status = {rr.status_code}\n{rr.text}", currentframe(), "Get Normal Video Player.so Result")
    rs2=search(r'<subtitle>(.+)</subtitle>',rr.text)
    if F:
        print(f"{lan['OUTPUT8'].replace('<number>',str(i))}{data['page'][i-1]['part']}")#第<number>P：
    if rs2!=None :
        rs2=json.loads(rs2.groups()[0])
        if log:
            logg.write(f"rs2 = {rs2}", currentframe(), "Get Normal Video Player.so Sub Regex")
        JSONParser2.getsub(rs2,data)
    if "data" in re and "durl" in re['data']:
        vq=re["data"]["quality"]
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq=re["data"]["accept_quality"]
        durl={vq:re["data"]['durl']}
        durz={}
        vqs=""
        if log:
            logg.write(f"vq = {vq}\nvqd = {vqd}\navq = {avq}\nvqs = {vqs}", currentframe(), "Normal Video Download Var3")
        if not c or F:
            j=0
            for l in avq :
                if not l in durl :
                    if napi:
                        r2.cookies.set('CURRENT_QUALITY',str(l),domain='.bilibili.com',path='/')
                        if log:
                            logg.write(f"Current request quality: {l}\nGET {url}", currentframe(), "Get Normal Video Webpage2")
                        re=r2.get(url)
                        re.encoding='utf8'
                        if log:
                            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Normal Video Webpage2 Result")
                        rs=search('__playinfo__=([^<]+)',re.text)
                        if rs!=None :
                            re=json.loads(rs.groups()[0])
                            if log:
                                logg.write(f"re = {re}", currentframe(), "Get Normal Video Webpage2 Regex")
                        else :
                            return -2
                    else :
                        uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=%s&otype=json&bvid=%s&fnver=0&fnval=80"%(data['page'][i-1]['cid'],l,data['bvid'])
                        if log:
                            logg.write(f"GET {uri}", currentframe(), "Get Normal Video Playurl2")
                        re=r2.get(uri)
                        re.encoding='utf8'
                        if log:
                            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Normal Video Playurl2 Result")
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
            if log:
                logg.write(f"durl.keys() = {durl.keys()}\ndurz = {durz}\nvqs = {vqs}", currentframe(), "Normal Video Download Var4")
            r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
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
        if log:
            logg.write(f"vq = {vq}\ndurl = {durl}\ndurz = {durz}\nvqs = {vqs}", currentframe(), "Normal Video Download Var5")
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
        ma = True
        if JSONParser.getset(se, "ma") == False:
            ma = False
        if 'ma' in ip:
            ma=ip['ma']
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nff = {ff}\nma = {ma}", currentframe(), "Normal Video Download Var6")
        if ff and (len(durl) > 1 or ma) and os.path.exists(f'{filen}.{vf}') and os.system(f'ffmpeg -h{getnul()}')==0:
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
                inp = input(f"{lan['INPUT1'].replace('<filename>', '%s.%s' % (filen, vf))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove(f'{filen}.{vf}')
                except :
                    if log:
                        logg.write(format_exc(), currentframe(), "Normal Video Download Remove File Failed")
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
                    if log:
                        logg.write(f"fn = {fn}\nar = {ar}", currentframe(), "Normal Video Download Var7")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "Normal Video Download Var8")
                        if ab :
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        if log:
                            logg.write(f"GET {k['url']}", currentframe(), "Normal Video Download Video Request")
                        re=r2.get(k['url'],stream=True)
                        read = downloadstream(nte, ip, k['url'], r2, re, fn, k['size'], c3)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "Normal Video Download Var9")
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
                    if log:
                        logg.write(f"fn = {fn}\nar = {ar}\nj = {j}", currentframe(), "Normal Video Download Var10")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "Normal Video Download Var11")
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        if log:
                            logg.write(f"GET {k['url']}", currentframe(), "Normal Video Download Video Request2")
                        re=r2.get(k['url'],stream=True)
                        read = downloadstream(nte, ip, k['url'], r2, re, fn, k['size'], c3, j, len(durl), True, durz, com)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "Normal Video Download Var12")
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
            if oll:
                oll.add(fn)
            j=j+1
        if 'sub' in data :
            for s in data['sub']:
                downsub(r2, filen + "." + vf, s, ip, se, data, ns, i)
        imgf = file.spfn(filen + "." + vf)[0] + "." + file.geturlfe(data['pic'])  # 图片文件名
        imgs=avpicdownload(data,r,ip,se,imgf)#封面下载状况
        if log:
            logg.write(f"imgf = {imgf}\nimgs = {imgs}", currentframe(), "Normal Video Download Var13")
        if (len(durl)>1 or ma) and os.system('ffmpeg -h%s'%(getnul()))==0 and ff :
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt=int(time.time())
            sa=""
            sb=""
            nss=""
            imga=""
            imga2 = ""
            if not ns:
                nss=getnul()
            if 'sub' in data:
                sa, sb = ffinputstr(data['sub'], 2, 1, logg=logg)
            if imgs==0 and vf == "mkv":
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            elif imgs == 0 and vf == "mp4":
                imga = f' -i "{imgf}"'
                imga2 = f' -disposition:v:1 attached_pic'
                if 'sub' in data:
                    sa, sb = ffinputstr(data['sub'], 3, 1, logg=logg)
                else:
                    sb = ' -map 0 -map 2'
            if len(durl) > 1 and vf == "mkv":
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"aid={data['aid']}\n")
                    te.write(f"bvid={data['bvid']}\n")
                    te.write(f"ctime={tostr2(data['ctime'])}\n")
                    te.write(f"description={bstr.g(data['desc'])}\n")
                    te.write(f"p={i}P/{data['videos']}P\n")
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"pubdate={tostr2(data['pubdate'])}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"cid={data['page'][i-1]['cid']}\n")
                    te.write(f"atitle={bstr.g(data['title'])}\n")
                    te.write(f"part={bstr.g(data['page'][i-1]['part'])}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"purl={bstr.g(url)}\n")
                    te.write(f"tags={bstr.g(bstr.gettags(data['tags']))}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"INPUT FILE 'Temp/{data['aid']}_{tt}.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Temp File")
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata")
                ml = f"ffmpeg -f concat -safe 0 -i \"Temp/{data['aid']}_{tt}.txt\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{sa} -map_metadata 1{sb}{imga} -c copy \"{filen}.mkv\"{nss}"
            elif vf == "mkv":
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"aid={data['aid']}\n")
                    te.write(f"bvid={data['bvid']}\n")
                    te.write(f"ctime={tostr2(data['ctime'])}\n")
                    te.write(f"description={bstr.g(data['desc'])}\n")
                    te.write(f"p={i}P/{data['videos']}P\n")
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"pubdate={tostr2(data['pubdate'])}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"cid={data['page'][i-1]['cid']}\n")
                    te.write(f"atitle={bstr.g(data['title'])}\n")
                    te.write(f"part={bstr.g(data['page'][i-1]['part'])}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"purl={bstr.g(url)}\n")
                    te.write(f"tags={bstr.g(bstr.gettags(data['tags']))}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata2")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{sa} -map_metadata 1{sb}{imga} -c copy \"{filen}.mkv\"{nss}"
            elif len(durl) > 1:
                te = open('Temp/%s_%s.txt' % (file.filtern('%s' % (data['aid'])), tt), 'wt', encoding='utf8')
                j = 1
                for k in durl:
                    te.write("file '../%s_%s.%s'\n" % (filen, j, hzm))
                    j = j + 1
                te.close()
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(data['desc'])}\n")
                    te.write(f"album={bstr.g(data['title'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"album_artist={bstr.g(data['name'])}\n")
                    te.write(f"track={i}/{data['videos']}\n")
                    te.write(f"disc=1/1\n")
                    te.write(f"episode_id=AV{data['aid']}\n")
                    te.write(f"date={tostr4(data['pubdate'])}\n")
                    te.write(f"description={bstr.g(vqs)},{data['uid']}\\\n")
                    te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
                    te.write(f"{bstr.g(url)}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"INPUT FILE 'Temp/{data['aid']}_{tt}.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Temp File2")
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata3")
                ml = f"ffmpeg -f concat -safe 0 -i \"Temp/{data['aid']}_{tt}.txt\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{imga}{sa} -map_metadata 1{sb} -c copy -c:s mov_text{imga2} \"{filen}.mp4\"{nss}"
            else:
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(data['desc'])}\n")
                    te.write(f"album={bstr.g(data['title'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"album_artist={bstr.g(data['name'])}\n")
                    te.write(f"track={i}/{data['videos']}\n")
                    te.write(f"disc=1/1\n")
                    te.write(f"episode_id=AV{data['aid']}\n")
                    te.write(f"date={tostr4(data['pubdate'])}\n")
                    te.write(f"description={bstr.g(vqs)},{data['uid']}\\\n")
                    te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
                    te.write(f"{bstr.g(url)}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata4")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{imga}{sa} -map_metadata 1{sb} -c copy -c:s mov_text{imga2} \"{filen}.mp4\"{nss}"
            if log:
                logg.write(f"ml = {ml}", currentframe(), "Normal Video Download FFmpeg Command Line")
            re=os.system(ml)
            if log:
                logg.write(f"re = {re}", currentframe(), "Normal Video Download FFmpeg Return")
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                if oll:
                    oll.add(f"{filen}.{vf}")
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
            os.remove(f"Temp/{data['aid']}_{tt}_metadata.txt")
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
        if log:
            logg.write(f"vq = {vq}\nvqd = {vqd}\navq2 = {avq2}\navq3 = {avq3}\navq = {avq}", currentframe(), "Normal Video Download Var14")
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
                    if log:
                        logg.write(f"Current request quality: {j}\nGET {url}", currentframe(), "Get Normal Video Webpage3")
                    re=r2.get(url)
                    re.encoding='utf8'
                    if log:
                        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Normal Video Webpage3 Result")
                    rs=search('__playinfo__=([^<]+)',re.text)
                    if rs!=None :
                        re=json.loads(rs.groups()[0])
                        if log:
                            logg.write(f"re = {re}", currentframe(), "Get Normal Video Webpage3 Regex")
                    else :
                        return -2
                    if "data" in re and "dash" in re['data'] :
                        for j in re['data']['dash']['video'] :
                            if (str(j['id'])+j['codecs']) not in dash['video'] :
                                dash['video'][str(j['id'])+j['codecs']]=j
                                avq.append(str(j['id'])+j['codecs'])
                                avq3[j['id']]=0
                                bs=True
                        if log:
                            logg.write(f"avq = {avq}\navq3 = {avq3}", currentframe(), "Normal Video Download Var15")
                        break
                    else :
                        return -2
        r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
        nau=False #不存在音频
        if not 'audio' in re['data']['dash'] or re['data']['dash']['audio']==None :
            nau=True
        if log:
            logg.write(f"nau = {nau}", currentframe(), "Normal Video Download Var16")
        if not nau:
            for j in re['data']['dash']['audio']:
                dash['audio'][j['id']]=j
                aaq.append(j['id'])
            aaq.sort(reverse=True)
            if log:
                logg.write(f"aaq = {aaq}", currentframe(), "Normal Video Download Var17")
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
                print(f"{lan['OUTPUT9']}{vqd[0]}({dash['video']['width']}x{dash['video']['height']},{dash['video']['codecs']},{getfps(dash['video']['frame_rate'])})")#图质：
            dash['video']['size'] = streamgetlength(r2, dash['video']['base_url'], logg)
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['video']['size'])}({dash['video']['size']}B,{file.cml(dash['video']['size'],re['data']['timelength'])})")#大小：
                if not nau:
                    print(lan['OUTPUT16'])#音频轨：
                    print('ID：%s'%(dash['audio']['id']))
            if not nau:
                dash['audio']['size'] = streamgetlength(r2, dash['audio']['base_url'], logg)
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
                dash['video'][j]['size'] = streamgetlength(r2, dash['video'][j]['base_url'], logg)
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
                    dash['audio'][j]['size'] = streamgetlength(r2, dash['audio'][j]['base_url'], logg)
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
        if log:
            logg.write(f"vqs = {vqs}\ndash = {dash}", currentframe(), "Normal Video Download Var18")
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if data['videos']==1 :
            if not fin:
                filen = f"{o}{file.filtern(data['title'])}.{vf}"
            elif sv:
                if not nau:
                    filen = '%s%s' % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]},{vqs[1]}).{vf}"))
                else :
                    filen = '%s%s' % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]}).{vf}"))
            else :
                filen = '%s%s' % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']}).{vf}"))
        else :
            if not fin and not dmp:
                filen = f"{o}{file.filtern(data['title'])}-{i}.{file.filtern(data['page'][i-1]['part'])}.{vf}"
            elif not fin and dmp:
                filen = f"{o}{i}.{file.filtern(data['page'][i - 1]['part'])}.{vf}"
            elif sv and not dmp:
                if not nau:
                    filen = '%s%s' % (o, file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]},{vqs[1]}).{vf}"))
                else :
                    filen = '%s%s' % (o, file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']},{vqs[0]}).{vf}"))
            elif not dmp:
                filen = '%s%s' % (o, file.filtern(f"{data['title']}-{i}.{data['page'][i-1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i-1]['cid']}).{vf}"))
            elif sv:
                if not nau:
                    filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs[0]},{vqs[1]}).{vf}"))
                else:
                    filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs[0]}).{vf}"))
            else:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']}).{vf}"))
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
            if 'y' in se:
                fg = se['y']
                bs = False
            if 'y' in ip :
                fg = ip['y']
                bs = False
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
                    if log:
                        logg.write(format_exc(), currentframe(), "Normal Video Download Remove File Failed")
                    print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        durz=dash['video']['size']
        if not nau :
            durz=durz+dash['audio']['size']
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nhzm = {hzm}\nff = {ff}\ndurz = {durz}", currentframe(), "Normal Video Download Var19")
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
            if log:
                logg.write(f"ar = {ar}", currentframe(), "Normal Video Download Var20")
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if log:
                    logg.write(f"ab = {ab}", currentframe(), "Normal Video Download Var21")
                if ab:
                    read = dwaria2(r2, getfn(0, i, data, vqs, hzm, o, fin, dmp), geturll(dash['video']), dash['video']['size'], c3, ip, se, 1, 2, True)
                else :
                    read = dwaria2(r2, getfn(0, i, data, vqs, hzm, o, fin, dmp), dash['video']['base_url'], dash['video']['size'], c3, ip, se, 1, 2, True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                if log:
                    logg.write(f"GET {dash['video']['base_url']}", currentframe(), "Normal Video Download Video Request3")
                re=r2.get(dash['video']['base_url'],stream=True)
                read = downloadstream(nte, ip, dash['video']['base_url'], r2, re, getfn(0, i, data, vqs, hzm, o, fin, dmp), dash['video']['size'], c3, 1, 2, True, durz, 0)
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Video Download Var22")
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
        if oll:
            oll.add(getfn(0, i, data, vqs, hzm, o, fin, dmp))
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
            if log:
                logg.write(f"ar = {ar}", currentframe(), "Normal Video Download Var23")
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if log:
                    logg.write(f"ab = {ab}", currentframe(), "Normal Video Download Var24")
                if ab:
                    read = dwaria2(r2, getfn(1, i, data, vqs, hzm, o, fin, dmp), geturll(dash['audio']), dash['audio']['size'], c3, ip, se, 2, 2, True)
                else :
                    read = dwaria2(r2, getfn(1, i, data, vqs, hzm, o, fin, dmp), dash['audio']['base_url'], dash['audio']['size'], c3, ip, se, 2, 2, True)
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                if log:
                    logg.write(f"GET {dash['audio']['base_url']}", currentframe(), "Normal Video Download Video Audio Request")
                re=r2.get(dash['audio']['base_url'],stream=True)
                read = downloadstream(nte, ip, dash['audio']['base_url'], r2, re, getfn(1, i, data, vqs, hzm, o, fin, dmp), dash['audio']['size'], c3, 2, 2, True, durz, dash['video']['size'])
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Video Download Var25")
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
        if oll:
            oll.add(getfn(1, i, data, vqs, hzm, o, fin, dmp))
        if 'sub' in data :
            for s in data['sub']:
                downsub(r2, filen, s, ip, se, data, ns, i, dash['video']['width'], dash['video']['height'])
        imgf=file.spfn(filen)[0]+"."+file.geturlfe(data['pic'])#图片文件名
        imgs=avpicdownload(data,r,ip,se,imgf)#封面下载状况
        if log:
            logg.write(f"imgf = {imgf}\nimgs = {imgs}", currentframe(), "Normal Video Download Var26")
        if os.system('ffmpeg -h%s'%(getnul()))==0 and ff:
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt = int(time.time())
            sa=""
            sb=""
            nss=""
            imga=""
            imga2 = ""
            if not ns:
                nss=getnul()
            if 'sub' in data:
                if not nau:
                    sa, sb = ffinputstr(data['sub'], 3, 2, logg=logg)
                else :
                    sa, sb = ffinputstr(data['sub'], 2, 1, logg=logg)
            if imgs == 0 and vf == "mkv":
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            elif imgs == 0 and vf == "mp4":
                imga = f' -i "{imgf}"'
                imga2 = f' -disposition:v:1 attached_pic'
                if 'sub' in data:
                    if not nau:
                        sa, sb = ffinputstr(data['sub'], 4, 2, logg=logg)
                    else:
                        sa, sb = ffinputstr(data['sub'], 3, 1, logg=logg)
                else:
                    if not nau:
                        sb = ' -map 0 -map 1 -map 3'
                    else:
                        sb = ' -map 0 -map 2'
            if not nau and vf == "mkv":
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"description={bstr.g(data['desc'])}\n")
                    te.write(f"aid={data['aid']}\n")
                    te.write(f"bvid={data['bvid']}\n")
                    te.write(f"cid={data['page'][i-1]['cid']}\n")
                    te.write(f"atitle={bstr.g(data['title'])}\n")
                    te.write(f"pubdate={tostr2(data['pubdate'])}\n")
                    te.write(f"ctime={tostr2(data['ctime'])}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"p={i}P/{data['videos']}P\n")
                    te.write(f"part={bstr.g(data['page'][i-1]['part'])}\n")
                    te.write(f"vq={bstr.g(vqs[0])}\n")
                    te.write(f"aq={bstr.g(vqs[1])}\n")
                    te.write(f"purl={bstr.g(url)}\n")
                    te.write(f"tags={bstr.g(bstr.gettags(data['tags']))}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata5")
                ml = f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\" -i \"{getfn(1,i,data,vqs,hzm,o,fin,dmp)}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{sa} -map_metadata 2{sb}{imga} -c copy \"{filen}\"{nss}"
            elif vf == "mkv":
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"description={bstr.g(data['desc'])}\n")
                    te.write(f"aid={data['aid']}\n")
                    te.write(f"bvid={data['bvid']}\n")
                    te.write(f"cid={data['page'][i-1]['cid']}\n")
                    te.write(f"atitle={bstr.g(data['title'])}\n")
                    te.write(f"pubdate={tostr2(data['pubdate'])}\n")
                    te.write(f"ctime={tostr2(data['ctime'])}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"p={i}P/{data['videos']}P\n")
                    te.write(f"part={bstr.g(data['page'][i-1]['part'])}\n")
                    te.write(f"vq={bstr.g(vqs[0])}\n")
                    te.write(f"purl={bstr.g(url)}\n")
                    te.write(f"tags={bstr.g(bstr.gettags(data['tags']))}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata6")
                ml = f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{sa} -map_metadata 1{sb}{imga} -c copy \"{filen}\"{nss}"
            elif not nau:
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(data['desc'])}\n")
                    te.write(f"album={bstr.g(data['title'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"album_artist={bstr.g(data['name'])}\n")
                    te.write(f"track={i}/{data['videos']}\n")
                    te.write(f"disc=1/1\n")
                    te.write(f"episode_id=AV{data['aid']}\n")
                    te.write(f"date={tostr4(data['pubdate'])}\n")
                    te.write(f"description={bstr.g(vqs[0])},{bstr.g(vqs[1])},{data['uid']}\\\n")
                    te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
                    te.write(f"{bstr.g(url)}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata7")
                ml = f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\" -i \"{getfn(1,i,data,vqs,hzm,o,fin,dmp)}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{imga}{sa} -map_metadata 2{sb} -c copy -c:s mov_text{imga2} \"{filen}\"{nss}"
            else:
                tit = data['title']
                tit2 = data['page'][i - 1]['part']
                if tit2 != "":
                    tit = f'{tit} - {tit2}'
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(data['desc'])}\n")
                    te.write(f"album={bstr.g(data['title'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"album_artist={bstr.g(data['name'])}\n")
                    te.write(f"track={i}/{data['videos']}\n")
                    te.write(f"disc=1/1\n")
                    te.write(f"episode_id=AV{data['aid']}\n")
                    te.write(f"date={tostr4(data['pubdate'])}\n")
                    te.write(f"description={bstr.g(vqs[0])},{data['uid']}\\\n")
                    te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
                    te.write(f"{bstr.g(url)}\n")
                if log:
                    with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Video Download Metadata8")
                ml = f"ffmpeg -i \"{getfn(0,i,data,vqs,hzm,o,fin,dmp)}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{imga}{sa} -map_metadata 1{sb} -c copy -c:s mov_text{imga2} \"{filen}\"{nss}"
            if log:
                logg.write(f"ml = {ml}", currentframe(), "Normal Video Download FFmpeg Command Line2")
            re = os.system(ml)
            if log:
                logg.write(f"re = {re}", currentframe(), "Normal Video Download FFmpeg Return2")
            de=False
            if re==0 :
                print(lan['OUTPUT14'])#合并完成！
            if re==0:
                if oll:
                    oll.add(filen)
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
            os.remove(f"Temp/{data['aid']}_{tt}_metadata.txt")
def avsubdownload(i,url,data,r,se,ip,ud) :
    '''下载普通类视频字幕
    -1 文件夹创建失败'''
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
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
    dmp = False
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
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nfin = {fin}\ndmp = {dmp}", currentframe(), "Normal Video Download Subtitles Para")
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Normal Video Download Subtitles Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -1
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if log:
        logg.write(f"read = {read}", currentframe(), "Normal Video Download Subtitles Var")
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    if i>1:
        url="%s?p=%s"%(url,i)
    r2.headers.update({'referer':url})
    r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','80',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['page'][i-1]['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={r2.cookies.get('buvid3')}"
    if log:
        logg.write(f"GET {uri}", currentframe(), "Normal Video Download Subtitles Get Player.so")
    rr = r2.get(uri)
    rr.encoding='utf8'
    if log:
        logg.write(f"status = {rr.status_code}\n{rr.text}", currentframe(), "Normal Video Download Subtitles Get Player.so Result")
    rs2=search(r'<subtitle>(.+)</subtitle>',rr.text)
    if rs2!=None :
        rs2=json.loads(rs2.groups()[0])
        if log:
            logg.write(f"rs2 = {rs2}", currentframe(), "Normal Video Download Subtitles Player.so Regex")
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
        if log:
            logg.write(f"filen = {filen}", currentframe(), "Normal Video Download Subtitles Var2")
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
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
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
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nfin = {fin}\ndmp = {dmp}", currentframe(), "Normal Video Download Pic Para")
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Normal Video Download Pic Mkdir Failed")
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
    if log:
        logg.write(f"fn = {fn}", currentframe(), "Normal Video Download Pic Var")
    if os.path.exists(fn) :
        fg=False
        bs=True
        if not ns:
            fg=True
            bs=False
        if 'y' in se:
            fg = se['y']
            bs = False
        if 'y' in ip:
            fg = ip['y']
            bs = False
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
                if log:
                    logg.write(format_exc(), currentframe(), "Normal Video Download Pic Remove File Failed")
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return -3
    if log:
        logg.write(f"GET {data['pic']}", currentframe(), "Normal Video Download Pic Request")
    re=r.get(data['pic'])
    if log:
        logg.write(f"status = {re.status_code}", currentframe(), "Normal Video Download Pic Request Result")
    if re.status_code==200 :
        f=open(fn,'wb')
        f.write(re.content)
        f.close()
        if oll:
            oll.add(fn)
        if ns:
            print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        return 0
    else :
        print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
        return -2


def avaudiodownload(data: dict, r: requests.session, i: int, ip: dict, se: dict, url: str, c: bool, c3: bool, ud: dict) -> int:
    """仅下载音频
    -1 读取cookies出现错误
    -2 API解析错误
    -3 下载错误
    -4 aria2c参数错误
    -5 创建文件夹失败
    -6 缺少必要参数
    -7 不支持durl
    -8 不存在音频流"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
    ns = True
    if 's' in ip:
        ns = False
    nte = False
    if JSONParser.getset(se, 'te') == False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    bp = False  # 删除无用文件时是否保留封面图片
    if JSONParser.getset(se, 'bp') == True:
        bp = True
    if 'bp' in ip:
        bp = ip['bp']
    o = 'Download/'
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    dmp = False  # 是否为多P视频创建单独文件夹
    if JSONParser.getset(se, 'dmp') == True:
        dmp = True
    if 'dmp' in ip:
        dmp = ip['dmp']
    if data['videos'] == 1:
        dmp = False
    F = False  # 进输出音频信息
    if 'F' in ip:
        F = True
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    if dmp:
        if not fin:
            o = f"{o}{file.filtern(data['title'])}/"
        else:
            o = "%s%s/" % (o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']})"))
    if log:
        logg.write(f"ns = {ns}\nnte = {nte}\nbp = {bp}\no = '{o}'\ndmp = {dmp}\nF = {F}\nfin = {fin}", currentframe(), "Normal Video Audio Download Para")
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Normal Video Audio Download Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建文件夹"<dirname>"失败
        return -5
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    r2 = requests.Session()
    r2.headers = copydict(r.headers)
    if nte:
        r2.trust_env = False
    r2.proxies = r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if log:
        logg.write(f"read = {read}", currentframe(), "Normal Video Audio Download Var1")
    if read != 0:
        print(lan['ERROR2'])  # 读取cookies.json出现错误
        return -1
    if i>1:
        url = f"{url}?p={i}"
    r2.headers.update({'referer': url})
    r2.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
    r2.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
    r2.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
    r2.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
    if log:
        logg.write(f"GET {url}", currentframe(), "Audio Download Get Normal Video Webpage")
    re = r2.get(url)
    re.encoding = 'utf8'
    if log:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Download Get Normal Video Webpage Result")
    rs = search(r'__playinfo__=([^<]+)', re.text)
    if rs is not None:
        re = json.loads(rs.groups()[0])
        if log:
            logg.write(f"re = {re}", currentframe(), "Audio Download Webpage Regex")
    elif data['videos'] >= 1:
        uri = f"https://api.bilibili.com/x/player/playurl?cid={data['page'][i - 1]['cid']}&qn=125&otype=json&bvid={data['bvid']}&fnver=0&fnval=80"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Audio Download Get Playurl")
        re = r2.get(uri)
        re.encoding = "utf8"
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Download Get Playurl Result")
        re = re.json()
        if re["code"] != 0:
            print({"code": re["code"], "message": re["message"]})
            return -2
    else:
        return -2
    uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['page'][i-1]['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={r.cookies.get('buvid3')}"
    if log:
        logg.write(f"GET {uri}", currentframe(), "Audio Download Get Player.so")
    rr = r2.get(uri)
    rr.encoding = 'utf8'
    if log:
        logg.write(f"status = {rr.status_code}\n{rr.text}", currentframe(), "Audio Download Get Player.so Result")
    rs2 = search(r'<subtitle>(.+)</subtitle>', rr.text)
    if rs2 is not None:
        rs2 = json.loads(rs2.groups()[0])
        if log:
            logg.write(f"rs2 = {rs2}", currentframe(), "Normal Video Audio Download Var2")
        JSONParser2.getsub(rs2, data)
    if F:
        print(f"{lan['OUTPUT8'].replace('<number>', str(i))}{data['page'][i - 1]['part']}")#第<number>P
    if 'data' in re and 'durl' in re['data']:
        print(lan['NOT_SUP_DURL'])  # 不支持durl流
        return -7
    elif 'data' in re and 'dash' in re['data']:
        if not 'audio' in re['data']['dash'] or re['data']['dash']['audio'] is None:
            print(lan['NO_AUDIO'])
            return -8
        accept_audio_quality = []
        dash = {}
        for j in re['data']['dash']['audio']:
            dash[j['id']] = j
            accept_audio_quality.append(j['id'])
        accept_audio_quality.sort(reverse=True)
        if log:
            logg.write(f"accept_audio_quality = {accept_audio_quality}\ndash.keys() = {dash.keys()}", currentframe(), "Normal Video Audio Download Var3")
        if c and not F:
            dash = dash[accept_audio_quality[0]]
            if ns:
                print(lan['OUTPUT16'])  # 音频轨
                print(f"ID:{dash['id']}")
            dash['size'] = streamgetlength(r2, dash['base_url'], logg)
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['size'])}({dash['size']}B,{file.cml(dash['size'], re['data']['timelength'])})")  # 大小：
            vqs = accept_audio_quality[0]
        else:
            if ns or (not ns and F):
                print(lan['OUTPUT16'])  # 音频轨：
            k = 0
            for j in accept_audio_quality:
                if ns or (not ns and F):
                    print(f"{k + 1}.ID:{j}")
                dash[j]['size'] = streamgetlength(r2, dash[j]['base_url'], logg)
                if ns or (not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(dash[j]['size'])}({dash[j]['size']}B,{file.cml(dash[j]['size'], re['data']['timelength'])})")  # 大小：
                k = k + 1
            if F:
                return 0
            if len(accept_audio_quality) > 1:
                bs = True
                fi = True
                while bs:
                    if fi and 'a' in ip:
                        fi = False
                        inp = ip['a']
                    elif ns:
                        inp = input(lan['INPUT5'])  # 请选择音质：
                    else:
                        print(lan['ERROR6'])  # 请使用-a <id>选择音质
                        return -6
                    if len(inp) > 0 and inp.isnumeric():
                        if int(inp) > 0 and int(inp) < len(accept_audio_quality) + 1:
                            bs = False
                            dash = dash[accept_audio_quality[int(inp) - 1]]
                            if ns:
                                print(lan['OUTPUT17'].replace('<audioquality>', str(accept_audio_quality[int(inp) - 1])))  # 已选择%s音质
                            vqs = accept_audio_quality[int(inp) - 1]
            else:
                dash = dash[accept_audio_quality[0]]
                vqs = accept_audio_quality[0]
        if log:
            logg.write(f"dash = {dash}\nvqs = {vqs}", currentframe(), "Normal Video Audio Download Var4")
        sv = True
        if JSONParser.getset(se, 'sv') == False:
            sv = False
        if 'sv' in ip:
            sv = ip['sv']
        if data['videos'] == 1:
            if not fin:
                filen = f"{o}{file.filtern(data['title'])}"
            elif sv:
                filen = '%s%s' %(o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i - 1]['cid']},{vqs})"))
            else:
                filen = '%s%s' %(o, file.filtern(f"{data['title']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i - 1]['cid']})"))
        else:
            if not fin and not dmp:
                filen = f"{o}{file.filtern(data['title'])}-{i}.{file.filtern(data['page'][i - 1]['part'])}"
            elif not fin and dmp:
                filen = f"{o}{i}.{file.filtern(data['page'][i - 1]['part'])}"
            elif sv and not dmp:
                filen = '%s%s' % (o, file.filtern(f"{data['title']}-{i}.{data['page'][i - 1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i - 1]['cid']},{vqs})"))
            elif not dmp:
                filen = '%s%s' % (o, file.filtern(f"{data['title']}-{i}.{data['page'][i - 1]['part']}(AV{data['aid']},{data['bvid']},P{i},{data['page'][i - 1]['cid']})"))
            elif sv:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']},{vqs})"))
            else:
                filen = '%s%s' % (o, file.filtern(f"{i}.{data['page'][i - 1]['part']}(P{i},{data['page'][i - 1]['cid']})"))
        hzm = file.geturlfe(dash['base_url'])
        ffmpeg = True
        if JSONParser.getset(se, 'nf') == True:
            ffmpeg = False
        if 'yf' in ip:
            ffmpeg = ip['yf']
        if ffmpeg and os.system(f'ffmpeg -h{getnul()}') != 0:
            ffmpeg = False
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nhzm = {hzm}\nffmpeg = {ffmpeg}", currentframe(), "Normal Video Audio Download Var4")
        if ffmpeg and os.path.exists(f"{filen}.m4a"):
            overwrite = False
            bs = True
            if not ns:
                overwrite = True
                bs = False
            if 'y' in se:
                overwrite = se['y']
                bs = False
            if 'y' in ip:
                overwrite = ip['y']
                bs = False
            while bs:
                inp = input(f"{lan['INPUT1'].replace('<filename>', filen + '.m4a')}(y/n)")  # "%s"文件已存在，是否覆盖？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        overwrite = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if overwrite:
                try:
                    os.remove(f"{filen}.m4a")
                except:
                    if log:
                        logg.write(format_exc(), currentframe(), "Normal Video Audio Download Error")
                    print(lan['OUTPUT7'])  # 删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        bs2 = True
        aria2c = True
        if JSONParser.getset(se, 'a') == False:
            aria2c = False
        if 'ar' in ip:
            aria2c = ip['ar']
        if aria2c and os.system(f'aria2c -h{getnul()}') != 0:
            aria2c = False
        if aria2c:
            ab = True  # 是否使用备用地址
            if JSONParser.getset(se, 'ab') == False:
                ab = False
            if 'ab' in ip:
                ab = ip['ab']
        if log:
            logg.write(f"aria2c = {aria2c}", currentframe(), "Normal Video Audio Download Var5")
        while bs2:
            bs2 = False
            if aria2c:
                if ab:
                    read = dwaria2(r2, f"{filen}.{hzm}", geturll(dash), dash['size'], c3, ip, se)
                else:
                    read = dwaria2(r2, f"{filen}.{hzm}", dash['base_url'], dash['size'], c3, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Normal Video Audio Download Aria2c Return")
                if read == -3:
                    print(lan['ERROR4'])  # aria2c 参数错误
                    return -4
            else:
                re = r2.get(dash['base_url'], stream=True)
                read = downloadstream(nte, ip, dash['base_url'], r2, re, f"{filen}.{hzm}", dash['size'], c3)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Normal Video Audio Download Return")
            if read == -1:
                return -1
            elif read == -2:
                bs = True
                rc = False
                if not ns:
                    bs = False
                read = JSONParser.getset(se, 'rd')
                if read == True:
                    bs = False
                    rc = True
                elif read == False:
                    bs = False
                if 'r' in ip:
                    rc = ip['r']
                    bs = False
                while bs:
                    inp = input(f"{lan['INPUT3']}(y/n)")  # 文件下载失败，是否重新下载？
                    if len(inp) > 0:
                        if inp[0].lower() == 'y':
                            bs = False
                            rc = True
                        elif inp[0].lower() == 'n':
                            bs = False
                if rc:
                    if os.path.exists(f"{filen}.{hzm}"):
                        os.remove(f"{filen}.{hzm}")
                    bs2 = True
                else:
                    return -3
        if oll:
            oll.add(f"{filen}.{hzm}")
        if 'sub' in data:
            nal = False
            if 'nal' in se:
                nal = se['nal']
            if 'nal' in ip:
                nal = ip['nal']
            if log:
                logg.write(f"nal = {nal}", currentframe(), "Normal Video Audio Download Var6")
            if len(data['sub']) == 1 and nal:
                downlrc(r2, f'{filen}.m4a', data['sub'][0], ip, se, data, ns, i, nal)
            else:
                for s in data['sub']:
                    downlrc(r2, f'{filen}.m4a', s, ip, se, data, ns, i)
        imgf = file.spfn(filen + ".m4a")[0] + "." + file.geturlfe(data['pic'])  # 图片文件名
        if log:
            logg.write(f"imgf = {imgf}", currentframe(), "Normal Video Audio Download Var7")
        imgs = avpicdownload(data, r, ip, se, imgf)  # 封面下载状况
        if log:
            logg.write(f"imgs = {imgs}", currentframe(), "Normal Video Audio Download Var8")
        if ffmpeg:
            print(lan['CONV_M4S_TO_M4A'])
            tt = int(time.time())
            nss = ""
            imga = ""
            imga2 = ""
            if not ns:
                nss = getnul()
            if imgs == 0:
                imga = f" -i \"{imgf}\""
                imga2 = " -map 0 -map 2 -disposition:v:0 attached_pic"
            tit = data['page'][i - 1]['part']
            if tit == "":
                tit = data['title']
            with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                te.write(';FFMETADATA1\n')
                te.write(f"title={bstr.g(tit)}\n")
                te.write(f"comment={bstr.g(data['desc'])}\n")
                te.write(f"album={bstr.g(data['title'])}\n")
                te.write(f"artist={bstr.g(data['name'])}\n")
                te.write(f"album_artist={bstr.g(data['name'])}\n")
                te.write(f"track={i}/{data['videos']}\n")
                te.write(f"disc=1/1\n")
                te.write(f"episode_id=AV{data['aid']}\n")
                te.write(f"date={tostr4(data['pubdate'])}\n")
                te.write(f"description={bstr.g(vqs)},{data['uid']}\\\n")
                te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
                te.write(f"{bstr.g(url)}\n")
            if log:
                with open(f"Temp/{data['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                    logg.write(f"METADATAFILE 'Temp/{data['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Video Audio Download Metadata")
            cm = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{data['aid']}_{tt}_metadata.txt\"{imga} -map_metadata 1 -c copy{imga2} \"{filen}.m4a\"{nss}"
            if log:
                logg.write(f"cm = {cm}", currentframe(), "Normal Video Audio Download Ffmpeg Commandline")
            re = os.system(cm)
            if log:
                logg.write(f"re = {re}", currentframe(), "Normal Video Audio Download Ffmpeg Return")
            if re == 0:
                if oll:
                    oll.add(f"{filen}.m4a")
                print(lan['COM_CONV'])
                delete = False
                bs = True
                if not ns:
                    bs = False
                read = JSONParser.getset(se, 'ad')
                if read == True:
                    delete = True
                    bs = False
                elif read == False:
                    bs = False
                if 'ad' in ip:
                    delete = ip['ad']
                    bs = False
                while bs:
                    inp = input(f"{lan['INPUT4']}(y/n)")  # 是否删除中间文件？
                    if len(inp) > 0:
                        if inp[0].lower() == 'y':
                            delete = True
                            bs = False
                        elif inp[0].lower() == 'n':
                            bs = False
                if delete:
                    os.remove(f"{filen}.{hzm}")
                    if imgs == 0 and not bp:
                        os.remove(imgf)
            os.remove(f"Temp/{data['aid']}_{tt}_metadata.txt")
    return 0


def epvideodownload(i,url,data,r,c,c3,se,ip,ud):
    """下载番剧等视频"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
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
    if log:
        logg.write(f"che = {che}\nns = {ns}\nbp = {bp}\nnte = {nte}\no = '{o}'", currentframe(), "Bangumi Video Download Var")
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Bangumi Video Download Mkdir Failed")
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
    vf = 'mkv'
    if 'vf' in se:
        vf = se['vf']
    if 'vf' in ip:
        vf = ip['vf']
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    if log:
        logg.write(f"F = {F}\nfdir = {fdir}\nfin = {fin}\nvf = {vf}", currentframe(), "Bangumi Video Download Var2")
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if log:
        logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Var3")
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    r2.headers.update({'referer':url2})
    r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','80',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    if not che :
        napi = True
        paok = False
        if log:
            logg.write(f"GET {url2}", currentframe(), "Bangumi Video Download Get Webpage")
        re=r2.get(url2)
        re.encoding='utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Webpage Result")
        rs=search('__playinfo__=([^<]+)',re.text)
        rs2=search('__PGC_USERSTATE__=([^<]+)',re.text)
        if rs != None:
            re=json.loads(rs.groups()[0])
            if log:
                logg.write(f"re = {re}", currentframe(), "Bangumi Video Download Webpage Regex")
            paok = True
        else:
            napi = False
            uri = f"https://api.bilibili.com/pgc/player/web/playurl?cid={i['cid']}&qn=125&type=&otype=json&fourk=1&bvid={i['bvid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
            if log:
                logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download Get Playurl")
            re = r2.get(uri)
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl Result")
            re = re.json()
            if re['code'] != 0:
                print(f"{re['code']} {re['message']}")
            else:
                re['data'] = re['result']
                paok = True
        if not paok and rs2!=None:
            rs2=json.loads(rs2.groups()[0])
            if log:
                logg.write(f"rs2 = {rs2}", currentframe(), "Bangumi Video Download Webpage Regex2")
            if 'dialog' in rs2:
                print(rs2['dialog']['title'])
            if rs2['area_limit']:
                print(lan['ERROR7'])#有区域限制，请尝试使用代理。
            return -2
        elif not paok:
            return -2
    else :
        uri = f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn=125&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
        if log:
            logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download Get Playurl2")
        re=r2.get(uri)
        re.encoding='utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl2 Result")
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
        if log:
            logg.write(f"vqd = {vqd}\navq = {avq}\navq2 = {avq2}\navq3 = {avq3}", currentframe(), "Bangumi Video Download Var4")
        bs=True
        rtry = 0
        while bs:
            bs=False
            for j in avq2 :
                if j not in avq3 :
                    if ud['vip']<1 and j<=80 and j!=74:
                        bs=True #防止非大会员进入无限死循环
                    elif ud['vip']>0 :
                        bs=True #大会员一旦强制获取所有
                    if not che:
                        if napi:
                            r2.cookies.set('CURRENT_QUALITY', str(j), domain='.bilibili.com', path='/')
                            if log:
                                logg.write(f"Current request quality: {j}\nGET {url2}", currentframe(), "Bangumi Video Download Get Webpage2")
                            re = r2.get(url2)
                            re.encoding = 'utf8'
                            if log:
                                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Webpage2 Result")
                            rs = search('__playinfo__=([^<]+)', re.text)
                            if rs != None:
                                re = json.loads(rs.groups()[0])
                                if log:
                                    logg.write(f"re = {re}", currentframe(), "Bangumi Video Download Webpage2 Regex")
                            else:
                                napi = False
                                uri = f"https://api.bilibili.com/pgc/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&bvid={i['bvid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
                                if log:
                                    logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download Get Playurl3")
                                re = r2.get(uri)
                                if log:
                                    logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl3 Result")
                                re = re.json()
                                if re['code'] != 0:
                                    print(f"{re['code']} {re['message']}")
                                    return -2
                                re['data'] = re['result']
                        else:
                            uri = f"https://api.bilibili.com/pgc/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&bvid={i['bvid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
                            if log:
                                logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download Get Playurl4")
                            re = r2.get(uri)
                            if log:
                                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl4 Result")
                            re = re.json()
                            if re['code'] != 0:
                                print(f"{re['code']} {re['message']}")
                                return -2
                            re['data'] = re['result']
                    else :
                        uri = f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
                        if log:
                            logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download Get Playurl5")
                        re = r2.get(uri)
                        re.encoding='utf8'
                        if log:
                            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl5 Result")
                        re=re.json()
                    if "data" in re and "dash" in re['data'] :
                        for j in re['data']['dash']['video'] :
                            if (str(j['id'])+j['codecs']) not in dash['video'] :
                                t=str(j['id'])+j['codecs']
                                dash['video'][t]=j
                                avq.append(t)
                                avq3[j['id']]=0
                                bs=True
                        if log:
                            logg.write(f"avq = {avq}\navq3 = {avq3}", currentframe(), "Bangumi Video Download Var5")
                        break
                    else :
                        return -2
            if bs:
                rtry = rtry + 1
                if log:
                    logg.write(f"rtry = {rtry}", currentframe(), "Bangumi Video Download Var6")
                if rtry > 1:
                    napi = False
                if rtry > 3:
                    bs = False
        if not che:
            r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
        for j in re['data']['dash']['audio']:
            dash['audio'][j['id']]=j
            aaq.append(j['id'])
        aaq.sort(reverse=True)
        if log:
            logg.write(f"aaq = {aaq}", currentframe(), "Bangumi Video Download Var7")
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
                print(f"{lan['OUTPUT9']}{vqd[0]}({dash['video']['width']}x{dash['video']['height']},{dash['video']['codecs']},{getfps(dash['video']['frame_rate'])})")#图质：
            dash['video']['size'] = streamgetlength(r2, dash['video']['base_url'], logg)
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['video']['size'])}({dash['video']['size']}B,{file.cml(dash['video']['size'],re['data']['timelength'])})")#大小
                print(lan['OUTPUT16'])#音频轨：
                print('ID：%s'%(dash['audio']['id']))
            dash['audio']['size'] = streamgetlength(r2, dash['audio']['base_url'], logg)
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
                dash['video'][j]['size'] = streamgetlength(r2, dash['video'][j]['base_url'], logg)
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
                dash['audio'][j]['size'] = streamgetlength(r2, dash['audio'][j]['base_url'], logg)
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
        if log:
            logg.write(f"vqs = {vqs}\ndash = {dash}", currentframe(), "Bangumi Video Download Var8")
        sv=True
        if JSONParser.getset(se,'sv')==False :
            sv=False
        if 'sv' in ip:
            sv=ip['sv']
        if i['s']=='e' :
            if not fin:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i']+1}.{i['longTitle']}.{vf}"))
            elif sv:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i']+1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']},{vqs[0]},{vqs[1]}).{vf}"))
            else :
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i']+1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']}).{vf}"))
        else :
            if not fin:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}.{vf}"))
            elif sv:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']},{vqs[0]},{vqs[1]}).{vf}"))
            else :
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']}).{vf}"))
        hzm=[file.geturlfe(dash['video']['base_url']),file.geturlfe(dash['audio']['base_url'])]
        ff=True
        if JSONParser.getset(se,'nf')==True :
            ff=False
        if 'yf' in ip :
            if ip['yf']:
                ff=True
            else :
                ff=False
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nhzm = {hzm}\nff = {ff}", currentframe(), "Bangumi Video Download Var9")
        if ff and os.path.exists(filen) and os.system('ffmpeg -h%s'%(getnul()))==0 :
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
                    if log:
                        logg.write(format_exc(), currentframe(), "Bangumi Video Download Remove File Failed")
                    print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        durz=dash['video']['size']+dash['audio']['size']
        if log:
            logg.write(f"durz = {durz}", currentframe(), "Bangumi Video Download Var10")
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
            if log:
                logg.write(f"ar = {ar}", currentframe(), "Bangumi Video Download Var11")
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if log:
                    logg.write(f"ab = {ab}", currentframe(), "Bangumi Video Download Var12")
                if ab:
                    read=dwaria2(r2,getfn2(i,0,fdir,vqs,hzm,fin),geturll(dash['video']),dash['video']['size'],c3,ip,se,1,2,True)
                else :
                    read=dwaria2(r2,getfn2(i,0,fdir,vqs,hzm,fin),dash['video']['base_url'],dash['video']['size'],c3,ip,se,1,2,True)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Var13")
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                if log:
                    logg.write(f"GET {dash['video']['base_url']}", currentframe(), "Bangumi Video Download File Download")
                re=r2.get(dash['video']['base_url'],stream=True)
                read=downloadstream(nte, ip, dash['video']['base_url'], r2, re, getfn2(i,0,fdir,vqs,hzm,fin), dash['video']['size'], c3, 1, 2, True, durz, 0)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Var14")
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
        if oll:
            oll.add(getfn2(i, 0, fdir, vqs, hzm, fin))
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
            if log:
                logg.write(f"ar = {ar}", currentframe(), "Bangumi Video Download Var15")
            if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                ab=True
                if JSONParser.getset(se,'ab')==False :
                    ab=False
                if 'ab' in ip:
                    if ip['ab']:
                        ab=True
                    else :
                        ab=False
                if log:
                    logg.write(f"ab = {ab}", currentframe(), "Bangumi Video Download Var16")
                if ab:
                    read=dwaria2(r2,getfn2(i,1,fdir,vqs,hzm,fin),geturll(dash['audio']),dash['audio']['size'],c3,ip,se,2,2,True)
                else :
                    read=dwaria2(r2,getfn2(i,1,fdir,vqs,hzm,fin),dash['audio']['base_url'],dash['audio']['size'],c3,ip,se,2,2,True)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Var17")
                if read==-3 :
                    print(lan['ERROR4'])#aria2c 参数错误
                    return -4
            else :
                if log:
                    logg.write(f"GET {dash['audio']['base_url']}", currentframe(), "Bangumi Video Download File Download2")
                re=r2.get(dash['audio']['base_url'],stream=True)
                read=downloadstream(nte,ip,dash['audio']['base_url'],r2,re,getfn2(i,1,fdir,vqs,hzm,fin),dash['audio']['size'],c3,2,2,True,durz,dash['video']['size'])
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Var18")
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
        if oll:
            oll.add(getfn2(i, 1, fdir, vqs, hzm, fin))
        if not che:
            imgf=f"{file.spfn(filen)[0]}.{file.geturlfe(i['cover'])}"#图片文件名
            imgs=eppicdownload(i,data,r,ip,se,imgf)#封面下载状况
            if log:
                logg.write(f"imgf = {imgf}\nimgs = {imgs}", currentframe(), "Bangumi Video Download Var19")
        if os.system('ffmpeg -h%s'%(getnul()))==0 and ff:
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt = int(time.time())
            nss=""
            imga=""
            imga2 = ""
            if not ns:
                nss=getnul()
            if not che and imgs == 0 and vf == "mkv":
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            elif not che and imgs == 0 and vf == "mp4":
                imga = f' -i "{imgf}" -map 0 -map 1 -map 3'
                imga2 = f' -disposition:v:1 attached_pic'
            if vf == "mkv":
                mediaInfo = data['mediaInfo']
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                author = "哔哩哔哩番剧"
                uid = "928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f"{mediaInfo['up_info']['mid']}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"id={mediaInfo['id']}\n")
                    te.write(f"ssid={mediaInfo['ssId']}\n")
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"series={bstr.g(mediaInfo['series'])}\n")
                    te.write(f"description={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"pubtime={bstr.g(mediaInfo['time'])}\n")
                    te.write(f"atitle={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"eptitle={bstr.g(i['longTitle'])}\n")
                    te.write(f"titleformat={bstr.g(i['titleFormat'])}\n")
                    te.write(f"epid={i['id']}\n")
                    te.write(f"aid={i['aid']}\n")
                    te.write(f"bvid={i['bvid']}\n")
                    te.write(f"cid={i['cid']}\n")
                    te.write(f"aq={bstr.g(vqs[1])}\n")
                    te.write(f"vq={bstr.g(vqs[0])}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"author={bstr.g(author)}\n")
                    te.write(f"uid={uid}\n")
                    te.write(f"purl={bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata")
                cm = f"ffmpeg -i \"{getfn2(i,0,fdir,vqs,hzm,fin)}\" -i \"{getfn2(i,1,fdir,vqs,hzm,fin)}\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\" -map_metadata 2{imga} -c copy \"{filen}\"{nss}"
            elif vf == "mp4":
                le = 1
                if 'sections' in data and len(data['sections']) > 1:
                    le = len(data['sections']) + 1
                sectionType = i['sectionType']
                le2 = len(data['epList'])
                if sectionType > 0:
                    for section in data['sections']:
                        if section['type'] == sectionType:
                            le2 = len(section['epList'])
                            break
                mediaInfo = data['mediaInfo']
                author = "哔哩哔哩番剧"
                uid = ",UID928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f",UID{mediaInfo['up_info']['mid']}"
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"album={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"album_artist={bstr.g(author)}\n")
                    te.write(f"track={i['i'] + 1}/{le2}\n")
                    te.write(f"disc={sectionType + 1}/{le}\n")
                    te.write(f"episode_id=AV{i['aid']},EP{i['id']}\n")
                    te.write(f"date={bstr.g(mediaInfo['time'][:10])}\n")
                    te.write(f"description={bstr.g(vqs[0])},{bstr.g(vqs[1])}{uid},SS{mediaInfo['ssId']}\\\n")
                    te.write(f"{bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata2")
                cm = f"ffmpeg -i \"{getfn2(i,0,fdir,vqs,hzm,fin)}\" -i \"{getfn2(i,1,fdir,vqs,hzm,fin)}\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\"{imga} -map_metadata 2 -c copy{imga2} \"{filen}\"{nss}"
            if log:
                logg.write(f"cm = {cm}", currentframe(), "Bangumi Video Download FFmpeg Command Line")
            re = os.system(cm)
            if log:
                logg.write(f"re = {re}", currentframe(), "Bangumi Video Download FFmpeg Return")
            de=False
            if re==0 :
                print(lan['OUTPUT14'])#合并完成！
            if re==0:
                if oll:
                    oll.add(filen)
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
            os.remove(f"Temp/{i['aid']}_{tt}_metadata.txt")
    elif 'data' in re and 'durl' in re['data'] :
        vq=re["data"]["quality"]
        vqd = getqualitytransl(re["data"]["accept_description"])
        avq=re["data"]["accept_quality"]
        durl={vq:re["data"]['durl']}
        durz={}
        vqs=""
        if log:
            logg.write(f"vq = {vq}\nvqd = {vqd}\navq = {avq}\ndurl.keys() = {durl.keys()}", currentframe(), "Bangumi Video Download Var20")
        if not c or F:
            j=0
            for l in avq :
                if not l in durl :
                    if not che :
                        r2.cookies.set('CURRENT_QUALITY',str(l),domain='.bilibili.com',path='/')
                        if log:
                            logg.write(f"Current request quality: {l}\nGET {url2}", currentframe(), "Bangumi Video Download Get Webpage3")
                        re=r2.get(url2)
                        re.encoding='utf8'
                        if log:
                            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Webpage3 Result")
                        rs=search('__playinfo__=([^<]+)',re.text)
                        if rs!=None:
                            re=json.loads(rs.groups()[0])
                            if log:
                                logg.write(f"re = {re}", currentframe(), "Bangumi Video Download Webpage3 Regex")
                        else :
                            return -2
                    else :
                        uri = f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn={j}&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
                        if log:
                            logg.write(f"GET {uri}", currentframe(), "Bangumi Video Download  Get Playurl6")
                        re=r2.get(uri)
                        re.encoding='utf8'
                        if log:
                            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Video Download Get Playurl6 Result")
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
            if log:
                logg.write(f"avq = {avq}\nvqd = {vqd}", currentframe(), "Bangumi Video Download Var21")
            r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
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
        if log:
            logg.write(f"vqs = {vqs}\ndurl = {durl}", currentframe(), "Bangumi Video Download Var21")
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
        ma = True
        if JSONParser.getset(se, "ma") == False:
            ma = False
        if 'ma' in ip:
            ma=ip['ma']
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nff = {ff}\nma = {ma}", currentframe(), "Bangumi Video Download Var22")
        if ff and (len(durl)>1 or ma) and os.path.exists('%s.mkv'%(filen)) and os.system('ffmpeg -h%s'%(getnul()))==0 :
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
                inp = input(f"{lan['INPUT1'].replace('<filename>', '%s.%s'%(filen, vf))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove(f'{filen}.{vf}')
                except :
                    if log:
                        logg.write(format_exc(), currentframe(), "Bangumi Video Download Remove File Failed2")
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
                    if log:
                        logg.write(f"fn = {fn}\nar = {ar}", currentframe(), "Bangumi Video Download Var23")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "Bangumi Video Download Var24")
                        if ab :
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se)
                        if log:
                            logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Video Download Return3")
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        if log:
                            logg.write(f"GET {k['url']}", currentframe(), "Bangumi Video Download Video Download Request")
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3)
                        if log:
                            logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Video Download Return4")
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
                    if log:
                        logg.write(f"fn = {fn}\nar = {ar}", currentframe(), "Bangumi Video Download Var25")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "Bangumi Video Download Var26")
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if log:
                            logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Video Download Return5")
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        if log:
                            logg.write(f"GET {k['url']}", currentframe(), "Bangumi Video Download Video Download Request2")
                        re=r2.get(k['url'],stream=True)
                        read=downloadstream(nte,ip,k['url'],r2,re,fn,k['size'],c3,j,len(durl),True,durz,com)
                        if log:
                            logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Video Download Return6")
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
            if oll:
                oll.add(fn)
            j=j+1
        if not che:
            imgf = f"{file.spfn(filen + '.' + vf)[0]}.{file.geturlfe(i['cover'])}"#图片文件名
            imgs=eppicdownload(i,data,r,ip,se,imgf)#封面下载状况
            if log:
                logg.write(f"imgf = {imgf}\nimgs = {imgs}", currentframe(), "Bangumi Video Download Var27")
        if (len(durl)>1 or ma) and os.system('ffmpeg -h%s'%(getnul()))==0 and ff :
            print(lan['OUTPUT13'])#将用ffmpeg自动合成
            tt=int(time.time())
            nss=""
            imga=""
            imga2 = ""
            if not ns:
                nss=getnul()
            if not che and imgs == 0 and vf == "mkv":
                imga=f" -attach \"{imgf}\" -metadata:s:t mimetype=image/jpeg"
            elif not che and imgs == 0 and vf == "mp4":
                imga = f' -i "{imgf}" -map 0 -map 2'
                imga2 = f' -disposition:v:1 attached_pic'
            if len(durl) > 1 and vf == "mkv":
                mediaInfo = data['mediaInfo']
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(i['id'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                author = "哔哩哔哩番剧"
                uid = "928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f"{mediaInfo['up_info']['mid']}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"id={mediaInfo['id']}\n")
                    te.write(f"ssid={mediaInfo['ssId']}\n")
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"series={bstr.g(mediaInfo['series'])}\n")
                    te.write(f"description={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"pubtime={bstr.g(mediaInfo['time'])}\n")
                    te.write(f"atitle={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"eptitle={bstr.g(i['longTitle'])}\n")
                    te.write(f"titleformat={bstr.g(i['titleFormat'])}\n")
                    te.write(f"epid={i['id']}\n")
                    te.write(f"aid={i['aid']}\n")
                    te.write(f"bvid={i['bvid']}\n")
                    te.write(f"cid={i['cid']}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"author={bstr.g(author)}\n")
                    te.write(f"uid={uid}\n")
                    te.write(f"purl={bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['id']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"INPUT FILE 'Temp/{i['id']}_{tt}.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Input File")
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata3")
                ml=f"ffmpeg -f concat -safe 0 -i \"Temp/{file.filtern('%s'%(i['id']))}_{tt}.txt\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\" -map_metadata 1{imga} -c copy \"{filen}.mkv\"{nss}"
            elif vf == "mkv":
                mediaInfo = data['mediaInfo']
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                author = "哔哩哔哩番剧"
                uid = "928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f"{mediaInfo['up_info']['mid']}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"id={mediaInfo['id']}\n")
                    te.write(f"ssid={mediaInfo['ssId']}\n")
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"series={bstr.g(mediaInfo['series'])}\n")
                    te.write(f"description={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"pubtime={bstr.g(mediaInfo['time'])}\n")
                    te.write(f"atitle={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"eptitle={bstr.g(i['longTitle'])}\n")
                    te.write(f"titleformat={bstr.g(i['titleFormat'])}\n")
                    te.write(f"epid={i['id']}\n")
                    te.write(f"aid={i['aid']}\n")
                    te.write(f"bvid={i['bvid']}\n")
                    te.write(f"cid={i['cid']}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"author={bstr.g(author)}\n")
                    te.write(f"uid={uid}\n")
                    te.write(f"purl={bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata4")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\" -map_metadata 1{imga} -c copy \"{filen}.mkv\"{nss}"
            elif len(durl) > 1:
                te = open('Temp/%s_%s.txt' % (file.filtern('%s'%(i['id'])), tt), 'wt',encoding='utf8')
                j = 1
                for k in durl:
                    te.write("file '../%s_%s.%s'\n" % (filen, j, hzm))
                    j = j + 1
                te.close()
                le = 1
                if 'sections' in data and len(data['sections']) > 1:
                    le = len(data['sections']) + 1
                sectionType = i['sectionType']
                le2 = len(data['epList'])
                if sectionType > 0:
                    for section in data['sections']:
                        if section['type'] == sectionType:
                            le2 = len(section['epList'])
                            break
                mediaInfo = data['mediaInfo']
                author = "哔哩哔哩番剧"
                uid = ",UID928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f",UID{mediaInfo['up_info']['mid']}"
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"album={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"album_artist={bstr.g(author)}\n")
                    te.write(f"track={i['i'] + 1}/{le2}\n")
                    te.write(f"disc={sectionType + 1}/{le}\n")
                    te.write(f"episode_id=AV{i['aid']},EP{i['id']}\n")
                    te.write(f"date={bstr.g(mediaInfo['time'][:10])}\n")
                    te.write(f"description={bstr.g(vqs)}{uid},SS{mediaInfo['ssId']}\\\n")
                    te.write(f"{bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['id']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"INPUT FILE 'Temp/{i['id']}_{tt}.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Input File2")
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata5")
                ml = f"ffmpeg -f concat -safe 0 -i \"Temp/{file.filtern('%s'%(i['id']))}_{tt}.txt\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\"{imga} -map_metadata 1 -c copy{imga2} \"{filen}\"{nss}"
            else:
                le = 1
                if 'sections' in data and len(data['sections']) > 1:
                    le = len(data['sections']) + 1
                sectionType = i['sectionType']
                le2 = len(data['epList'])
                if sectionType > 0:
                    for section in data['sections']:
                        if section['type'] == sectionType:
                            le2 = len(section['epList'])
                            break
                mediaInfo = data['mediaInfo']
                author = "哔哩哔哩番剧"
                uid = ",UID928123"
                if che:
                    author = mediaInfo['up_info']['uname']
                    uid = f",UID{mediaInfo['up_info']['mid']}"
                tit = i['titleFormat']
                tit2 = i['longTitle']
                if tit2 != "":
                    tit = f"{mediaInfo['title']} - {tit} {tit2}"
                else:
                    tit = f"{mediaInfo['title']} - {tit}"
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(tit)}\n")
                    te.write(f"comment={bstr.g(mediaInfo['evaluate'])}\n")
                    te.write(f"album={bstr.g(mediaInfo['title'])}\n")
                    te.write(f"artist={bstr.g(author)}\n")
                    te.write(f"album_artist={bstr.g(author)}\n")
                    te.write(f"track={i['i'] + 1}/{le2}\n")
                    te.write(f"disc={sectionType + 1}/{le}\n")
                    te.write(f"episode_id=AV{i['aid']},EP{i['id']}\n")
                    te.write(f"date={bstr.g(mediaInfo['time'][:10])}\n")
                    te.write(f"description={bstr.g(vqs)}{uid},SS{mediaInfo['ssId']}\\\n")
                    te.write(f"{bstr.g(url2)}\n")
                if log:
                    with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Video Download Metadata6")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\"{imga} -map_metadata 1 -c copy{imga2} \"{filen}\"{nss}"
            if log:
                logg.write(f"ml = {ml}", currentframe(), "Bangumi Video Download FFmpeg Command Line2")
            re=os.system(ml)
            if log:
                logg.write(f"re = {re}", currentframe(), "Bangumi Video Download FFmpeg Return2")
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                if oll:
                    oll.add(filen)
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
            os.remove(f"Temp/{i['aid']}_{tt}_metadata.txt")
            if len(durl)>1:
                os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(i['id'])),tt))
def eppicdownload(i,data,r:requests.Session,ip,se,fn:str=None)->int :
    """下载封面图片
    fn 指定文件名
    -1 文件夹创建失败
    -2 封面文件下载失败
    -3 覆盖文件失败"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
    ns=True
    if 's' in ip:
        ns=False
    o="Download/"
    read=JSONParser.getset(se,'o')
    if read!=None :
        o=read
    if 'o' in ip:
        o=ip['o']
    if log:
        logg.write(f"ns = {ns}\no = '{o}'", currentframe(), "Bangumi Video Cover Download Var")
    try :
        if not os.path.exists(o) :
            mkdir(o)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Bangumi Video Cover Download Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -1
    fdir=f"{o}{file.filtern('%s(SS%s)'%(data['mediaInfo']['title'],data['mediaInfo']['ssId']))}"#SS文件夹
    if log:
        logg.write(f"fdir = {fdir}", currentframe(), "Bangumi Video Cover Download Var2")
    try :
        if not os.path.exists(fdir) :
            mkdir(fdir)
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Bangumi Video Cover Download Mkdir Failed2")
        print(lan['ERROR1'].replace('<dirname>',fdir))#创建文件夹"<dirname>"失败。
        return -1
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    cf2=data['mediaInfo']['cover']
    fn2=f"{fdir}/cover.{file.geturlfe(cf2)}"
    if log:
        logg.write(f"fin = {fin}\ncf2 = {cf2}\nfn2 = {fn2}", currentframe(), "Bangumi Video Cover Download Var3")
    if not os.path.exists(fn2) :
        if log:
            logg.write(f"GET {cf2}", currentframe(), "Bangumi Video Cover Download Request")
        re=r.get(cf2)
        if log:
            logg.write(f"status = {re.status_code}", currentframe(), "Bangumi Video Cover Download Result")
        if re.status_code==200 :
            f=open(fn2,'wb')
            f.write(re.content)
            f.close()
            if oll:
                oll.add(fn2)
            if ns:
                print(lan['OUTPUT23'].replace('<filename>',fn2))#封面图片下载完成。
        else :
            print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
    if 'che' in  data :
        if 'brief' in data :
            ii=1
            for uri in data['brief'] :
                chepicdownload(uri, r, fdir, ii, ns, logg, oll)
                ii=ii+1
        return 0
    cf=i['cover']
    if fn==None :
        if fin:
            fn=f"{fdir}/{file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s).%s'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],file.geturlfe(cf)))}"
        else :
            fn=f"{fdir}/{file.filtern('%s.%s.%s'%(i['i']+1,i['longTitle'],file.geturlfe(cf)))}"
    if log:
        logg.write(f"cf = {cf}\nfn = {fn}", currentframe(), "Bangumi Video Cover Download Var4")
    if os.path.exists(fn) :
        fg=False
        bs=True
        if not ns:
            fg=True
            bs=False
        if 'y' in se:
            fg = se['y']
            bs = False
        if 'y' in ip:
            fg = ip['y']
            bs = False
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
                if log:
                    logg.write(format_exc(), currentframe(), "Bangumi Video Cover Download Remove File Failed")
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return -3
    if log:
        logg.write(f"GET {cf}", currentframe(), "Bangumi Video Cover Download Request2")
    re=r.get(cf)
    if log:
        logg.write(f"status = {re.status_code}", currentframe(), "Bangumi Video Cover Download Result2")
    if re.status_code==200 :
        f=open(fn,'wb')
        f.write(re.content)
        f.close()
        if oll:
            oll.add(fn)
        if ns:
            print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        return 0
    else :
        print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
        return -2


def epaudiodownload(i: dict, url: str, data: dict, r: requests.Session, c: bool, c3: bool, se:dict, ip:dict, ud:dict):
    """仅下载音频
    -1 读取cookies出现错误
    -2 API解析错误
    -3 下载错误
    -4 aria2c参数错误
    -5 创建文件夹失败
    -6 缺少必要参数
    -7 不支持durl
    -8 不存在音频流"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
    che = False
    if 'che' in data:
        che = True
    ns = True
    if 's' in ip:
        ns = False
    nte = False
    if JSONParser.getset(se, 'te') == False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    bp = False  # 删除无用文件时是否保留封面图片
    if JSONParser.getset(se, 'bp') == True:
        bp = True
    if 'bp' in ip:
        bp = ip['bp']
    o = 'Download/'
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    if log:
        logg.write(f"che = {che}\nns = {ns}\nnte = {nte}\nbp = {bp}\no = '{o}'", currentframe(), "Bangumi Download Audio Only Var")
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Bangumi Download Audio Only Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建%s文件夹失败
        return -5
    F = False  # 仅输出音频信息
    if 'F' in ip:
        F = True
    if F:
        print(f"{i['titleFormat']}:{i['longTitle']}")
    fdir = '%s%s' % (o, file.filtern(f"{data['mediaInfo']['title']}(SS{data['mediaInfo']['ssId']})"))
    if che:
        url2 = f"https://www.bilibili.com/cheese/play/ep{i['id']}"
    else:
        url2 = f"https://www.bilibili.com/bangumi/play/ep{i['id']}"
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    if log:
        logg.write(f"F = {F}\nfdir = {fdir}\nurl2 = {url2}\nfin = {fin}", currentframe(), "Bangumi Download Audio Only Var2")
    try:
        if not os.path.exists(fdir):
            mkdir(fdir)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Bangumi Download Audio Only Mkdir Failed2")
        print(lan['ERROR1'].replace('<dirname>', fdir))  # 创建%s文件夹失败
        return -5
    r2 = requests.Session()
    r2.headers = copydict(r.headers)
    if nte:
        r2.trust_env = False
    r2.proxies = r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if log:
        logg.write(f"read = {read}", currentframe(), "Bangumi Download Audio Only Var3")
    if read != 0:
        print(lan['ERROR2'])  # 读取cookies.json出现错误
        return -1
    r2.headers.update({'referer': url2})
    r2.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
    r2.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
    r2.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
    r2.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
    if not che:
        paok = False
        if log:
            logg.write(f"GET {url2}", currentframe(), "Bangumi Download Audio Only Get Webpage")
        re = r2.get(url2)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Download Audio Only Get Webpage Result")
        rs = search(r'__playinfo__=([^<]+)', re.text)
        rs2 = search(r'__PGC_USERSTATE__=([^<]+)', re.text)
        if rs != None:
            re = json.loads(rs.groups()[0])
            paok = True
            if log:
                logg.write(f"re = {re}", currentframe(), "Bangumi Download Audio Only Webpage Regex")
        else:
            uri = f"https://api.bilibili.com/pgc/player/web/playurl?cid={i['cid']}&qn=125&type=&otype=json&fourk=1&bvid={i['bvid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
            if log:
                logg.write(f"GET {uri}", currentframe(), "Bangumi Download Audio Only Get Playurl")
            re = r2.get(uri)
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Bangumi Download Audio Only Get Playurl Result")
            re = re.json()
            if re['code'] != 0:
                print(f"{re['code']} {re['message']}")
            else:
                re['data'] = re['result']
                paok = True
        if not paok and rs2!=None:
            rs2 = json.loads(rs2.groups()[0])
            if log:
                logg.write(f"rs2 = {rs2}", currentframe(), "Bangumi Download Audio Only Webpage Regex2")
            if 'dialog' in rs2:
                print(rs2['dialog']['title'])
            if rs2['area_limit']:
                print(lan['ERROR7'])  # 有区域限制，请尝试使用代理。
            return -2
        elif not paok:
            return -2
    else:
        uri = f"https://api.bilibili.com/pugv/player/web/playurl?cid={i['cid']}&qn=125&type=&otype=json&fourk=1&avid={i['aid']}&ep_id={i['id']}&fnver=0&fnval=80&session="
        if log:
            logg.write(f"GET {uri}", currentframe(), "Purchased Courses' Download Audio Only Get Playurl")
        re = r2.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Purchased Courses' Download Audio Only Get Playurl Result")
        re = re.json()
    if 'data' in re and 'durl' in re['data']:
        print(lan['NOT_SUP_DURL'])  # 不支持durl流
        return -7
    elif 'data' in re and 'dash' in re['data']:
        if not 'audio' in re['data']['dash'] or re['data']['dash']['audio'] is None:
            print(lan['NO_AUDIO'])
            return -8
        accept_audio_quality = []
        dash = {}
        for j in re['data']['dash']['audio']:
            dash[j['id']] = j
            accept_audio_quality.append(j['id'])
        accept_audio_quality.sort(reverse=True)
        if log:
            logg.write(f"accept_audio_quality = {accept_audio_quality}", currentframe(), "Bangumi Download Audio Only Var4")
        if c and not F:
            dash = dash[accept_audio_quality[0]]
            if ns:
                print(lan['OUTPUT16'])  # 音频轨
                print(f"ID:{dash['id']}")
            dash['size'] = streamgetlength(r2, dash['base_url'], logg)
            if ns:
                print(f"{lan['OUTPUT10']}{file.info.size(dash['size'])}({dash['size']}B,{file.cml(dash['size'], re['data']['timelength'])})")  # 大小：
            vqs = accept_audio_quality[0]
        else:
            if ns or (not ns and F):
                print(lan['OUTPUT16'])  # 音频轨：
            k = 0
            for j in accept_audio_quality:
                if ns or (not ns and F):
                    print(f"{k + 1}.ID:{j}")
                dash[j]['size'] = streamgetlength(r2, dash[j]['base_url'], logg)
                if ns or (not ns and F):
                    print(f"{lan['OUTPUT10']}{file.info.size(dash[j]['size'])}({dash[j]['size']}B,{file.cml(dash[j]['size'], re['data']['timelength'])})")  # 大小：
                k = k + 1
            if F:
                return 0
            if len(accept_audio_quality) > 1:
                bs = True
                fi = True
                while bs:
                    if fi and 'a' in ip:
                        fi = False
                        inp = ip['a']
                    elif ns:
                        inp = input(lan['INPUT5'])  # 请选择音质：
                    else:
                        print(lan['ERROR6'])  # 请使用-a <id>选择音质
                        return -6
                    if len(inp) > 0 and inp.isnumeric():
                        if int(inp) > 0 and int(inp) < len(accept_audio_quality) + 1:
                            bs = False
                            dash = dash[accept_audio_quality[int(inp) - 1]]
                            if ns:
                                print(lan['OUTPUT17'].replace('<audioquality>', str(accept_audio_quality[int(inp) - 1])))  # 已选择%s音质
                            vqs = accept_audio_quality[int(inp) - 1]
            else:
                dash = dash[accept_audio_quality[0]]
                vqs = accept_audio_quality[0]
        if log:
            logg.write(f"vqs = {vqs}\ndash = {dash}", currentframe(), "Bangumi Download Audio Only Var5")
        sv = True
        if JSONParser.getset(se, 'sv') == False:
            sv = False
        if 'sv' in ip:
            sv = ip['sv']
        if i['s'] == 'e':
            if not fin:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i'] + 1}.{i['longTitle']}"))
            elif sv:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i'] + 1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']},{vqs})"))
            else:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['i'] + 1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']})"))
        else:
            if not fin:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i'] + 1}.{i['longTitle']}"))
            elif sv:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i'] + 1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']},{vqs})"))
            else:
                filen = '%s/%s' % (fdir, file.filtern(f"{i['title']}{i['i'] + 1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']})"))
        hzm = file.geturlfe(dash['base_url'])
        ffmpeg = True
        if JSONParser.getset(se, 'nf') == True:
            ffmpeg = False
        if 'yf' in ip:
            ffmpeg = ip['yf']
        if ffmpeg and os.system(f'ffmpeg -h{getnul()}') != 0:
            ffmpeg = False
        if log:
            logg.write(f"sv = {sv}\nfilen = {filen}\nhzm = {hzm}\nffmpeg = {ffmpeg}", currentframe(), "Bangumi Download Audio Only Var6")
        if ffmpeg and os.path.exists(f"{filen}.m4a"):
            overwrite = False
            bs = True
            if not ns:
                overwrite = True
                bs = False
            if 'y' in se:
                overwrite = se['y']
                bs = False
            if 'y' in ip:
                overwrite = ip['y']
                bs = False
            while bs:
                inp = input(f"{lan['INPUT1'].replace('<filename>', filen + '.m4a')}(y/n)")  # "%s"文件已存在，是否覆盖？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        overwrite = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if overwrite:
                try:
                    os.remove(f"{filen}.m4a")
                except:
                    if log:
                        logg.write(format_exc(), currentframe(), "Bangumi Download Audio Only Remove File Failed")
                    print(lan['OUTPUT7'])  # 删除原有文件失败，跳过下载
                    return 0
            else:
                return 0
        bs2 = True
        aria2c = True
        if JSONParser.getset(se, 'a') == False:
            aria2c = False
        if 'ar' in ip:
            aria2c = ip['ar']
        if aria2c and os.system(f'aria2c -h{getnul()}') != 0:
            aria2c = False
        if log:
            logg.write(f"aria2c = {aria2c}", currentframe(), "Bangumi Download Audio Only Var7")
        if aria2c:
            ab = True  # 是否使用备用地址
            if JSONParser.getset(se, 'ab') == False:
                ab = False
            if 'ab' in ip:
                ab = ip['ab']
            if log:
                logg.write(f"ab = {ab}", currentframe(), "Bangumi Download Audio Only Var8")
        while bs2:
            bs2 = False
            if aria2c:
                if ab:
                    read = dwaria2(r2, f"{filen}.{hzm}", geturll(dash), dash['size'], c3, ip, se)
                else:
                    read = dwaria2(r2, f"{filen}.{hzm}", dash['base_url'], dash['size'], c3, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe() ,"Bangumi Download Audio Only Download File Return")
                if read == -3:
                    print(lan['ERROR4'])  # aria2c 参数错误
                    return -4
            else:
                if log:
                    logg.write(f"GET {dash['base_url']}", currentframe(), "Bangumi Download Audio Only Download File")
                re = r2.get(dash['base_url'], stream=True)
                read = downloadstream(nte, ip, dash['base_url'], r2, re, f"{filen}.{hzm}", dash['size'], c3)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Download Audio Only Download File Return2")
            if read == -1:
                return -1
            elif read == -2:
                bs = True
                rc = False
                if not ns:
                    bs = False
                read = JSONParser.getset(se, 'rd')
                if read == True:
                    bs = False
                    rc = True
                elif read == False:
                    bs = False
                if 'r' in ip:
                    rc = ip['r']
                    bs = False
                while bs:
                    inp = input(f"{lan['INPUT3']}(y/n)")  # 文件下载失败，是否重新下载？
                    if len(inp) > 0:
                        if inp[0].lower() == 'y':
                            bs = False
                            rc = True
                        elif inp[0].lower() == 'n':
                            bs = False
                if rc:
                    if os.path.exists(f"{filen}.{hzm}"):
                        os.remove(f"{filen}.{hzm}")
                    bs2 = True
                else:
                    return -3
        if oll:
            oll.add(f"{filen}.{hzm}")
        if not che:
            imgf = f"{file.spfn(filen + '.m4a')[0]}.{file.geturlfe(i['cover'])}"
            imgs = eppicdownload(i, data, r, ip, se, imgf)
            if log:
                logg.write(f"imgf = {imgf}\nimgs = {imgs}", currentframe(), "Bangumi Download Audio Only Var9")
        if ffmpeg:
            print(lan['CONV_M4S_TO_M4A'])
            tt = int(time.time())
            nss = ""
            imga = ""
            imga2 = ""
            if not ns:
                nss = getnul()
            if not che and imgs == 0:
                imga = f" -i \"{imgf}\""
                imga2 = " -map 0 -map 2 -disposition:v:0 attached_pic"
            le = 1
            if 'sections' in data and len(data['sections']) > 1:
                le = len(data['sections']) + 1
            sectionType = i['sectionType']
            le2 = len(data['epList'])
            if sectionType > 0:
                for section in data['sections']:
                    if section['type'] == sectionType:
                        le2 = len(section['epList'])
                        break
            mediaInfo = data['mediaInfo']
            author = "哔哩哔哩番剧"
            uid = ",UID928123"
            if che:
                author = mediaInfo['up_info']['uname']
                uid = f",UID{mediaInfo['up_info']['mid']}"
            tit = i['titleFormat']
            tit2 = i['longTitle']
            if tit2 != "":
                tit = f"{tit} {tit2}"
            with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                te.write(';FFMETADATA1\n')
                te.write(f"title={bstr.g(tit)}\n")
                te.write(f"comment={bstr.g(mediaInfo['evaluate'])}\n")
                te.write(f"album={bstr.g(mediaInfo['title'])}\n")
                te.write(f"artist={bstr.g(author)}\n")
                te.write(f"album_artist={bstr.g(author)}\n")
                te.write(f"track={i['i'] + 1}/{le2}\n")
                te.write(f"disc={sectionType + 1}/{le}\n")
                te.write(f"episode_id=AV{i['aid']},EP{i['id']}\n")
                te.write(f"date={bstr.g(mediaInfo['time'][:10])}\n")
                te.write(f"description={bstr.g(vqs)}{uid},SS{mediaInfo['ssId']}\\\n")
                te.write(f"{bstr.g(url2)}\n")
            if log:
                with open(f"Temp/{i['aid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                    logg.write(f"METADATAFILE 'Temp/{i['aid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Bangumi Download Audio Only Metadata")
            cm = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{i['aid']}_{tt}_metadata.txt\"{imga} -map_metadata 1 -c copy{imga2} \"{filen}.m4a\"{nss}"
            if log:
                logg.write(f"cm = {cm}", currentframe(), "Bangumi Download Audio Only FFmpeg CommandLine")
            re = os.system(cm)
            if log:
                logg.write(f"re = {re}", currentframe(), "Bangumi Download Audio Only FFmpeg Return")
            if re == 0:
                if oll:
                    oll.add(f"{filen}.m4a")
                print(lan['COM_CONV'])
                delete = False
                bs = True
                if not ns:
                    bs = False
                read = JSONParser.getset(se, 'ad')
                if read == True:
                    delete = True
                    bs = False
                elif read == False:
                    bs = False
                if 'ad' in ip:
                    delete = ip['ad']
                    bs = False
                while bs:
                    inp = input(f"{lan['INPUT4']}(y/n)")  # 是否删除中间文件？
                    if len(inp) > 0:
                        if inp[0].lower() == 'y':
                            delete = True
                            bs = False
                        elif inp[0].lower() == 'n':
                            bs = False
                if delete:
                    os.remove(f"{filen}.{hzm}")
                    if not che and imgs == 0 and not bp:
                        os.remove(imgf)
            os.remove(f"Temp/{i['aid']}_{tt}_metadata.txt")
    return 0


def chepicdownload(url:str, r:requests.session, fdir:str, i:int, ns:bool, logg=None, oll=None) :
    fn=f"{fdir}/des{i}.{file.geturlfe(url)}"
    if logg is not None:
        logg.write(f"fn = {fn}", currentframe(), "Purchased Courses' Cover Download Var")
    if not os.path.exists(fn) :
        if logg is not None:
            logg.write(f"GET {url}", currentframe(), "Purchased Courses' Cover Download Request")
        re=r.get(url)
        if logg is not None:
            logg.write(f"status = {re.status_code}", currentframe(), "Purchased Courses' Cover Download Result")
        if re.status_code==200 :
            f=open(fn,'wb')
            f.write(re.content)
            f.close()
            if oll:
                oll.add(fn)
            if ns:
                print(lan['OUTPUT23'].replace('<filename>',fn))#封面图片下载完成。
        else :
            print(f"{lan['OUTPUT24']}HTTP {re.status_code}")#下载封面图片时发生错误：
def smdownload(r:requests.Session,i:dict,c:bool,se:dict,ip:dict) :
    """下载小视频
    c 继续下载"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
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
        if log:
            logg.write(format_exc(), currentframe(), "ERROR MKDIR")
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
    vf = 'mkv'
    if 'vf' in se:
        vf = se['vf']
    if 'vf' in ip:
        vf = ip['vf']
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nnte = {nte}\nF = {F}\nfin = {fin}\nvf = '{vf}'", currentframe(), "SMDOWNLOAD PARAMETERS")
    r2=requests.session()
    r2.headers=copydict(r.headers)
    r2.proxies=r.proxies
    if nte:
        r2.trust_env=False
    r2.headers.update({'referer':'https://vc.bilibili.com/video/%s'%(i['id'])})
    fz = streamgetlength(r2, i['video_playurl'], logg)
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
    ma = True
    if JSONParser.getset(se, "ma") == False:
        ma = False
    if 'ma' in ip:
        ma=ip['ma']
    if log:
        logg.write(f"sv = {sv}\nslt = {slt}\nsn = {sn}\nfilen = {filen}\nff = {ff}\nma = {ma}", currentframe(), "SMDOWNLOAD PARAMETERS 2")
    if ff and ma and os.path.exists(f'{filen}.{vf}') and os.system('ffmpeg -h%s'%(getnul()))==0 :
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
            inp = input(f"{lan['INPUT1'].replace('<filename>', '%s.%s'%(filen, vf))}(y/n)")
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            try :
                os.remove(f'{filen}.{vf}')
            except :
                if log:
                    logg.write(format_exc(), currentframe(), "SMDOWNLOAD REMOVE FILE FAILED")
                print(lan['OUTPUT7'])#删除原有文件失败，跳过下载
                return 0
        else:
            return 0
    hzm=file.geturlfe(i['video_playurl'])
    if ma and ff and os.system(f'ffmpeg -h{getnul()}') == 0 and vf == "mp4":
        hzm = "temp.mp4"
    fn='%s.%s'%(filen,hzm)
    if log:
        logg.write(f"fn = {fn}", currentframe(), "SMDOWNLOAD FILENAME")
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
        if log:
            logg.write(f"ar = {ar}", currentframe(), "SMDOWNLOAD AR")
        if os.system('aria2c -h%s'%(getnul()))==0 and ar :
            ab=True
            if JSONParser.getset(se,'ab')==False :
                ab=False
            if 'ab' in ip:
                if ip['ab']:
                    ab=True
                else :
                    ab=False
            if log:
                logg.write(f"ab = {ab}", currentframe(), "SMDOWNLOAD AB")
            if ab:
                read = dwaria2(r2, fn, geturll(i), fz, c, ip, se)
            else :
                read = dwaria2(r2, fn, i['video_playurl'], fz, c, ip, se)
            if read==-3 :
                print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                return -4
        else :
            if log:
                logg.write(f"GET {i['video_playurl']}", currentframe(), "SMDOWNLOAD GET STREAM")
            re=r2.get(i['video_playurl'],stream=True)
            if log:
                logg.write(f"status = {re.status_code}", currentframe(), "SMDOWNLOAD DOWNLOAD URL STATUS")
            read = downloadstream(nte, ip, i['video_playurl'], r2, re, fn, fz, c)
        if log:
            logg.write(f"read = {read}", currentframe(), "SMDOWNLOAD DOWNLOAD RESULT")
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
            if log:
                logg.write(f"rc = {rc}", currentframe(), "SMDOWNLOAD RC")
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
        tt = int(time.time())
        nss=""
        if not ns:
            nss=getnul()
        if vf == "mkv":
            with open(f"Temp/{i['id']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                te.write(';FFMETADATA1\n')
                te.write(f"title={bstr.g(i['name'])} - {bstr.g(sn)}\n")
                te.write(f"description={bstr.g(i['description'])}\n")
                te.write(f"id={i['id']}\n")
                te.write(f"pubtime={i['upload_time']}\n")
                te.write(f"artist={bstr.g(i['name'])}\n")
                te.write(f"author={bstr.g(i['name'])}\n")
                te.write(f"uid={i['uid']}\n")
                te.write(f"vq={i['width']}x{i['height']}\n")
                te.write(f"tags={bstr.g(bstr.gettags(i['tags']))}\n")
                te.write(f"purl=https://vc.bilibili.com/video/{i['id']}\n")
            if log:
                with open(f"Temp/{i['id']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                    logg.write(f"METADATAFILE 'Temp/{i['id']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "SMDOWNLOAD METADATAFILE")
            ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{i['id']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mkv\"{nss}"
        elif vf == "mp4":
            with open(f"Temp/{i['id']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                te.write(';FFMETADATA1\n')
                te.write(f"title={bstr.g(i['name'])} - {bstr.g(sn)}\n")
                te.write(f"comment={bstr.g(i['description'])}\n")
                te.write(f"artist={bstr.g(i['name'])}\n")
                te.write(f"episode_id={i['id']}\n")
                te.write(f"date={i['upload_time'][:10]}\n")
                te.write(f"description=UID{i['uid']},{i['width']}x{i['height']},{bstr.g(bstr.gettags(i['tags']))}\\\n")
                te.write(f"https://vc.bilibili.com/video/{i['id']}\n")
            if log:
                with open(f"Temp/{i['id']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                    logg.write(f"METADATAFILE 'Temp/{i['id']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "SMDOWNLOAD METADATAFILE")
            ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{i['id']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mp4\"{nss}"
        if log:
            logg.write(f"ml = {ml}", currentframe(), "SMDOWNLOAD FFMPEG COMMAND LINE")
        re=os.system(ml)
        if log:
            logg.write(f"re = {re}", currentframe(), "SMDOWNLOAD FFMPEG RESULT")
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
        os.remove(f"Temp/{i['id']}_{tt}_metadata.txt")
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
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
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
        if log:
            logg.write(format_exc(), currentframe(), "LIVE RECORD VIDEO MKDIR FAILED")
        print(lan['ERROR1'].replace('<dirname>',o))#创建文件夹"<dirname>"失败。
        return -5
    fin=True
    if JSONParser.getset(se,'in')==False :
        fin=False
    if 'in' in ip:
        fin=ip['in']
    vf = 'mkv'
    if 'vf' in se:
        vf = se['vf']
    if 'vf' in ip:
        vf = ip['vf']
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    if log:
        logg.write(f"ns = {ns}\nnte = {nte}\no = '{o}'\nF = {F}\nfin = {fin}\nvf = '{vf}'", currentframe(), "LIVE RECORD VIDEO PARA")
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    if nte:
        r2.trust_env=False
    r2.proxies=r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if read!=0 :
        print(lan['ERROR2'])#读取cookies.json出现错误
        return -1
    r2.headers.update({'referer':'https://live.bilibili.com/record/%s'%(data['rid'])})
    r2.cookies.set('CURRENT_QUALITY','125',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','80',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    if log:
        logg.write(f"GET https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?rid={data['rid']}&platform=html5", currentframe(), "GET LIVE RECORD VIDEO URL")
    re=r2.get('https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?rid=%s&platform=html5'%(data['rid']))
    if log:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE RECORD VIDEO URL RETURN")
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
        ma = True
        if JSONParser.getset(se,"ma") == False:
            ma = False
        if 'ma' in ip:
            ma=ip['ma']
        if log:
            logg.write(f"sv = {sv}\nfilen = '{filen}'\nff = {ff}\nma = {ma}", currentframe(), "LIVE RECORD VIDEO PARA 2")
        if ff and (len(durl)>1 or ma) and os.path.exists(f'{filen}.{vf}') and os.system('ffmpeg -h%s'%(getnul()))==0 :
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
                inp = input(f"{lan['INPUT1'].replace('<filename>', '%s.%s'%(filen, vf))}(y/n)")
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        fg=True
                        bs=False
                    elif inp[0].lower()=='n' :
                        bs=False
            if fg:
                try :
                    os.remove(f'{filen}.{vf}')
                except :
                    if log:
                        logg.write(format_exc(), currentframe(), "LIVE RECORD VIDEO REMOVE FILE FAILED")
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
                if log:
                    logg.write(f"fn = '{fn}'", currentframe(), "LIVE RECORD VIDEO TEMP FILE NAME")
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
                    if log:
                        logg.write(f"ar = {ar}", currentframe(), "LIVE RECORD VIDEO AR")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "LIVE RECORD VIDEO AB")
                        if ab :
                            read = dwaria2(r2, fn, geturll(k), k['size'], c3, ip, se)
                        else :
                            read = dwaria2(r2, fn, k['url'], k['size'], c3, ip, se)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read = downloadstream(nte, ip, k['url'], r2, re, fn, k['size'], c3)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "LIVE RRCORD VIDEO DOWNLOAD RETURN")
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
                if log:
                    logg.write(f"fn = '{fn}'", currentframe(), "LIVE RECORD VIDEO TEMP FILE NAME 2")
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
                    if log:
                        logg.write(f"ar = {ar}", currentframe(), "LIVE RECORD VIDEO AR")
                    if os.system('aria2c -h%s'%(getnul()))==0 and ar :
                        ab=True
                        if JSONParser.getset(se,'ab')==False :
                            ab=False
                        if 'ab' in ip:
                            if ip['ab']:
                                ab=True
                            else :
                                ab=False
                        if log:
                            logg.write(f"ab = {ab}", currentframe(), "LIVE RECORD VIDEO AB")
                        if ab:
                            read=dwaria2(r2,fn,geturll(k),k['size'],c3,ip,se,j,len(durl),True)
                        else :
                            read=dwaria2(r2,fn,k['url'],k['size'],c3,ip,se,j,len(durl),True)
                        if read==-3 :
                            print(f"{lan['ERROR4']}{lan['ERROR5']}")#aria2c 参数错误
                            return -4
                    else :
                        re=r2.get(k['url'],stream=True)
                        read = downloadstream(nte, ip, k['url'], r2, re, fn, k['size'], c3, j, len(durl), True, durz, com)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "LIVE RRCORD VIDEO DOWNLOAD RETURN 2")
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
            if oll:
                oll.add(fn)
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
            if len(durl) > 1 and vf == "mkv":
                te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['rid'])),tt),'wt',encoding='utf8')
                j=1
                for k in durl :
                    te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                    j=j+1
                te.close()
                with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"rid={data['rid']}\n")
                    te.write(f"room_id={data['roomid']}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"title={bstr.g(data['title'])}\n")
                    te.write(f"area_id={data['areaid']}\n")
                    te.write(f"parent_area_id={data['pareaid']}\n")
                    te.write(f"starttime={tostr2(data['st'])}\n")
                    te.write(f"endtime={tostr2(data['et'])}\n")
                    te.write(f"description={bstr.g(data['des'])}\n")
                    te.write(f"area_name={bstr.g(data['arean'])}\n")
                    te.write(f"parent_area_name={bstr.g(data['parean'])}\n")
                    te.write(f"tags={bstr.g(data['tags'])}\n")
                    te.write(f"hot_words={bstr.g(bstr.gettags(data['hotwords']))}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"sex={bstr.g(data['sex'])}\n")
                    te.write(f"sign={bstr.g(data['sign'])}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"purl=https://live.bilibili.com/record/{data['rid']}\n")
                if log:
                    with open(f"Temp/{data['rid']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"FFMPEG CONCAT FILE 'Temp/{data['rid']}_{tt}.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO FFMPEG CONCAT")
                    with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['rid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO METADATAFILE")
                ml = f"ffmpeg -f concat -safe 0 -i \"Temp/{data['rid']}_{tt}.txt\" -i \"Temp/{data['rid']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mkv\"{nss}"
            elif vf == "mkv":
                with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"rid={data['rid']}\n")
                    te.write(f"room_id={data['roomid']}\n")
                    te.write(f"uid={data['uid']}\n")
                    te.write(f"title={bstr.g(data['title'])}\n")
                    te.write(f"area_id={data['areaid']}\n")
                    te.write(f"parent_area_id={data['pareaid']}\n")
                    te.write(f"starttime={tostr2(data['st'])}\n")
                    te.write(f"endtime={tostr2(data['et'])}\n")
                    te.write(f"description={bstr.g(data['des'])}\n")
                    te.write(f"area_name={bstr.g(data['arean'])}\n")
                    te.write(f"parent_area_name={bstr.g(data['parean'])}\n")
                    te.write(f"tags={bstr.g(data['tags'])}\n")
                    te.write(f"hot_words={bstr.g(bstr.gettags(data['hotwords']))}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"author={bstr.g(data['name'])}\n")
                    te.write(f"sex={bstr.g(data['sex'])}\n")
                    te.write(f"sign={bstr.g(data['sign'])}\n")
                    te.write(f"vq={bstr.g(vqs)}\n")
                    te.write(f"purl=https://live.bilibili.com/record/{data['rid']}\n")
                if log:
                    with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['rid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO METADATAFILE")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{data['rid']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mkv\"{nss}"
            elif len(durl) > 1:
                te = open('Temp/%s_%s.txt' % (file.filtern('%s' % (data['rid'])), tt), 'wt', encoding='utf8')
                j = 1
                for k in durl:
                    te.write("file '../%s_%s.%s'\n" % (filen, j, hzm))
                    j = j + 1
                te.close()
                with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(data['title'])}\n")
                    te.write(f"comment={bstr.g(data['des'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"episode_id=rid{data['rid']}\n")
                    te.write(f"date={tostr2(data['st'])[:10]}\n")
                    te.write(f"description=UID{data['uid']},ROOMID{data['roomid']},{bstr.g(vqs)}\\\n")
                    te.write(f"https://live.bilibili.com/record/{data['rid']}\n")
                if log:
                    with open(f"Temp/{data['rid']}_{tt}.txt", 'r', encoding='utf8') as te:
                        logg.write(f"FFMPEG CONCAT FILE 'Temp/{data['rid']}_{tt}.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO FFMPEG CONCAT")
                    with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['rid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO METADATAFILE")
                ml = f"ffmpeg -f concat -safe 0 -i \"Temp/{data['rid']}_{tt}.txt\" -i \"Temp/{data['rid']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mp4\"{nss}"
            else:
                with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                    te.write(';FFMETADATA1\n')
                    te.write(f"title={bstr.g(data['title'])}\n")
                    te.write(f"comment={bstr.g(data['des'])}\n")
                    te.write(f"artist={bstr.g(data['name'])}\n")
                    te.write(f"episode_id=rid{data['rid']}\n")
                    te.write(f"date={tostr2(data['st'])[:10]}\n")
                    te.write(f"description=UID{data['uid']},ROOMID{data['roomid']},{bstr.g(vqs)}\\\n")
                    te.write(f"https://live.bilibili.com/record/{data['rid']}\n")
                if log:
                    with open(f"Temp/{data['rid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                        logg.write(f"METADATAFILE 'Temp/{data['rid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "LIVE RECORD VIDEO METADATAFILE")
                ml = f"ffmpeg -i \"{filen}.{hzm}\" -i \"Temp/{data['rid']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}.mp4\"{nss}"
            if log:
                logg.write(f"ml = {ml}", currentframe(), "LIVE RECORD VIDEO FFMPEG COMMAND LINE")
            re=os.system(ml)
            if log:
                logg.write(f"re = {re}", currentframe(), "LIVE RECORD VIDEO FFMPEG RETURN")
            if re==0:
                print(lan['OUTPUT14'])#合并完成！
            de=False
            if re==0:
                if oll:
                    oll.add(f"{filen}.{vf}")
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
            os.remove(f"Temp/{data['rid']}_{tt}_metadata.txt")
            if len(durl)>1:
                os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(data['rid'])),tt))
    return 0


def livevideodownload(data: dict, data2: dict, r: requests.session, c: bool, se: dict, ip: dict):
    """下载直播视频
    -2 API Error
    -4 aria2c 参数错误
    -5 文件夹创建失败
    -6 缺少必要参数
    -7 参数错误"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
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
        if log:
            logg.write(format_exc(), currentframe(), "LIVE VIDEO MKDIR FAILED")
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
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nF = {F}\nnte = {nte}\nfin = {fin}\nsv = {sv}", currentframe(), "LIVE VIDEO PARA 2")
    if 'play_url' in data2 and data2['play_url'] is not None:
        play_url = data2['play_url']
    else:
        uri = f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={data['roomid']}&qn=10000&platform=web&https_url_req=1&ptype=16"
        if log:
            logg.write(f"GET {uri}", currentframe(), "GET LIVE VIDEO PLAYURL")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE VIDEO PLAYURL RESULT")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            return -2
        play_url = re['data']
    if log:
        logg.write(f"play_url = {play_url}", currentframe(), "LIVE VIDEO PLAYURL")
    quality_description = play_url['quality_description']
    accept_quality_list = []
    quality_des_dict = {}
    for i in quality_description:
        accept_quality_list.append(i['qn'])
        quality_des_dict[i['qn']] = getqualitytrans(i['desc'])
    current_qn = play_url['current_qn']
    if log:
        logg.write(f"quality_description = {quality_description}\naccept_quality_list = {accept_quality_list}\nquality_des_dict = {quality_des_dict}\ncurrent_qn = {current_qn}", currentframe(), "LIVE VIDEO PLAYVAR")
    if 'durl' in play_url:
        durl = {}
        durl[current_qn] = play_url['durl']
        if not c or F:
            for quality in accept_quality_list:
                if quality not in durl:
                    uri = f"https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={data['roomid']}&qn={quality}&platform=web&https_url_req=1&ptype=16"
                    if log:
                        logg.write(f"GET {uri}", currentframe(), "GET LIVE VIDEO PLAYURL2")
                    re = r.get(uri)
                    re.encoding = 'utf8'
                    if log:
                        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE VIDEO PLAYURL2 RESULT")
                    re = re.json()
                    if re['code'] != 0:
                        print(f"{re['code']} {re['message']}")
                        return -2
                    play_url = re['data']
                    current_qn = play_url['current_qn']
                    if log:
                        logg.write(f"play_url = {play_url}\ncurrent_qn = {current_qn}", currentframe(), "LIVE VIDEO PLAYVAR2")
                    if quality == current_qn:
                        if 'durl' in play_url:
                            durl[quality] = play_url['durl']
                    else:
                        accept_quality_list.remove(quality)
                        if log:
                            logg.write(f"Remove quality {quality}.", currentframe(), "LIVE VIDEO PLAYURL NOT FOUND")
                        print(lan['NOT_GET_QUA'].replace('<quality>', str(quality)))  # 无法获取画质为<quality>的播放地址。
            if log:
                logg.write(f"accept_quality_list = {accept_quality_list}\ndurl = {durl}", currentframe(), "LIVE VIDEO PLAYVAR3")
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
                if log:
                    logg.write(f"GET {uri}", currentframe(), "GET LIVE VIDEO PLAYURL3")
                re = r.get(uri)
                re.encoding = 'utf8'
                if log:
                    logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE VIDEO PLAYURL3 RESULT")
                re = re.json()
                if re['code'] != 0:
                    print(f"{re['code']} {re['message']}")
                    return -2
                play_url = re['data']
                if play_url['current_qn'] == quality and 'durl' in play_url:
                    durl[quality] = play_url['durl']
            durl = durl[quality]
            if log:
                logg.write(f"durl = {durl}", currentframe(), "LIVE VIDEO PLAYVAR4")
            if ns:
                print(f"{lan['OUTPUT9']}{quality},{quality_des_dict[quality]}{lan['ALL_URL_COUNT'].replace('<number>', str(len(durl)))}")
            video_quality = quality
        if log:
            logg.write(f"video_quality = {video_quality}", currentframe(), "LIVE VIDEO PLAYVAR5")
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
        if log:
            logg.write(f"link_index = {link_index}\nlink = {link}\nurl = {url}", currentframe(), "LIVE VIDEO PLAYVAR6")
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
            fn = file.filtern(f"{data['title']}({tostr2(now)}).flv")
        elif sv:
            fn = file.filtern(f"{data['title']}({data['roomid']},UID{data['uid']},{tostr2(now)},{quality_des_dict[video_quality]}).flv")
        else:
            fn = file.filtern(f"{data['title']}({data['roomid']},UID{data['uid']},{tostr2(now)}).flv")
        filen = f"{o}{fn}"
        if log:
            logg.write(f"ffmpeg = {ffmpeg}\naria2c = {aria2c}\nfilen = {filen}", currentframe(), "LIVE VIDEO PLAYVAR7")
        if ffmpeg:
            lrh = True  # 是否进行去HTML化
            if JSONParser.getset(se, 'lrh') == False:
                lrh = False
            if 'lrh' in ip:
                lrh = ip['lrh']
            if lrh:
                data['des'] = bstr.rhtml(data['des'])
            tt = int(time.time())
            with open(f"Temp/{data['roomid']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
                te.write(';FFMETADATA1\n')
                te.write(f"roomid={data['roomid']}\n")
                te.write(f"livetime={data['livetime']}\n")
                te.write(f"description={bstr.g(data['des'])}\n")
                te.write(f"title={bstr.g(data['title'])}\n")
                te.write(f"uid={data['uid']}\n")
                te.write(f"artist={bstr.g(data['name'])}\n")
                te.write(f"author={bstr.g(data['name'])}\n")
                te.write(f"authorsex={bstr.g(data['sex'])}\n")
                te.write(f"sign={bstr.g(data['sign'])}\n")
                te.write(f"areaid={data['areaid']}\n")
                te.write(f"areaname={bstr.g(data['areaname'])}\n")
                te.write(f"pareaid={data['pareaid']}\n")
                te.write(f"pareaname={bstr.g(data['pareaname'])}\n")
                te.write(f"tags={bstr.g(data['tags'])}\n")
                te.write(f"hotwords={bstr.g(bstr.gettags(data['hotwords']))}\n")
                te.write(f"purl={bstr.g(r.headers['referer'])}\n")
            if log:
                with open(f"Temp/{data['roomid']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                    logg.write(f"METADATAFILE 'Temp/{data['roomid']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "LIVE VIDEO FFMPEG METADATA")
            nss = ""
            if not ns:
                nss = getnul()
            cm = f"ffmpeg -user_agent \"{r.headers['User-Agent']}\" -referer \"{r.headers['referer']}\" -i \"{url}\" -i \"Temp/{data['roomid']}_{tt}_metadata.txt\" -map_metadata 1 -c copy \"{filen}\"{nss}"
            if log:
                logg.write(f"cm = {cm}", currentframe(), "LIVE VIDEO FFMPEG COMMAND LINE")
            read = os.system(cm)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE VIDEO FFMPEG RETURN")
            if read == 0:
                oll.add(filen)
            os.remove(f"Temp/{data['roomid']}_{tt}_metadata.txt")
        elif aria2c:
            read = dwaria2(r, filen, url, -1, False, ip, se)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE VIDEO ARIA2C RETURN")
            if read == 0:
                oll.add(filen)
            elif read == -3:
                print(f"{lan['ERROR4']}{lan['ERROR5']}")  # aria2c 参数错误
                return -4
        else:
            re = r.get(url, stream=True)
            read = downloadstream(nte, ip, url, r, re, filen, -1, False)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE VIDEO NORMAL RETURN")
            if read == 0:
                oll.add(filen)
    return 0


def audownload(data: dict, r: requests.Session, se: dict, ip: dict, m: bool, a: bool):
    """AU号音频下载
    m 是否自动选择最高画质
    a 是否自动继续下载
    -1 文件夹创建失败
    -2 读取cookies.json发生错误
    -3 API调用错误
    -4 命令行输入错误
    -5 aria2c命令行错误
    -6 下载错误"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
    ns = True
    if 's' in ip:
        ns = False
    nte = False
    if JSONParser.getset(se, 'te') == False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    bp = False  # 删除无用文件时是否保留封面图片
    if JSONParser.getset(se, 'bp') == True:
        bp = True
    if 'bp' in ip:
        bp = ip['bp']
    o = 'Download/'
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    F = False  # 仅输出视频信息
    if 'F' in ip:
        F = True
    aria2c = True
    if JSONParser.getset(se, 'a') == False:
        aria2c = False
    if 'ar' in ip:
        aria2c = ip['ar']
    ma = True
    if JSONParser.getset(se, 'ma') == False:
        ma = False
    if 'ma' in ip:
        ma = ip['ma']
    ffmpeg = True
    if JSONParser.getset(se, 'nf') == True:
        ffmpeg = False
    if 'yf' in ip:
        ffmpeg = ip['yf']
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    sv = True
    if JSONParser.getset(se, 'sv') == False:
        sv = False
    if 'sv' in ip:
        sv = ip['sv']
    ab = True  # 是否使用备用地址
    if JSONParser.getset(se, 'ab') == False:
        ab = False
    if 'ab' in ip:
        ab = ip['ab']
    if log:
        logg.write(f"ns = {ns}\nnte = {nte}\nbp = {bp}\no = '{o}'\nF = {F}\naria2c = {aria2c}\nma = {ma}\nffmpeg = {ffmpeg}\nfin = {fin}\nsv = {sv}\nab = {ab}", currentframe(), "Normal Video Download Para")
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Normal Audio MKDIR FAILED")
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建文件夹"<dirname>"失败。
        return -1
    if not os.path.exists('Temp/'):
        mkdir('Temp/')
    r2 = requests.Session()
    r2.headers = copydict(r.headers)
    r2.headers.update({'referer': f"https://www.bilibili.com/audio/au{data['id']}"})
    if nte:
        r2.trust_env = False
    r2.proxies = r.proxies
    read = JSONParser.loadcookie(r2, logg)
    if log:
        logg.write(f"read = {read}", currentframe(), "Normal Audio Download Var1")
    if read != 0:
        print(lan['ERROR2'])  # 读取cookies.json出现错误
        return -2
    uri = f"https://www.bilibili.com/audio/music-service-c/web/url?sid={data['id']}&privilege=2&quality=2"
    if log:
        logg.write(f"GET {uri}", currentframe(), "Normal Audio Get Playurl")
    re = r2.get(uri)
    re.encoding = 'utf8'
    if log:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Normal Audio Get Playurl Result")
    re = re.json()
    if re['code'] != 0:
        print(f"{re['code']} {re['msg']}")
        return -3
    re = re['data']
    if 'qualities' in re and re['qualities'] is not None:
        input(f"{lan['AUDOMULQ']}\n{lan['ERROR5']}\n{lan['INPUT6']}")  # 不支持多个音质
    accept_qualities = [2]
    dash = {}
    dash[2] = {'id': 2, 'base_url': re['cdns'][0], 'r': r2}
    dash[2]['backup_url'] = re['cdns'][1:] if len(re['cdns']) > 1 else None
    if data['aid'] != 0:
        if ns:
            print(lan['USEFROMV'])  # 发现关联的视频
        url = f"https://www.bilibili.com/video/av{data['aid']}"
        r3 = requests.Session()
        r3.headers = r.headers
        r3.headers.update({'referer': url})
        if nte:
            r3.trust_env = False
        r3.proxies = r3.proxies
        read = JSONParser.loadcookie(r3, logg)
        if log:
            logg.write(f"read = {read}", currentframe(), "Normal Audio Download Var2")
        if read != 0:
            print(lan['ERROR2'])  # 读取cookies.json出现错误
            return -2
        r3.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r3.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r3.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r3.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn=125&otype=json&bvid={data['bvid']}&fnver=0&fnval=80"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Normal Audio Video Get Playurl")
        re = r3.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Normal Audio Video Get Playurl Result")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            return -3
        if 'data' in re and 'dash' in re['data'] and 'audio' in re['data']['dash'] and re['data']['dash']['audio'] is not None:
            accept_audio_quality = []
            for j in re['data']['dash']['audio']:
                j['r'] = r3
                dash[j['id']] = j
                accept_audio_quality.append(j['id'])
            accept_audio_quality.sort(reverse=True)
            accept_qualities = accept_qualities + accept_audio_quality
            timel = re['data']['timelength']
    for quality in accept_qualities:
        dash[quality]['size'] = streamgetlength(dash[quality]['r'], dash[quality]['base_url'], logg)
    if m and not F:
        mi = accept_qualities[0]
        ms = dash[mi]['size']
        for quality in accept_qualities:
            if dash[quality]['size'] > ms:
                ms = dash[quality]['size']
                mi = quality
        dash = dash[mi]
        timelength = data['duration'] * 1000 if mi < 30000 else timel
        if ns:
            print(lan['OUTPUT16'])  # 音频轨
            print(f"ID:{dash['id']}")
            print(f"{lan['OUTPUT10']}{file.info.size(dash['size'])}({dash['size']}B,{file.cml(dash['size'], timelength)})")
        vqs = mi
    else:
        if ns or (not ns and F):
            print(lan['OUTPUT16'])  # 音频轨
        k = 0
        for quality in accept_qualities:
            timelength = data['duration'] * 1000 if quality < 30000 else timel
            if ns or (not ns and F):
                print(f"{k + 1}.ID:{quality}")
                print(f"{lan['OUTPUT10']}{file.info.size(dash[quality]['size'])}({dash[quality]['size']}B,{file.cml(dash[quality]['size'], timelength)})")
            k = k + 1
        if F:
            return 0
        if len(accept_qualities) > 1:
            bs = True
            fi = True
            while bs:
                if fi and 'a' in ip:
                    fi = False
                    inp = ip['a']
                elif ns:
                    inp = input(lan['INPUT5'])  # 请选择音质
                else:
                    print(lan['ERROR6'])  # 请使用-a <id>选择音质
                    return -4
                if len(inp) > 0 and inp.isnumeric():
                    if int(inp) > 0 and int(inp) < len(accept_qualities) + 1:
                        bs = False
                        vqs = accept_qualities[int(inp) - 1]
                        dash = dash[vqs]
                        if ns:
                            print(lan['OUTPUT17'].replace('<audioquality>', str(vqs)))  # 已选择%s音质
        else:
            vqs = accept_qualities[0]
            dash = dash[vqs]
    avi = "" if data['aid'] == 0 else f",AV{data['aid']},{data['bvid']},{data['cid']}"
    if not fin:
        filen = f"{o}{file.filtern(data['title'])}"
    elif sv:
        filen = f"""{o}{file.filtern(f"{data['title']}(AU{data['id']}{avi},{vqs})")}"""
    else:
        filen = f"""{o}{file.filtern(f"{data['title']}(AU{data['id']}{avi})")}"""
    hzm = file.geturlfe(dash['base_url'])
    if hzm == "m4a" and ma:
        hzm = "temp.m4a"
    if log:
        logg.write(f"dash = {dash}\nvqs = {vqs}\nfilen = {filen}\nhzm = {hzm}", currentframe(), "Normal Audio Download Var3")
    if ffmpeg and (ma or hzm != "m4a" ) and os.path.exists(f"{filen}.m4a"):
        overwrite = False
        bs = True
        if not ns:
            overwrite = True
            bs = False
        if 'y' in se:
            overwrite = se['y']
            bs = False
        if 'y' in ip:
            overwrite = ip['y']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT1'].replace('<filename>', filen + '.m4a')}(y/n)")  # "%s"文件已存在，是否覆盖？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    overwrite = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if overwrite:
            try:
                os.remove(f"{filen}.m4a")
            except:
                if log:
                    logg.write(format_exc(), currentframe(), "Normal Audio Download Remove File Error")
                print(lan['OUTPUT7'])  # 删除原有文件失败，跳过下载
                return 0
        else:
            return 0
    bs2 = True
    aria2c = True
    while bs2:
        bs2 = False
        if aria2c:
            if ab:
                read = dwaria2(dash['r'], f"{filen}.{hzm}", geturll(dash), dash['size'], a, ip, se)
            else:
                read = dwaria2(dash['r'], f"{filen}.{hzm}", dash['base_url'], dash['size'], a, ip, se)
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Audio Download Aria2c Return")
            if read == -3:
                print(lan['ERROR4'])  # aria2c 参数错误
                return -5
        else:
            re = dash['r'].get(dash['base_url'], stream=True)
            read = downloadstream(nte, ip, dash['base_url'], dash['r'], re, f"{filen}.{hzm}", dash['size'], a)
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Audio Download Return")
        if read == -1:
            return -2
        elif read == -2:
            bs = True
            rc = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'rd')
            if read == True:
                bs = False
                rc = True
            elif read == False:
                bs = False
            if 'r' in ip:
                rc = ip['r']
                bs = False
            while bs:
                inp = input(f"{lan['INPUT3']}(y/n)")  # 文件下载失败，是否重新下载？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        bs = False
                        rc = True
                    elif inp[0].lower() == 'n':
                        bs = False
            if rc:
                if os.path.exists(f"{filen}.{hzm}"):
                    os.remove(f"{filen}.{hzm}")
                bs2 = True
            else:
                return -6
    if oll:
        oll.add(f"{filen}.{hzm}")
    imgf = filen + "." + file.geturlfe(data['cover'])
    if log:
        logg.write(f"imgf = {imgf}", currentframe(), "Normal Audio Download Var4")
    imgs = aupicdownload(data, dash['r'], se, ip, imgf)
    if log:
        logg.write(f"imgs = {imgs}", currentframe(), "Normal Audio Download Var5")
    if ffmpeg and (ma or hzm != "m4a"):
        if hzm == "m4s":
            print(lan['CONV_M4S_TO_M4A'])
        else:
            print(lan['ADDMETA'])
        tt = int(time.time())
        nss = ""
        imga = ""
        imga2 = ""
        if not ns:
            nss = getnul()
        if imgs == 0:
            imga = f" -i \"{imgf}\""
            imga2 = " -map 0 -map 2 -disposition:v:0 attached_pic"
        with open(f"Temp/AU{data['id']}_{tt}_metadata.txt", 'w', encoding='utf8', newline='\n') as te:
            te.write(';FFMETADATA\n')
            te.write(f"title={bstr.g(data['title'])}\n")
            te.write(f"comment={bstr.g(data['intro'])}\n")
            te.write(f"artist={bstr.g(data['author'])}\n")
            te.write(f"episode_id=AU{data['id']}\n")
            te.write(f"date={tostr4(data['passtime'])}\n")
            te.write(f"description={bstr.g(vqs)},{data['uid']},{data['uname']}\\\n")
            te.write(f"{bstr.g(bstr.gettags(data['tags']))}\\\n")
            te.write(f"""{bstr.g(f"https://www.bilibili.com/audio/au{data['id']}")}\n""")
        if log:
            with open(f"Temp/AU{data['id']}_{tt}_metadata.txt", 'r', encoding='utf8') as te:
                logg.write(f"METADTAFILE 'Temp/AU{data['id']}_{tt}_metadata.txt'\n{te.read()}", currentframe(), "Normal Audio Download Metadata")
        cm = f"""ffmpeg -i "{filen}.{hzm}" -i "Temp/AU{data['id']}_{tt}_metadata.txt"{imga} -map_metadata 1 -c copy{imga2} "{filen}.m4a"{nss}"""
        if log:
            logg.write(f"cm = {cm}", currentframe(), "Normal Audio Download Ffmpeg Commandline")
        re = os.system(cm)
        if log:
            logg.write(f"re = {re}", currentframe(), "Normal Audio Download Ffmpeg Return")
        if re == 0:
            if oll:
                oll.add(f"{filen}.m4a")
            if hzm == "m4s":
                print(lan['COM_CONV'])
            else:
                print(lan['ADDMECOM'])
            delete = False
            bs = True
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'ad')
            if read == True:
                delete = True
                bs = False
            elif read == False:
                bs = False
            if 'ad' in ip:
                delete = ip['ad']
                bs = False
            while bs:
                inp = input(f"{lan['INPUT4']}(y/n)")  # 是否删除中间文件？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        delete = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if delete:
                os.remove(f"{filen}.{hzm}")
                if imgs == 0 and not bp:
                    os.remove(imgf)
        os.remove(f"Temp/AU{data['id']}_{tt}_metadata.txt")
    read = aulrcdownload(data, r, se, ip, filen)
    if log:
        logg.write(f"read = {read}", currentframe(), "Normal Audio Download Lrc Down Return")
    return 0


def aupicdownload(data: dict, r: requests.Session, se: dict, ip: dict, fn: str = None) -> int:
    """下载AU号封面
    fn 指定文件名
    -1 文件夹创建失败
    -2 封面文件下载失败
    -3 覆盖文件失败"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if 'oll' in ip:
        oll = ip['oll']
    ns = True
    if 's' in ip:
        ns = False
    o = "Download/"
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nfin = {fin}", currentframe(), "Normal Audio Download Pic Para")
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Normal Audio Download Pic Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建文件夹"<dirname>"失败。
        return -1
    if fn is None:
        avi = "" if data['aid'] == 0 else f",AV{data['aid']},{data['bvid']},{data['cid']}"
        if fin:
            te = file.filtern(f"{data['title']}(AU{data['id']}{avi}).{file.geturlfe(data['cover'])}")
        else:
            te = file.filtern(f"{data['title']}.{file.geturlfe(data['cover'])}")
        fn = f"{o}{te}"
    if log:
        logg.write(f"fn = {fn}", currentframe(), "Normal Audio Download Pic Var")
    if os.path.exists(fn):
        overwrite = False
        bs = True
        if not ns:
            overwrite = True
            bs = False
        if 'y' in se:
            overwrite = se['y']
            bs = False
        if 'y' in ip:
            overwrite = ip['y']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT1'].replace('<filename>', fn)}(y/n)")  # "%s"文件已存在，是否覆盖？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    overwrite = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if overwrite:
            try:
                os.remove(fn)
            except:
                if log:
                    logg.write(format_exc(), currentframe(), "Normal Aideo Download Pic Remove File Failed")
                print(lan['OUTPUT7'])  # 删除原有文件失败，跳过下载
                return -3
    if log:
        logg.write(f"GET {data['cover']}", currentframe(), "Normal Audio Download Pic Request")
    re = r.get(data['cover'])
    if log:
        logg.write(f"status = {re.status_code}", currentframe(), "Normal Audio Download Pic Request Result")
    if re.status_code == 200:
        with open(fn, 'wb') as f:
            f.write(re.content)
        if oll:
            oll.add(fn)
        if ns:
            print(lan['OUTPUT23'].replace('<filename>', fn))  # 封面图片下载完成。
        return 0
    else:
        print(f"{lan['OUTPUT24']}HTTP {re.status_code}")  # 下载封面图片时发生错误：
        return -2


def aulrcdownload(data: dict, r: requests.Session, se: dict, ip: dict, fn: str=None):
    """下载AU号歌词
    fn 指定文件名
    -1 新建文件夹失败
    -2 歌词下载失败
    -3 删除文件失败
    -4 读取cookies.json错误"""
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    oll = None
    if oll:
        oll = ip['oll']
    ns = True
    if 's' in ip:
        ns = False
    o = 'Download/'
    read = JSONParser.getset(se, 'o')
    if read is not None:
        o = read
    if 'o' in ip:
        o = ip['o']
    fin = True
    if JSONParser.getset(se, 'in') == False:
        fin = False
    if 'in' in ip:
        fin = ip['in']
    nte = True
    if JSONParser.getset(se, 'te') == False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    auf = True  # 是否标准化LRC
    if JSONParser.getset(se, 'auf') == False:
        auf = False
    if 'auf' in ip:
        auf = ip['auf']
    if log:
        logg.write(f"ns = {ns}\no = '{o}'\nfin = {fin}\nnte = {nte}\nauf = {auf}", currentframe(), "Normal Audio Download Lrc Para")
    try:
        if not os.path.exists(o):
            mkdir(o)
    except:
        if log:
            logg.write(format_exc(), currentframe(), "Normal Audio Download Pic Mkdir Failed")
        print(lan['ERROR1'].replace('<dirname>', o))  # 创建文件夹"<dirname>"失败。
        return -1
    if fn is None:
        avi = "" if data['aid'] == 0 else f",AV{data['aid']},{data['bvid']},{data['cid']}"
        if fin:
            te = file.filtern(f"{data['title']}(AU{data['id']}{avi})")
        else:
            te = file.filtern(f"{data['title']}")
        fn = f"{o}{te}"
    if log:
        logg.write(f"fn = {fn}", currentframe(), "Normal Audio Download Lrc Var")
    if 'lyric' in data and data['lyric'] != "":
        tfn = f"{fn}.{file.geturlfe(data['lyric'])}"
        if os.path.exists(tfn):
            overwrite = False
            bs = True
            if not ns:
                overwrite = True
                bs = False
            if 'y' in se:
                overwrite = se['y']
                bs = False
            if 'y' in ip:
                overwrite = ip['y']
                bs = False
            while bs:
                inp = input(f"{lan['INPUT1'].replace('<filename>', tfn)}(y/n)")  # "%s"文件已存在，是否覆盖？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        overwrite = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if overwrite:
                try:
                    os.remove(tfn)
                except:
                    if log:
                        logg.write(format_exc(), currentframe(), "Normal Aideo Download Lrc Remove File Failed")
                    print(lan['OUTPUT7'])  # 删除原有文件失败，跳过下载
                    return -3
        if log:
            logg.write(f"GET {data['lyric']}", currentframe(), "Normal Audio Download Lrc Request")
        re = r.get(data['lyric'])
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Normal Audio Download Lrc Request Result")
        if re.status_code == 200:
            with open(tfn, 'w', encoding='utf8') as f:
                if auf:
                    res, read = filterLRC(re.text)
                    if read > 0:
                        print(lan['FILLRC'].replace('<count>', str(read)))
                    f.write(res)
                else:
                    f.write(re.text)
            if oll:
                oll.add(tfn)
            if ns:
                print(lan['LRCCOM'].replace('<filename>', tfn))  # 歌词下载完成
        else:
            print(f"{lan['LRCERR']}HTTP {re.status_code}")
            return -2
    if data['aid'] != 0:
        if ns:
            print(lan['USEFROMV2'])  # 发现关联的视频
        url = f"https://www.bilibili.com/video/av{data['aid']}"
        r2 = requests.Session()
        r2.headers.update({'referer': url})
        if nte:
            r2.trust_env = False
        r2.proxies = r.proxies
        read = JSONParser.loadcookie(r2, logg)
        if log:
            logg.write(f"read = {read}", currentframe(), "Normal Audio Download Lrc Var2")
        if read != 0:
            print(lan['ERROR2'])  # 读取cookies.json出现错误
            return -4
        uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={r2.cookies.get('buvid3')}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Normal Audio Download Lrc Get Player.so")
        rr = r2.get(uri)
        rr.encoding = 'utf8'
        if log:
            logg.write(f"status = {rr.status_code}\n{rr.text}", currentframe(), "Normal Audio Download Lrc Get Player.so Result")
        rs = search(r'<subtitle>(.+)</subtitle>', rr.text)
        if rs is not None:
            rs = json.loads(rs.groups()[0])
            if log:
                logg.write(f"rs = {rs}", currentframe(), "Normal Audio Download Lrc Player.so Regex")
            JSONParser2.getsub(rs, data)
            if 'sub' in data:
                for s in data['sub']:
                    downlrc(r2, fn + ".m4a", s, ip, se, data, ns, isau=True)
    return 0


def downloadstream(nte, ip, uri, r, re, fn, size, d2, i=1, n=1, d=False, durz=-1, pre=-1):
    logg = None
    if 'logg' in ip:
        logg = ip['logg']
    if d :
        print(lan['OUTPUT1'].replace('<i>',str(i)).replace('<count>',str(n)))#正在开始下载第<i>个文件，共<count>个文件
    else :
        print(lan['OUTPUT2'])#正在开始下载
    if os.path.exists(fn) :
        fsize=file.getinfo({'a':fn,'f':''})['s']
        if logg is not None:
            logg.write(f"fsize = {fsize}\nsize = {size}", currentframe(), "DOWNLOADSTREAM FILESIZE")
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
            if logg is not None:
                logg.write(f"Update HTTP Header: Range: bytes={fsize}-{size-1}", currentframe(), "DOWNLOADSTREAM UPDATE HTTP HEADER")
            read = JSONParser.loadcookie(r2, logg)
            if logg is not None:
                logg.write(f"read = {read}", currentframe(), "Downloadstream Load Cookies Return")
            if read!=0 :
                print(lan['ERROR2'])#读取cookies.json出现错误
                return -1
            if logg is not None:
                logg.write(f"GET {uri}", currentframe(), "DOWNLOADSTREAM REGET STREAM")
            re=r2.get(uri,stream=True)
            if logg is not None:
                logg.write(f"status = {re.status_code}", currentframe(), "DOWNLOADSTREAM REGET STATUS")
            s=fsize
        if not d2 and ('y' in ip or 's' in ip):
            if 's' in ip:
                fg=True
                bs=False
            if 'y' in se:
                fg = se['y']
                bs = False
            if 'y' in ip:
                fg = ip['y']
                bs = False
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
                if logg is not None:
                    logg.write(format_exc(), currentframe(), "DOWNLOADSTREAM REMOVE FILE FAILED")
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
        if logg is not None:
            logg.write(f"s = {s}\nsize = {size}", currentframe(), "DOWNLOADSTREAM LENGTH CHANGED")
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
            return '%s/%s' % (f, file.filtern(f"{i['title']}{i['i']+1}.{i['longTitle']}({i['titleFormat']},AV{i['aid']},{i['bvid']},ID{i['id']},{i['cid']},{vqs[i2]}).{hzm[i2]}"))
        else :
            return f"{f}/{file.filtern(i['title'])}{i['i']+1}.{file.filtern(i['longTitle'])}({file.filtern(vqs[i2])}).{hzm[i2]}"
def streamgetlength(r:requests.Session, uri, logg = None):
    bs=True
    while bs:
        bs=False
        try :
            if logg is not None:
                logg.write(f"GETLENGTH {uri}", currentframe(), "STREAMGETLENGTH")
            re=r.get(uri,stream=True)
            try :
                if re.headers.get('Content-Length')!=None :
                    a=int(re.headers.get('Content-Length'))
                else :
                    a=-1#无法获取长度，什么神必服务器
                re.close()
                if logg is not None:
                    logg.write(f"headers = {re.headers}\nsize = {a}", currentframe(), "STREAMLENGTH")
                return a
            except :
                if logg is not None:
                    logg.write(format_exc(), currentframe(), "RETRY GET STREAM LENGTH")
                re.close()
                print(lan['OUTPUT21'])#获取文件大小失败。尝试重新获取……
                bs=True
        except :
            if logg is not None:
                logg.write(format_exc(), currentframe(), "RETRY GET STREAM LENGTH 2")
            print(lan['OUTPUT21'])#获取文件大小失败。尝试重新获取……
            bs=True
if __name__=="__main__" :
    print(lan['OUTPUT22'])#请使用start.py
