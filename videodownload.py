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
    print(re)
    if re["code"]!=0 :
        print({"code":re["code"],"message":re["message"]})
        return -2
    if "data" in re:
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
            te=open('Temp/%s.txt'%(file.filtern('%s'%(data['aid']))),'wt')
            j=1
            for k in durl :
                te.write("file '../%s_%s.%s'\n"%(filen,j,hzm))
                j=j+1
            te.close()
            ml='ffmpeg -f concat -i "Temp/%s.txt" -c copy "%s.mp4"' %(file.filtern('%s'%(data['aid'])),filen)
            re=os.system(ml)
            if re==0 :
                bs=True
                while bs :
                    inp=input('是否删除中间文件？(y/n)')
                    if len(inp)>0 :
                        if inp[0].lower()=='y' :
                            bs=False
                            j=1
                            for k in durl :
                                os.remove('%s_%s.%s'%(filen,j,hzm))
                                j=j+1
                        elif inp[0].lower()=='n' :
                            bs=False
            os.remove('Temp/%s.txt'%(file.filtern('%s'%(data['aid']))))
def downloadstream(re,fn,size,i=1,n=1,d=False) :
    if d :
        print('正在开始下载第%s个文件，共%s个文件'%(i,n))
    else :
        print('正在开始下载')
    if os.path.exists(fn) :
        bs=True
        while bs :
            inp=input('"%s"文件已存在，是否覆盖？(y/n)'%(fn))
            if len(inp)>0 :
                if inp[0].lower()=='y':
                    os.remove(fn)
                    bs=False
                elif inp[0].lower()=='n' :
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
                        print('\r (%s/%s)%s(%sB)/%s(%sB)\t%.2f%%'%(i,n,file.info.size(s),s,file.info.size(size),size,s/size*100),end='',flush=True)
                    t2=t1
    print()
    f.close()
    return 0
if __name__=="__main__" :
    print("请使用start.py")
