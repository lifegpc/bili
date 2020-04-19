import requests
import JSONParser
import biliLogin
import HTMLParser
import json
import file
from os import path
import os
def epdownload(ep,fn="") :
    s=requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36","Connection": "keep-alive","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Language": "zh-CN,zh;q=0.8","referer":"https://www.bilibili.com/bangumi/play/ep%s"%(ep)})
    read=JSONParser.loadcookie(s)
    login=0
    if read==0 :
        read=biliLogin.tryok(s)
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
        read=biliLogin.login(s)
        if read==0 :
            login=1
        elif read==1 :
            exit()
        else :
            exit()
    re=s.get("https://www.bilibili.com/bangumi/play/ep%s"%(ep))
    re.encoding='utf8'
    p2=HTMLParser.Myparser2()
    p2.feed(re.text)
    p=HTMLParser.Myparser()
    p.feed(re.text)
    d=JSONParser.Myparser2(p.videodata)
    d2=json.loads(p2.videodata)
    k=0
    ok=False
    if 'epList' in d :
        for i in d['epList'] :
            k=k+1
            if i['loaded'] :
                v=i
                ok=True
                break
    if 'sections' in d and not ok :
        for i in d['sections'] :
            b=False
            for j in i['epList'] :
                k=k+1
                if j['loaded'] :
                    v=j
                    b=True
                    break
            if b:
                break
    if fn=='' :
        if not path.exists('Download') :
            os.mkdir('Download')
        dirname="Download/%s(SS%s)"%(file.filtern(d['mediaInfo']['title']),d['mediaInfo']['ssId'])
        if not path.exists(dirname) :
            os.mkdir(dirname)
        fn='%s/%s.%s' %(dirname,k,file.filtern('%s(%s,AV%s,ID%s,%s).flv' % (v['longTitle'],v['titleFormat'],v['aid'],v['id'],v['cid'])))
    urlt=False
    for i in d2['data']['durl'] :
        if 'url' in i :
            url=i['url']
            urlt=True
            break
    if urlt :
        re=s.get(url,stream=True)
        with open(fn,'wb') as f:
            for c in re.iter_content(chunk_size=1024) :
                if c:
                    f.write(c)
        f.close()
