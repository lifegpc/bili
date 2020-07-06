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
from selenium import webdriver
import requests
import JSONParser
import time
import traceback
import hashlib
import rsa
from getpass import getpass
from urllib import parse
import base64
def login(r,ud:dict,ip:dict):
    '登录至B站'
    try :
        driver=webdriver.Chrome()
        driver.get('https://passport.bilibili.com/ajax/miniLogin/minilogin')
        aa=True
        while aa :
            time.sleep(1)
            if driver.current_url=='https://passport.bilibili.com/ajax/miniLogin/redirect' :
                aa=False
        sa=[]
        for i in driver.get_cookies() :
            r.cookies.set(i['name'],i['value'],domain=i['domain'],path=i['path'])
            t={'name':i['name'],'value':i['value'],'domain':i['domain'],'path':i['path']}
            sa.append(t)
        driver.close()
    except Exception:
        print(traceback.format_exc())
        print('使用ChromeDriver登录发生错误，尝试采用用户名、密码登录')
        read=login2(r)
        if read==-1 :
            print('登录失败！')
            return 2
        sa=read
    rr=tryok(r,ud)
    if rr==True :
        if not 's' in ip:
            print('登录成功')
        JSONParser.savecookie(sa)
        return 0
    elif rr==False :
        print('网络错误')
        return 1
    else :
        print("登录失败："+str(rr['code'])+","+str(rr['message']))
        return 2
def tryok(r,ud:dict) :
    '验证是否登录成功'
    try :
        re=r.get('https://api.bilibili.com/x/web-interface/nav')
    except :
        return False
    re.encoding='utf8'
    try :
        obj=re.json()
        if obj['code']==0 and 'data' in obj and obj['data']['isLogin']:
            ud['d']=obj['data']
            return True
        return obj
    except :
        return re.text
def login2(r:requests.Session):
    "使用用户名密码登录"
    username=input('请输入用户名：')
    password=getpass('请输入密码：')
    appkey="bca7e84c2d947ac6"
    def getk():
        re=r.post('https://passport.bilibili.com/api/oauth2/getKey',{'appkey':appkey,'sign':cal_sign("appkey=%s"%(appkey))})
        re=re.json()
        if re['code']!=0 :
            return -1,-1
        return re['data']['hash'],rsa.PublicKey.load_pkcs1_openssl_pem(re['data']['key'].encode())
    keyhash,pubkey=getk()
    if keyhash==-1:
        return -1
    pm=f"appkey={appkey}&password={parse.quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(), pubkey)))}&username={parse.quote_plus(username)}"
    pm2=f"{pm}&sign={cal_sign(pm)}"
    re=r.post('https://passport.bilibili.com/api/v2/oauth2/login',pm2,headers={'Content-type': "application/x-www-form-urlencoded"})
    re=re.json()
    sa=[]
    while True:
        if re and re["code"]!=None:
            if re['code']==0 :
                for i in re['data']['cookie_info']['cookies'] :
                    r.cookies.set(i['name'],i['value'],domain='.bilibili.com',path='/')
                    sa.append({'name':i['name'],'value':i['value'],'domain':'.bilibili.com','path':'/'})
                return sa
            elif re['code']==-105 :
                re=r.get('https://passport.bilibili.com/captcha',headers={'Host': "passport.bilibili.com"},decode_level=1)
                cp=scap(r,re)
                if cp:
                    print('登录验证码识别结果:%s'%(cp))
                    keyhash,pubkey=getk()
                    if keyhash==-1:
                        return -1
                    pm=f"appkey={appkey}&captcha={cp}&password={parse.quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(),pubkey)))}&username={parse.quote_plus(username)}"
                    re=r.post('https://passport.bilibili.com/api/v2/oauth2/login',f"{pm}&sign={cal_sign(pm)}",headers={'Content-type':"application/x-www-form-urlencoded"})
                    re=re.json()
                else :
                    print('登录验证码识别服务暂时不可用，请稍后再试')
                    return -1
            elif re['code']==-449:
                print('服务繁忙, 尝试使用V3接口登录')
                pm=f"access_key=&actionKey=appkey&appkey={appkey}&build=6040500&captcha=&challenge=&channel=bili&cookies=&device=phone&mobi_app=android&password={parse.quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(),pubkey)))}&permission=ALL&platform=android&seccode=&subid=1&ts={int(time.time())}&username={parse.quote_plus(username)}&validate="
                re=r.post('https://passport.bilibili.com/api/v3/oauth2/login',f"{pm}&sign={cal_sign(pm)}",headers={'Content-type':"application/x-www-form-urlencoded"})
                re=re.json()
            else :
                print(f"{re['code']} {re['message']}")
                return -1
    return sa
def cal_sign(p):
    salt = "60698ba2f68e01ce44738920a0ffe768"
    sh=hashlib.md5()
    sh.update(f"{p}{salt}".encode())
    return sh.hexdigest()
def scap(r:requests.session,image):
    re=r.post("https://bili.dev:2233/captcha",json={'image':base64.b64encode(image).decode("utf-8")})
    return re['message'] if re and re.get("code")==0 else None
