import requests
import JSONParser
import biliLogin
import HTMLParser
import json
import file
#https://api.bilibili.com/x/player/playurl?cid=<cid>&qn=<图质大小>&otype=json&avid=<avid>&fnver=0&fnval=16 番剧也可，但不支持4K
#https://api.bilibili.com/pgc/player/web/playurl?avid=<avid>&cid=<cid>&bvid=&qn=<图质大小>&type=&otype=json&ep_id=<epid>&fourk=1&fnver=0&fnval=16 貌似仅番剧
#result -> dash -> video/audio -> [0-?](list) -> baseUrl/base_url
#第二个需要带referer，可以解析4K
def videodownload(url,data,r,t) :
    if t=='ss' or t=='ep' :
        pass
if __name__=="__main__" :
    r=requests.Session()
    r.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36","Connection": "keep-alive","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Language": "zh-CN,zh;q=0.8"})
    read=JSONParser.loadcookie(r)
    login=0
    if read==0 :
        read=biliLogin.tryok(r)
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
        lrogin=2
    else :
        print("文件读取错误！")
        login=2
    if login==2 :
        read=biliLogin.login(r)
        if read==0 :
            login=1
        elif read==1 :
            exit()
        else :
            exit()
    