import requests
import JSONParser
import json
import file
import time
import os
#https://api.bilibili.com/x/player/playurl?cid=<cid>&qn=<图质大小>&otype=json&avid=<avid>&fnver=0&fnval=16 番剧也可，但不支持4K
#https://api.bilibili.com/pgc/player/web/playurl?avid=<avid>&cid=<cid>&bvid=&qn=<图质大小>&type=&otype=json&ep_id=<epid>&fourk=1&fnver=0&fnval=16 貌似仅番剧
#result -> dash -> video/audio -> [0-?](list) -> baseUrl/base_url
#第二个需要带referer，可以解析4K
def avvideodownload(i,url,data,r,c,c2) :
    """下载av号视频
    -1 cookies.json读取错误
    -2 API Error"""
    if not os.path.exists('Download/') :
        os.mkdir('Download/')
    r2=requests.Session()
    r2.headers=r.headers
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
                print("大小：%s(%sB)"%(file.info.size(size),size))
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
            print('大小：%s(%sB)'%(file.info.size(durz),durz))
            durl=durl[vq]
        if data['videos']==1 :
            filen='Download/%s'%(file.filtern('%s(AV%s,P%s,%s,%s)'%(data['title'],data['aid'],i,data['page'][i-1]['cid'],vqs)))
        else :
            filen='Download/%s'%(file.filtern('%s-%s(AV%s,P%s,%s,%s)'%(data['title'],data['page'][i-1]['part'],data['aid'],i,data['page'][i-1]['cid'],vqs)))
        print('共有%s个文件'%(len(durl)))
        j=1
        hzm=file.geturlfe(durl[0]['url'])
        for k in durl :
            if len(durl)==1 :
                fn='%s.%s' % (filen,hzm)
                re=r2.get(k['url'],stream=True)
                downloadstream(re,fn,k['size'])
            else :
                fn='%s_%s.%s' %(filen,j,hzm)
                re=r2.get(k['url'],stream=True)
                downloadstream(re,fn,k['size'],j,len(durl),True)
            j=j+1
        if len(durl)>1 and os.system('ffmpeg -h 2>&0 1>&0')==0 :
            print('将用ffmpeg自动合成')
            tt=int(time.time())
            if os.path.exists('%s.mp4'%(filen)) :
                bs=True
                while bs:
                    inp=input('"%s.mp4"文件已存在，是否覆盖？(y/n)'%(filen))
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            os.remove('%s.mp4'%(filen))
                            bs=False
                        elif inp[0].lower()=='n' :
                            return 0
            te=open('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt),'wt')
            j=1
            for k in durl :
                te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                j=j+1
            te.close()
            ml='ffmpeg -f concat -i "Temp/%s_%s.txt" -c copy "%s.mp4"' %(file.filtern('%s'%(data['aid'])),tt,filen)
            re=os.system(ml)
            if re==0:
                print('合并完成！')
            de=False
            if re==0 and not c2 :
                bs=True
                while bs :
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and (de or c2) :
                j=1
                for k in durl:
                    os.remove("%s_%s.%s"%(filen,j,hzm))
                    j=j+1
            os.remove('Temp/%s_%s.txt'%(file.filtern('%s'%(data['aid'])),tt))
    elif "data" in re and "dash" in re['data'] :
        vq=re["data"]["quality"]
        vqd=re["data"]["accept_description"]
        avq=re["data"]["accept_quality"]
        aaq=[]
        dash={'video':{},'audio':{}}
        vqs=[]
        for j in re['data']['dash']['video']:
            dash['video'][j['id']]=j
        for j in re['data']['dash']['audio']:
            dash['audio'][j['id']]=j
            aaq.append(j['id'])
        if c:
            dash['video']=dash['video'][avq[0]]
            dash['audio']=dash['audio'][aaq[0]]
            print('视频轨：')
            print("图质：%s(%sx%s)"%(vqd[0],dash['video']['width'],dash['video']['height']))
            dash['video']['size']=streamgetlength(r,dash['video']['base_url'])
            print('大小：%s(%sB)'%(file.info.size(dash['video']['size']),dash['video']['size']))
            print('音频轨：')
            print('ID：%s'%(dash['audio']['id']))
            dash['audio']['size']=streamgetlength(r,dash['audio']['base_url'])
            print('大小：%s(%sB)'%(file.info.size(dash['audio']['size']),dash['audio']['size']))
            vqs=[vqd[0],aaq[0]]
        else :
            print('视频轨：')
            k=0
            for j in avq:
                print('%s.图质：%s(%sx%s)'%(k+1,vqd[k],dash['video'][j]['width'],dash['video'][j]['height']))
                dash['video'][j]['size']=streamgetlength(r,dash['video'][j]['base_url'])
                print('大小：%s(%sB)'%(file.info.size(dash['video'][j]['size']),dash['video'][j]['size']))
                k=k+1
            if len(avq)>1 :
                bs=True
                while bs:
                    inp=input('请选择画质：')
                    if len(inp)>0 and inp.isnumeric() :
                        if int(inp)>0 and int(inp)<len(avq)+1 :
                            bs=False
                            dash['video']=dash['video'][avq[int(inp)-1]]
                            print('已选择%s画质'%(vqd[int(inp)-1]))
                            vqs.append(vqd[int(inp)-1])
            else :
                dash['video']=dash['video'][avq[0]]
                vqs.append(vqd[0])
            print('音频轨：')
            k=0
            for j in aaq:
                print("%s.ID：%s"%(k+1,j))
                dash['audio'][j]['size']=streamgetlength(r,dash['audio'][j]['base_url'])
                print('大小：%s(%sB)'%(file.info.size(dash['audio'][j]['size']),dash['audio'][j]['size']))
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
            filen='Download/%s'%(file.filtern('%s(AV%s,P%s,%s,%s,%s).mp4'%(data['title'],data['aid'],i,data['page'][i-1]['cid'],vqs[0],vqs[1])))
        else :
            filen='Download/%s'%(file.filtern('%s-%s(AV%s,P%s,%s,%s,%s).mp4'%(data['title'],data['page'][i-1]['part'],data['aid'],i,data['page'][i-1]['cid'],vqs[0],vqs[1])))
        hzm=[file.geturlfe(dash['video']['base_url']),file.geturlfe(dash['audio']['base_url'])]
        re=r2.get(dash['video']['base_url'],stream=True)
        downloadstream(re,getfn(0,data,vqs,hzm),dash['video']['size'],1,2,True)
        re=r2.get(dash['audio']['base_url'],stream=True)
        downloadstream(re,getfn(1,data,vqs,hzm),dash['audio']['size'],2,2,True)
        if os.system('ffmpeg -h 2>&0 1>&0')==0 :
            print('将用ffmpeg自动合成')
            if os.path.exists(filen) :
                bs=True
                while bs:
                    inp=input('"%s"文件已存在，是否覆盖？(y/n)'%(filen))
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            os.remove('%s'%(filen))
                            bs=False
                        elif inp[0].lower()=='n' :
                            return 0
            re=os.system('ffmpeg -i "%s" -i "%s" -c copy "%s"'%(getfn(0,data,vqs,hzm),getfn(1,data,vqs,hzm),filen))
            de=False
            if re==0 :
                print('合并完成！')
            if re==0 and not c2 :
                bs=True
                while bs :
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            de=True
                        elif inp[0].lower()=='n' :
                            bs=False
            if re==0 and (de or c2) :
                for i in[0,1]:
                    os.remove(getfn(i,data,vqs,hzm))
def epvideodownload(i,url,data,r,c,c2):
    """下载番剧等视频"""
    if not os.path.exists('Download/') :
        os.mkdir('Download/')
    fdir='Download/%s'%(file.filtern('%s(SS%s)'%(data['mediaInfo']['title'],data['mediaInfo']['ssId'])))
    if not os.path.exists(fdir):
        os.mkdir(fdir)
    r2=requests.Session()
    r2.headers=r.headers
    read=JSONParser.loadcookie(r2)
    if read!=0 :
        print("读取cookies.json出现错误")
        return -1
    r2.headers.update({'referer':url})
    uri="https://api.bilibili.com/pgc/player/web/playurl?avid=%s&cid=%s&bvid=&qn=120&type=&otype=json&ep_id=%s&fourk=1&fnver=0&fnval=32"%(i['aid'],i['cid'],i['id'])
    re=r2.get(uri)
    re.encoding='utf8'
    re=re.json()
    print(re)
    if re["code"]!=0 :
        print({"code":re["code"],"message":re["message"]})
        return -2
    if 'result' in re and 'dash' in re['result']:
        vq=re["result"]["quality"]
        vqd=re["result"]["accept_description"]
        avq=re["result"]["accept_quality"]
        for j in re['result']['dash']['video']:
            print(j['id'])
def downloadstream(re,fn,size,i=1,n=1,d=False) :
    if d :
        print('正在开始下载第%s个文件，共%s个文件'%(i,n))
    else :
        print('正在开始下载')
    if os.path.exists(fn) :
        fsize=file.getinfo(fn)['s']
        if fsize!=size :
            s="(文件大小不一致，建议覆盖)"
        else :
            s=""
        bs=True
        while bs :
            inp=input('"%s"文件已存在，是否覆盖？%s(y/n)'%(fn,s))
            if len(inp)>0 :
                if inp[0].lower()=='y':
                    os.remove(fn)
                    bs=False
                elif inp[0].lower()=='n' :
                    re.close()
                    return 0
    t1=time.time()
    t2=time.time()
    s=0
    with open(fn,'wb') as f :
        for c in re.iter_content(chunk_size=1024) :
            if c :
                s=s+f.write(c)
                t1=time.time()
                if t1-t2>1 :
                    if d :
                        print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    else :
                        print('\r %s(%sB)/%s(%sB)\t%.2f%%'%(file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    t2=t1
    print()
    f.close()
    return 0
def getfn(i,data,vqs,hzm):
    if data['videos']==1 :
        return 'Download/%s'%(file.filtern('%s(AV%s,P%s,%s,%s).%s'%(data['title'],data['aid'],i,data['page'][i-1]['cid'],vqs[i],hzm[i])))
    else :
        return 'Download/%s'%(file.filtern('%s-%s(AV%s,P%s,%s,%s).%s'%(data['title'],data['page'][i-1]['part'],data['aid'],i,data['page'][i-1]['cid'],vqs[i],hzm[i])))
def streamgetlength(r:requests.Session,uri):
    re=r.get(uri,stream=True)
    a=int(re.headers.get('Content-Length'))
    re.close()
    return a
if __name__=="__main__" :
    print("请使用start.py")
