import requests
import JSONParser
import json
import file
import time
import os
from dictcopy import copydict,copylist
from re import search
from goto import with_goto
#https://api.bilibili.com/x/player/playurl?cid=<cid>&qn=<图质大小>&otype=json&avid=<avid>&fnver=0&fnval=16 番剧也可，但不支持4K
#https://api.bilibili.com/pgc/player/web/playurl?avid=<avid>&cid=<cid>&bvid=&qn=<图质大小>&type=&otype=json&ep_id=<epid>&fourk=1&fnver=0&fnval=16&session= 貌似仅番剧
#result -> dash -> video/audio -> [0-?](list) -> baseUrl/base_url
# session = md5(String((getCookie('buvid3') || Math.floor(Math.random() * 100000).toString(16)) + Date.now()));
#第二个需要带referer，可以解析4K
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
@with_goto
def avvideodownload(i,url,data,r,c,c3,se,ip) :
    """下载av号视频
    -1 cookies.json读取错误
    -2 API Error
    -3 下载错误"""
    if not os.path.exists('Download/') :
        os.mkdir('Download/')
    r2=requests.Session()
    r2.headers=copydict(r.headers)
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print("读取cookies.json出现错误")
        return -1
    r2.headers.update({'referer':url})
    uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=120&otype=json&avid=%s&fnver=0&fnval=16"%(data["page"][i-1]["cid"],data["aid"])
    re=r2.get(uri)
    re.encoding="utf8"
    re=re.json()
    if re["code"]!=0 :
        print({"code":re["code"],"message":re["message"]})
        return -2
    if "data" in re and "durl" in re['data']:
        vq=re["data"]["quality"]
        vqd=re["data"]["accept_description"]
        avq=re["data"]["accept_quality"]
        durl={vq:re["data"]['durl']}
        durz={}
        vqs=""
        if not c :
            j=0
            for l in avq :
                if not l in durl :
                    uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=%s&otype=json&avid=%s&fnver=0&fnval=16" % (data["page"][i-1]["cid"],l,data["aid"])
                    re=r2.get(uri)
                    re.encoding='utf8'
                    re=re.json()
                    if re["code"]!=0 :
                        print({"code":re["code"],"message":re["message"]})
                        return -2
                    durl[re["data"]['quality']]=re['data']['durl']
                print('%s.图质：%s'%(j+1,vqd[j]))
                j=j+1
                size=0
                for k in durl[l] :
                    size=size+k['size']
                durz[l]=size
                print("大小：%s(%sB,%s)"%(file.info.size(size),size,file.cml(size,re['data']['timelength'])))
            bs=True
            while bs :
                inp=input('请选择画质：')
                if len(inp) > 0 and inp.isnumeric() and int(inp)>0 and int(inp)<len(avq)+1 :
                    durl=durl[avq[int(inp)-1]]
                    durz=durz[avq[int(inp)-1]]
                    vq=avq[int(inp)-1]
                    bs=False
                print('已选择%s画质'%(vqd[int(inp)-1]))
                vqs=vqd[int(inp)-1]
        else :
            j=0
            for l in avq :
                if l==vq :
                    print('图质：%s'%(vqd[j]))
                    vqs=vqd[j]
                    break
                j=j+1
            durz=0
            for k in durl[vq] :
                durz=durz+k['size']
            print('大小：%s(%sBm,%s)'%(file.info.size(durz),durz,file.cml(durz,re['data']['timelength'])))
            durl=durl[vq]
        if data['videos']==1 :
            filen='Download/%s'%(file.filtern('%s(AV%s,%s,P%s,%s,%s)'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'],vqs)))
        else :
            filen='Download/%s'%(file.filtern('%s-%s(AV%s,%s,P%s,%s,%s)'%(data['title'],data['page'][i-1]['part'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'],vqs)))
        print('共有%s个文件'%(len(durl)))
        j=1
        hzm=file.geturlfe(durl[0]['url'])
        com=0
        for k in durl :
            if len(durl)==1 :
                fn='%s.%s' % (filen,hzm)
                label .a # pylint: disable=undefined-variable
                re=r2.get(k['url'],stream=True)
                read=downloadstream(ip,k['url'],r2,re,fn,k['size'],c3)
                if read==-1 :
                    return -1
                elif read==-2 :
                    bs=True
                    rc=False
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
                        inp=input('文件下载失败，是否重新下载？(y/n)')
                        if len(inp)>0 :
                            if inp[0].lower()=='y' :
                                bs=False
                                rc=True
                            elif inp[0].lower()=='n' :
                                bs=False
                    if rc :
                        os.remove(fn)
                        goto .a # pylint: disable=undefined-variable
                    else :
                        return -3
            else :
                fn='%s_%s.%s' %(filen,j,hzm)
                label .b # pylint: disable=undefined-variable
                re=r2.get(k['url'],stream=True)
                read=downloadstream(ip,k['url'],r2,re,fn,k['size'],c3,j,len(durl),True,durz,com)
                if read==-1 :
                    return -1
                elif read==-2 :
                    bs=True
                    rc=False
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
                        inp=input('文件下载失败，是否重新下载？(y/n)')
                        if len(inp)>0 :
                            if inp[0].lower()=='y' :
                                bs=False
                                rc=True
                            elif inp[0].lower()=='n' :
                                bs=False
                    if rc :
                        os.remove(fn)
                        goto .b # pylint: disable=undefined-variable
                    else :
                        return -3
                com=com+k['size']
            j=j+1
        if len(durl)>1 and os.system('ffmpeg -h 2>&0 1>&0')==0 :
            print('将用ffmpeg自动合成')
            tt=int(time.time())
            if os.path.exists('%s.mp4'%(filen)) :
                fg=False
                bs=True
                if 'y' in ip :
                    if ip['y'] :
                        fg=True
                        bs=False
                    else :
                        bs=False
                while bs:
                    inp=input('"%s.mp4"文件已存在，是否覆盖？(y/n)'%(filen))
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            fg=True
                            bs=False
                        elif inp[0].lower()=='n' :
                            bs=False
                if fg:
                    try :
                        os.remove('%s.mp4'%(filen))
                    except :
                        print('删除原有文件失败，跳过下载')
                        return 0
                else:
                    return 0
            te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt),'wt',encoding='utf8')
            j=1
            for k in durl :
                te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                j=j+1
            te.close()
            ml='ffmpeg -f concat -safe 0 -i "Temp/%s_%s.txt" -c copy "%s.mp4"' %(file.filtern('%s'%(data['aid'])),tt,filen)
            re=os.system(ml)
            if re==0:
                print('合并完成！')
            de=False
            if re==0:
                bs=True
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
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                j=1
                for k in durl:
                    os.remove("%s_%s.%s"%(filen,j,hzm))
                    j=j+1
            os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt))
    elif "data" in re and "dash" in re['data'] :
        vq=re["data"]["quality"]
        vqd=re["data"]["accept_description"]
        avq2=re['data']["accept_quality"]
        avq=[]
        aaq=[]
        dash={'video':{},'audio':{}}
        vqs=[]
        for j in re['data']['dash']['video'] :
            dash['video'][str(j['id'])+j['codecs']]=j
            avq.append(str(j['id'])+j['codecs'])
        for j in re['data']['dash']['audio']:
            dash['audio'][j['id']]=j
            aaq.append(j['id'])
        aaq.sort(reverse=True)
        if c:
            dash['video']=dash['video'][avq[0]]
            dash['audio']=dash['audio'][aaq[0]]
            print('视频轨：')
            print("图质：%s(%sx%s)"%(vqd[0],dash['video']['width'],dash['video']['height']))
            dash['video']['size']=streamgetlength(r2,dash['video']['base_url'])
            print('大小：%s(%sB,%s)'%(file.info.size(dash['video']['size']),dash['video']['size'],file.cml(dash['video']['size'],re['data']['timelength'])))
            print('音频轨：')
            print('ID：%s'%(dash['audio']['id']))
            dash['audio']['size']=streamgetlength(r2,dash['audio']['base_url'])
            print('大小：%s(%sB,%s)'%(file.info.size(dash['audio']['size']),dash['audio']['size'],file.cml(dash['audio']['size'],re['data']['timelength'])))
            vqs=[vqd[0]+","+dash['video']['codecs'],aaq[0]]
        else :
            print('视频轨：')
            k=0
            for j in avq:
                print('%s.图质：%s(%sx%s,%s)'%(k+1,vqd[sea(j,avq2)],dash['video'][j]['width'],dash['video'][j]['height'],sev(j)))
                dash['video'][j]['size']=streamgetlength(r2,dash['video'][j]['base_url'])
                print('大小：%s(%sB,%s)'%(file.info.size(dash['video'][j]['size']),dash['video'][j]['size'],file.cml(dash['video'][j]['size'],re['data']['timelength'])))
                k=k+1
            if len(avq)>1 :
                bs=True
                while bs:
                    inp=input('请选择画质：')
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(avq)+1 :
                            bs=False
                            dash['video']=dash['video'][avq[int(inp)-1]]
                            print('已选择%s(%s)画质'%(vqd[sea(avq[int(inp)-1],avq2)],sev(avq[int(inp)-1])))
                            vqs.append(vqd[sea(avq[int(inp)-1],avq2)]+","+sev(avq[int(inp)-1]))
            else :
                dash['video']=dash['video'][avq[0]]
                vqs.append(vqd[0]+","+sev(avq[0]))
            print('音频轨：')
            k=0
            for j in aaq:
                print("%s.ID：%s"%(k+1,j))
                dash['audio'][j]['size']=streamgetlength(r2,dash['audio'][j]['base_url'])
                print('大小：%s(%sB,%s)'%(file.info.size(dash['audio'][j]['size']),dash['audio'][j]['size'],file.cml(dash['audio'][j]['size'],re['data']['timelength'])))
                k=k+1
            if len(aaq)>1:
                bs=True
                while bs:
                    inp=input('请选择音质：')
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(aaq)+1 :
                            bs=False
                            dash['audio']=dash['audio'][aaq[int(inp)-1]]
                            print('已选择%s音质'%(aaq[int(inp)-1]))
                            vqs.append(aaq[int(inp)-1])
            else :
                dash['audio']=dash['audio'][aaq[0]]
                vqs.append(aaq[0])
        if data['videos']==1 :
            filen='Download/%s'%(file.filtern('%s(AV%s,%s,P%s,%s,%s,%s).mp4'%(data['title'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'],vqs[0],vqs[1])))
        else :
            filen='Download/%s'%(file.filtern('%s-%s(AV%s,%s,P%s,%s,%s,%s).mp4'%(data['title'],data['page'][i-1]['part'],data['aid'],data['bvid'],i,data['page'][i-1]['cid'],vqs[0],vqs[1])))
        hzm=[file.geturlfe(dash['video']['base_url']),file.geturlfe(dash['audio']['base_url'])]
        durz=dash['video']['size']+dash['audio']['size']
        label .c # pylint: disable=undefined-variable
        re=r2.get(dash['video']['base_url'],stream=True)
        read=downloadstream(ip,dash['video']['base_url'],r2,re,getfn(0,i,data,vqs,hzm),dash['video']['size'],c3,1,2,True,durz,0)
        if read==-1 :
            return -1
        elif read==-2 :
            bs=True
            rc=False
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
                inp=input('文件下载失败，是否重新下载？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        rc=True
                    elif inp[0].lower()=='n' :
                        bs=False
            if rc :
                os.remove(getfn(0,i,data,vqs,hzm))
                goto .c # pylint: disable=undefined-variable
            else :
                return -3
        label .d # pylint: disable=undefined-variable
        re=r2.get(dash['audio']['base_url'],stream=True)
        read=downloadstream(ip,dash['audio']['base_url'],r2,re,getfn(1,i,data,vqs,hzm),dash['audio']['size'],c3,2,2,True,durz,dash['video']['size'])
        if read==-1:
            return -1
        elif read==-2 :
            bs=True
            rc=False
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
                inp=input('文件下载失败，是否重新下载？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        rc=True
                    elif inp[0].lower()=='n' :
                        bs=False
            if rc :
                os.remove(getfn(1,i,data,vqs,hzm))
                goto .d # pylint: disable=undefined-variable
            else :
                return -3
        if os.system('ffmpeg -h 2>&0 1>&0')==0 :
            print('将用ffmpeg自动合成')
            if os.path.exists(filen) :
                fg=False
                bs=True
                if 'y' in ip :
                    if ip['y'] :
                        fg=True
                        bs=False
                    else :
                        bs=False
                while bs:
                    inp=input('"%s"文件已存在，是否覆盖？(y/n)'%(filen))
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
                        print('删除原有文件失败，跳过下载')
                        return 0
                else:
                    return 0
            re=os.system('ffmpeg -i "%s" -i "%s" -c copy "%s"'%(getfn(0,i,data,vqs,hzm),getfn(1,i,data,vqs,hzm),filen))
            de=False
            if re==0 :
                print('合并完成！')
            if re==0:
                bs=True
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
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                for j in[0,1]:
                    os.remove(getfn(j,i,data,vqs,hzm))
@with_goto
def epvideodownload(i,url,data,r,c,c3,se,ip):
    """下载番剧等视频"""
    if not os.path.exists('Download/') :
        os.mkdir('Download/')
    fdir='Download/%s'%(file.filtern('%s(SS%s)'%(data['mediaInfo']['title'],data['mediaInfo']['ssId'])))
    url2='https://bilibili.com/bangumi/play/ep'+str(i['id'])
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    r2=requests.Session()
    r2.headers=r.headers
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print("读取cookies.json出现错误")
        return -1
    r2.headers.update({'referer':url2})
    r2.cookies.set('CURRENT_QUALITY','116',domain='.bilibili.com',path='/')
    r2.cookies.set('CURRENT_FNVAL','16',domain='.bilibili.com',path='/')
    r2.cookies.set('laboratory','1-1',domain='.bilibili.com',path='/')
    r2.cookies.set('stardustvideo','1',domain='.bilibili.com',path='/')
    re=r2.get(url2)
    re.encoding='utf8'
    rs=search('__playinfo__=([^<]+)',re.text)
    if rs!=None :
        re=json.loads(rs.groups()[0])
    else :
        return -2
    if 'data' in re and 'dash' in re['data']:
        dash={'video':{},'audio':{}}
        vqd=re["data"]["accept_description"]
        avq=[]
        avq2=re["data"]["accept_quality"]
        aaq=[]
        vqs=[]
        for j in re['data']['dash']['video']:
            t=str(j['id'])+j['codecs']
            dash['video'][t]=j
            avq.append(t)
        for j in re['data']['dash']['audio']:
            dash['audio'][j['id']]=j
            aaq.append(j['id'])
        aaq.sort(reverse=True)
        if c:
            dash['video']=dash['video'][avq[0]]
            dash['audio']=dash['audio'][aaq[0]]
            print('视频轨：')
            print("图质：%s(%sx%s)"%(vqd[0],dash['video']['width'],dash['video']['height']))
            dash['video']['size']=streamgetlength(r2,dash['video']['base_url'])
            print('大小：%s(%sB,%s)'%(file.info.size(dash['video']['size']),dash['video']['size'],file.cml(dash['video']['size'],re['data']['timelength'])))
            print('音频轨：')
            print('ID：%s'%(dash['audio']['id']))
            dash['audio']['size']=streamgetlength(r2,dash['audio']['base_url'])
            print('大小：%s(%sB,%s)'%(file.info.size(dash['audio']['size']),dash['audio']['size'],file.cml(dash['audio']['size'],re['data']['timelength'])))
            vqs=[vqd[0]+","+dash['video']['codecs'],aaq[0]]
        else :
            print('视频轨：')
            k=0
            for j in avq:
                print('%s.图质：%s(%sx%s,%s)'%(k+1,vqd[sea(j,avq2)],dash['video'][j]['width'],dash['video'][j]['height'],sev(j)))
                dash['video'][j]['size']=streamgetlength(r2,dash['video'][j]['base_url'])
                print('大小：%s(%sB,%s)'%(file.info.size(dash['video'][j]['size']),dash['video'][j]['size'],file.cml(dash['video'][j]['size'],re['data']['timelength'])))
                k=k+1
            if len(avq)>1 :
                bs=True
                while bs:
                    inp=input('请选择画质：')
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(avq)+1 :
                            bs=False
                            dash['video']=dash['video'][avq[int(inp)-1]]
                            print('已选择%s(%s)画质'%(vqd[sea(avq[int(inp)-1],avq2)],sev(avq[int(inp)-1])))
                            vqs.append(vqd[sea(avq[int(inp)-1],avq2)]+","+sev(avq[int(inp)-1]))
            else :
                dash['video']=dash['video'][avq[0]]
                vqs.append(vqd[0]+","+sev(avq[0]))
            print('音频轨：')
            k=0
            for j in aaq:
                print("%s.ID：%s"%(k+1,j))
                dash['audio'][j]['size']=streamgetlength(r2,dash['audio'][j]['base_url'])
                print('大小：%s(%sB,%s)'%(file.info.size(dash['audio'][j]['size']),dash['audio'][j]['size'],file.cml(dash['audio'][j]['size'],re['data']['timelength'])))
                k=k+1
            if len(aaq)>1:
                bs=True
                while bs:
                    inp=input('请选择音质：')
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(aaq)+1 :
                            bs=False
                            dash['audio']=dash['audio'][aaq[int(inp)-1]]
                            print('已选择%s音质'%(aaq[int(inp)-1]))
                            vqs.append(aaq[int(inp)-1])
            else :
                dash['audio']=dash['audio'][aaq[0]]
                vqs.append(aaq[0])
        if i['s']=='e' :
            filen='%s/%s'%(fdir,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s,%s,%s).mp4'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[0],vqs[1])))
        else :
            filen='%s/%s'%(fdir,file.filtern('%s%s.%s(%s,AV%s,%s,ID%s,%s,%s,%s).mp4'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[0],vqs[1])))
        hzm=[file.geturlfe(dash['video']['base_url']),file.geturlfe(dash['audio']['base_url'])]
        durz=dash['video']['size']+dash['audio']['size']
        label .e # pylint: disable=undefined-variable
        re=r2.get(dash['video']['base_url'],stream=True)
        read=downloadstream(ip,dash['video']['base_url'],r2,re,getfn2(i,0,fdir,vqs,hzm),dash['video']['size'],c3,1,2,True,durz,0)
        if read==-1 :
            return -1
        elif read==-2 :
            bs=True
            rc=False
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
                inp=input('文件下载失败，是否重新下载？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        rc=True
                    elif inp[0].lower()=='n' :
                        bs=False
            if rc :
                os.remove(getfn2(i,0,fdir,vqs,hzm))
                goto .e # pylint: disable=undefined-variable
            else :
                return -3
        label .f # pylint: disable=undefined-variable
        re=r2.get(dash['audio']['base_url'],stream=True)
        read=downloadstream(ip,dash['audio']['base_url'],r2,re,getfn2(i,1,fdir,vqs,hzm),dash['audio']['size'],c3,2,2,True,durz,dash['video']['size'])
        if read==-1 :
            return -1
        elif read==-2 :
            bs=True
            rc=False
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
                inp=input('文件下载失败，是否重新下载？(y/n)')
                if len(inp)>0 :
                    if inp[0].lower()=='y' :
                        bs=False
                        rc=True
                    elif inp[0].lower()=='n' :
                        bs=False
            if rc :
                os.remove(getfn2(i,1,fdir,vqs,hzm))
                goto .f # pylint: disable=undefined-variable
            else :
                return -3
        if os.system('ffmpeg -h 2>&0 1>&0')==0 :
            print('将用ffmpeg自动合成')
            if os.path.exists(filen) :
                fg=False
                bs=True
                if 'y' in ip :
                    if ip['y'] :
                        fg=True
                        bs=False
                    else :
                        bs=False
                while bs:
                    inp=input('"%s"文件已存在，是否覆盖？(y/n)'%(filen))
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
                        print('删除原有文件失败，跳过下载')
                        return 0
                else:
                    return 0
            re=os.system('ffmpeg -i "%s" -i "%s" -c copy "%s"'%(getfn2(i,0,fdir,vqs,hzm),getfn2(i,1,fdir,vqs,hzm),filen))
            de=False
            if re==0 :
                print('合并完成！')
            if re==0:
                bs=True
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
                        de=True
                        bs=False
                while bs :
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and de:
                for j in[0,1]:
                    os.remove(getfn2(i,j,fdir,vqs,hzm))
def downloadstream(ip,uri,r,re,fn,size,d2,i=1,n=1,d=False,durz=-1,pre=-1) :
    s=0
    if d :
        print('正在开始下载第%s个文件，共%s个文件'%(i,n))
    else :
        print('正在开始下载')
    if os.path.exists(fn) :
        fsize=file.getinfo({'a':fn,'f':''})['s']
        if fsize!=size :
            s="(文件大小不一致，建议覆盖)"
        else :
            s=""
        bs=True
        fg=False
        if d2 and fsize==size :
            print('文件大小一致，跳过下载')
            return 0
        if d2 and fsize!=size :
            re.close()
            r2=requests.session()
            r2.headers=copydict(r.headers)
            r2.headers.update({'Range':'bytes=%s-%s'%(fsize,size-1)})
            read=JSONParser.loadcookie(r2)
            if read!=0 :
                print("读取cookies.json出现错误")
                return -1
            re=r2.get(uri,stream=True)
            s=fsize
        if not d2 and 'y' in ip :
            if ip['y'] :
                fg=True
                bs=False
            else :
                bs=False
        while bs and not d2 :
            inp=input('"%s"文件已存在，是否覆盖？%s(y/n)'%(fn,s))
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
                print('删除原有文件失败，跳过下载')
                re.close()
                return 0
        elif not d2 :
            re.close()
            return 0
    t1=time.time()
    t2=time.time()
    with open(fn,'ab') as f :
        for c in re.iter_content(chunk_size=1024) :
            if c :
                s=s+f.write(c)
                t1=time.time()
                if t1-t2>1 and durz==-1 :
                    if d :
                        print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    else :
                        print('\r %s(%sB)/%s(%sB)\t%.2f%%'%(file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    t2=t1
                elif t1-t2>1 and d:
                    print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%\t%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100,file.info.size(s+pre),s+pre,file.info.size(durz),durz,(s+pre)/durz*100),end='',flush=True)
                    t2=t1
    print()
    if s!= size :
        print('文件大小不匹配')
        return -2
    f.close()
    return 0
def getfn(i,i2,data,vqs,hzm):
    if data['videos']==1 :
        return 'Download/%s'%(file.filtern('%s(AV%s,%s,P%s,%s,%s).%s'%(data['title'],data['aid'],data['bvid'],i2,data['page'][i2-1]['cid'],vqs[i],hzm[i])))
    else :
        return 'Download/%s'%(file.filtern('%s-%s(AV%s,%s,P%s,%s,%s).%s'%(data['title'],data['page'][i2-1]['part'],data['aid'],data['bvid'],i2,data['page'][i2-1]['cid'],vqs[i],hzm[i])))
def getfn2(i,i2,f,vqs,hzm) :
    if i['s']=='e' :
        return '%s/%s'%(f,file.filtern('%s.%s(%s,AV%s,%s,ID%s,%s,%s).%s'%(i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[i2],hzm[i2])))
    else :
        return '%s/%s'%(f,file.filtern('%s.%s(%s%s,AV%s,%s,ID%s,%s,%s).%s'%(i['title'],i['i']+1,i['longTitle'],i['titleFormat'],i['aid'],i['bvid'],i['id'],i['cid'],vqs[i2],hzm[i2])))
def streamgetlength(r:requests.Session,uri):
    re=r.get(uri,stream=True)
    a=int(re.headers.get('Content-Length'))
    re.close()
    return a
if __name__=="__main__" :
    print("请使用start.py")
