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
from lang import getlan,getdict
import sys
from command import gopt
from inspect import currentframe
from json import dumps


lan=None
se=JSONParser.loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('biliLogin',getlan(se,ip))
def login(r, ud: dict, ip: dict, logg = None):
    '登录至B站'
    global lan
    try :
        driver=webdriver.Chrome()
        if logg is not None:
            logg.write("OEPN https://passport.bilibili.com/ajax/miniLogin/minilogin in ChromeDriver", currentframe(), "OPEN WEB")
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
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "CHROME DRIVER FAILED")
        print(traceback.format_exc())
        print(lan['ERROR1'])#使用ChromeDriver登录发生错误，尝试采用用户名、密码登录
        read = login2(r, logg)
        if read==-1 :
            print(lan['ERROR2'])#登录失败！
            return 2
        sa=read
    rr = tryok(r, ud , logg)
    if rr==True :
        if not 's' in ip:
            print(lan['OUTPUT1'])#登录成功！
        JSONParser.savecookie(sa)
        return 0
    elif rr==False :
        print(lan['ERROR3'])#网络错误！
        return 1
    else :
        print(lan['ERROR4']+str(rr['code'])+","+str(rr['message']))#登录失败：
        return 2
def tryok(r, ud: dict, logg = None):
    '验证是否登录成功'
    try :
        if logg is not None:
            logg.write(f"GET https://api.bilibili.com/x/web-interface/nav", currentframe(), "VERIFY LOGIN")
        re=r.get('https://api.bilibili.com/x/web-interface/nav')
    except :
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "VERIFY LOGIN FAILED 1")
        return False
    re.encoding='utf8'
    try :
        if logg is not None:
            logg.write(re.text, currentframe(), "VERIFY API RETURN")
        obj=re.json()
        if obj['code']==0 and 'data' in obj and obj['data']['isLogin']:
            ud['d']=obj['data']
            return True
        return obj
    except :
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "VERIFY LOGIN FAILED 2")
        return re.text
def login2(r: requests.Session, logg = None):
    "使用用户名密码登录"
    username=input(lan['INPUT1'])#请输入用户名：
    password=getpass(lan['INPUT2'])#请输入密码：
    appkey="bca7e84c2d947ac6"
    def getk():
        if logg is not None:
            logg.write("GET https://passport.bilibili.com/api/oauth2/getKey", currentframe(), "GETPUBKEY")
        re=r.post('https://passport.bilibili.com/api/oauth2/getKey',{'appkey':appkey,'sign':cal_sign("appkey=%s"%(appkey))})
        re=re.json()
        if re['code']!=0 :
            return -1,-1
        return re['data']['hash'],rsa.PublicKey.load_pkcs1_openssl_pem(re['data']['key'].encode())
    keyhash,pubkey=getk()
    if keyhash==-1:
        return -1
    if logg is not None:
        logg.write("POST https://passport.bilibili.com/api/v2/oauth2/login", currentframe(), "TRY V3 INTERFACE")
    pm=f"appkey={appkey}&password={parse.quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(), pubkey)))}&username={parse.quote_plus(username)}"
    pm2=f"{pm}&sign={cal_sign(pm)}"
    re=r.post('https://passport.bilibili.com/api/v2/oauth2/login',pm2,headers={'Content-type': "application/x-www-form-urlencoded"})
    re=re.json()
    sa=[]
    while True:
        if re and re["code"]!=None:
            if logg is not None and re['code'] != 0:
                logg.write(dumps(re, ensure_ascii=False), currentframe(), "RETURN")
            if re['code']==0 :
                if logg is not None:
                    logg.write(f"re['data'].keys() = {re['data'].keys()}", currentframe(), "Login info keys")
                if 'status' in re['data'] and re['data']['status'] == 2:
                    print(f"{re['data']['message']}\n{re['data']['url']}")
                    input(lan['ERROR7'])
                    continue
                if 'cookie_info' in re['data'] and 'cookies' in re['data']['cookie_info']:
                    for i in re['data']['cookie_info']['cookies'] :
                        r.cookies.set(i['name'],i['value'],domain='.bilibili.com',path='/')
                        sa.append({'name':i['name'],'value':i['value'],'domain':'.bilibili.com','path':'/'})
                    return sa
                return -1
            elif re['code']==-105 :
                if logg is not None:
                    logg.write("GET https://passport.bilibili.com/captcha", currentframe(), "GETCAPTCHA")
                re=r.get('https://passport.bilibili.com/captcha',headers={'Host': "passport.bilibili.com"}).content
                cp=scap(r,re)
                if cp:
                    print(lan['OUTPUT2'].replace('<result>',str(cp)))#登录验证码识别结果：<result>
                    keyhash,pubkey=getk()
                    if keyhash==-1:
                        return -1
                    pm=f"appkey={appkey}&captcha={cp}&password={parse.quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(),pubkey)))}&username={parse.quote_plus(username)}"
                    re=r.post('https://passport.bilibili.com/api/v2/oauth2/login',f"{pm}&sign={cal_sign(pm)}",headers={'Content-type':"application/x-www-form-urlencoded"})
                    re=re.json()
                else :
                    print(lan['ERROR5'])#登录验证码识别服务暂时不可用，请稍后再试
                    return -1
            elif re['code']==-449:
                print(lan['ERROR6'])#服务繁忙, 尝试使用V3接口登录
                if logg is not None:
                    logg.write("POST https://passport.bilibili.com/api/v3/oauth2/login", currentframe(), "TRY V3 INTERFACE")
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
    try:
        re=r.post("https://bili.dev:2233/captcha",json={'image':base64.b64encode(image).decode("utf-8")})
        re=re.json()
    except:
        return None
    return re['message'] if re and re["code"]==0 else None


def dealwithcap(r:requests.Session, uri:str, logg=None):
    "尝试通过验证"
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.bilibili.com')
        for i in ['DedeUserID', 'DedeUserID__ckMd5', 'Expires', 'SESSDATA', 'bili_jct']:
            driver.add_cookie({'name':i ,'value': r.cookies.get(i), 'domain': '.bilibili.com', 'path': '/'})
        driver.get(uri)
        time.sleep(10)  # 等待加载完毕
        aa = True
        while aa:
            time.sleep(1)
            try:
                driver.find_element_by_class_name('error-panel server-error')
            except:
                if logg is not None:
                    logg.write(traceback.format_exc(), currentframe(), "DEAL WITH CAP ERROR1")
                aa = False
    except Exception:
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "DEAL WITH CAP ERROR2")
        print(traceback.format_exc())
