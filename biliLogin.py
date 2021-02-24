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
import base64
from lang import getlan, getdict
import sys
from command import gopt
from inspect import currentframe
from json import dumps
from os.path import exists, abspath
from os import mkdir, remove
from random import randint, randrange
from urllib.parse import quote_plus, parse_qsl, urlsplit
from qrcode import QRCode, constants as qrconst
from qrcode.image.svg import SvgImage
from platform import system


lan = None
se = JSONParser.loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
lan = getdict('biliLogin', getlan(se, ip))


def login(r, ud: dict, ip: dict, logg=None):
    '登录至B站'
    global lan
    url = "https://passport.bilibili.com/ajax/miniLogin/minilogin"
    reurl = "https://passport.bilibili.com/ajax/miniLogin/redirect"
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("disable-logging")
        option.add_argument('log-level=3')
        driver = webdriver.Chrome(options=option)
        if logg is not None:
            logg.write(f"OEPN {url} in ChromeDriver", currentframe(), "OPEN WEB")
        driver.get(url)
        aa = True
        while aa:
            time.sleep(1)
            if driver.current_url == reurl:
                aa = False
        sa = []
        for i in driver.get_cookies():
            r.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
            t = {'name': i['name'], 'value': i['value'], 'domain': i['domain'], 'path': i['path']}
            sa.append(t)
        driver.close()
    except Exception:
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "CHROME DRIVER FAILED")
        print(traceback.format_exc())
        try:
            driver = webdriver.Firefox()
            if logg is not None:
                logg.write(f"OEPN {url} in FirefoxDriver", currentframe(), "OPEN WEB")
            driver.get(url)
            aa = True
            while aa:
                time.sleep(1)
                if driver.current_url == reurl:
                    aa = False
            sa = []
            for i in driver.get_cookies():
                r.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
                t = {'name': i['name'], 'value': i['value'], 'domain': i['domain'], 'path': i['path']}
                sa.append(t)
            driver.close()
        except:
            if logg is not None:
                logg.write(traceback.format_exc(), currentframe(), "GECKO DRIVER FAILED")
            print(traceback.format_exc())
            print(f"{lan['ERROR1']} {lan['QRCODE']}")  # 使用ChromeDriver登录发生错误，尝试采用用户名、密码登录
            read = login2(r, logg)
            if read in [-1, -2]:
                if read == -1:
                    print(lan['ERROR2'])  # 登录失败！
                read = loginwithqrcode(r, logg)
                if read == -1:
                    print(lan['ERROR2'])  # 登录失败！
                    return 2
            sa = read
    rr = tryok(r, ud, logg)
    if rr is True:
        if 's' not in ip:
            print(lan['OUTPUT1'])  # 登录成功！
        JSONParser.savecookie(sa)
        return 0
    elif rr is False:
        print(lan['ERROR3'])  # 网络错误！
        return 1
    else:
        print(lan['ERROR4'] + str(rr['code']) + "," + str(rr['message']))  # 登录失败：
        return 2


def tryok(r, ud: dict, logg=None):
    '验证是否登录成功'
    try:
        if logg is not None:
            logg.write("GET https://api.bilibili.com/x/web-interface/nav", currentframe(), "VERIFY LOGIN")
        re = r.get('https://api.bilibili.com/x/web-interface/nav')
    except:
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "VERIFY LOGIN FAILED 1")
        return False
    re.encoding = 'utf8'
    try:
        if logg is not None:
            logg.write(re.text, currentframe(), "VERIFY API RETURN")
        obj = re.json()
        if obj['code'] == 0 and 'data' in obj and obj['data']['isLogin']:
            ud['d'] = obj['data']
            if 'vipStatus' in ud['d'] and ud['d']['vipStatus'] != 1:
                ud['d']['vipStatus'] = 0
            return True
        return obj
    except:
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "VERIFY LOGIN FAILED 2")
        return re.text


def login2(r: requests.Session, logg=None):
    "使用用户名密码登录"
    username = input(lan['INPUT1'])  # 请输入用户名：
    if len(username) == 0:
        return -2
    password = getpass(lan['INPUT2'])  # 请输入密码：
    appkey = "bca7e84c2d947ac6"

    def getk():
        if logg is not None:
            logg.write("GET https://passport.bilibili.com/api/oauth2/getKey", currentframe(), "GETPUBKEY")
        re = r.post('https://passport.bilibili.com/api/oauth2/getKey', {'appkey': appkey, 'sign': cal_sign("appkey=%s" % (appkey))})
        re = re.json()
        if re['code'] != 0:
            return -1, -1
        return re['data']['hash'], rsa.PublicKey.load_pkcs1_openssl_pem(re['data']['key'].encode())
    keyhash, pubkey = getk()
    if keyhash == -1:
        return -1
    if logg is not None:
        logg.write("POST https://passport.bilibili.com/api/v2/oauth2/login", currentframe(), "TRY V3 INTERFACE")
    pm = f"appkey={appkey}&password={quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(), pubkey)))}&username={quote_plus(username)}"
    pm2 = f"{pm}&sign={cal_sign(pm)}"
    re = r.post('https://passport.bilibili.com/api/v2/oauth2/login', pm2, headers={'Content-type': "application/x-www-form-urlencoded"})
    re = re.json()
    sa = []
    while True:
        if re and re["code"] is not None:
            if logg is not None and re['code'] != 0:
                logg.write(dumps(re, ensure_ascii=False), currentframe(), "RETURN")
            if re['code'] == 0:
                if logg is not None:
                    logg.write(f"re['data'].keys() = {re['data'].keys()}", currentframe(), "Login info keys")
                if 'status' in re['data'] and re['data']['status'] == 2:
                    print(f"{re['data']['message']}\n{re['data']['url']}")
                    input(lan['ERROR7'])
                    continue
                if 'cookie_info' in re['data'] and 'cookies' in re['data']['cookie_info']:
                    for i in re['data']['cookie_info']['cookies']:
                        r.cookies.set(i['name'], i['value'], domain='.bilibili.com', path='/')
                        sa.append({'name': i['name'], 'value': i['value'], 'domain': '.bilibili.com', 'path': '/'})
                    return sa
                return -1
            elif re['code'] == -105:
                if logg is not None:
                    logg.write("GET https://passport.bilibili.com/captcha", currentframe(), "GETCAPTCHA")
                re = r.get('https://passport.bilibili.com/captcha', headers={'Host': "passport.bilibili.com"}).content
                cp = scap(r, re)
                if cp:
                    print(lan['OUTPUT2'].replace('<result>', str(cp)))  # 登录验证码识别结果：<result>
                    keyhash, pubkey = getk()
                    if keyhash == -1:
                        return -1
                    pm = f"appkey={appkey}&captcha={cp}&password={quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(),pubkey)))}&username={quote_plus(username)}"
                    re = r.post('https://passport.bilibili.com/api/v2/oauth2/login', f"{pm}&sign={cal_sign(pm)}", headers={'Content-type': "application/x-www-form-urlencoded"})
                    re = re.json()
                else:
                    print(lan['ERROR5'])  # 登录验证码识别服务暂时不可用，请稍后再试
                    return -1
            elif re['code'] == -449:
                print(lan['ERROR6'])  # 服务繁忙, 尝试使用V3接口登录
                logurl = "https://passport.bilibili.com/x/passport-login/oauth2/login"
                if logg is not None:
                    logg.write(f"POST {logurl}", currentframe(), "TRY V3 INTERFACE")
                pm = f"access_key=&actionKey=appkey&appkey={appkey}&build=6040500&captcha=&challenge=&channel=bili&cookies=&device=phone&mobi_app=android&password={quote_plus(base64.b64encode(rsa.encrypt(f'{keyhash}{password}'.encode(),pubkey)))}&permission=ALL&platform=android&seccode=&subid=1&ts={int(time.time())}&username={quote_plus(username)}&validate="
                re = r.post(logurl, f"{pm}&sign={cal_sign(pm)}", headers={'Content-type': "application/x-www-form-urlencoded"})
                re = re.json()
            else:
                print(f"{re['code']} {re['message']}")
                return -1
    return sa


def cal_sign(p):
    salt = "60698ba2f68e01ce44738920a0ffe768"
    sh = hashlib.md5()
    sh.update(f"{p}{salt}".encode())
    return sh.hexdigest()


def scap(r: requests.session, image):
    try:
        re = r.post("https://bili.dev:2233/captcha", json={'image': base64.b64encode(image).decode("utf-8")})
        re = re.json()
    except:
        return None
    return re['message'] if re and re["code"] == 0 else None


def dealwithcap(r: requests.Session, uri: str, logg=None):
    "尝试通过验证"
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.bilibili.com')
        for i in ['DedeUserID', 'DedeUserID__ckMd5', 'Expires', 'SESSDATA', 'bili_jct']:
            driver.add_cookie({'name': i, 'value': r.cookies.get(i), 'domain': '.bilibili.com', 'path': '/'})
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


def generateRandomHex(w: int) -> str:
    i = randrange(0, 16**w)
    s = hex(i)[2:].upper()
    return "0" * (w - len(s)) + s


def generateUUID():
    s = f"{generateRandomHex(8)}-{generateRandomHex(4)}-{generateRandomHex(4)}-{generateRandomHex(4)}-{generateRandomHex(12)}"
    t = round(time.time() * 1000)
    s += f"{t%10000:05}infoc"
    return s


def prepareSession(r: requests.Session):
    r.cookies.clear()
    r.cookies.clear_session_cookies()
    r.headers.update({"referer": "https://passport.bilibili.com/login"})
    r.get("https://api.bilibili.com/x/web-interface/nav")  # get bfe_id
    r.get("https://passport.bilibili.com/web/generic/country/list")  # get sid
    r.cookies.set("finger", str(randint(1e9, 2e9)), path='/', domain="passport.bilibili.com", discard=True)  # 瞎几把指定finger
    year = 365 * 24 * 3600
    r.cookies.set("_uuid", generateUUID(), path="/", domain=".bilibili.com", expires=round(time.time() + year), discard=False)  # generate UUID
    r.get("https://data.bilibili.com/v/web/web_page_view", data={"mid": "null", "fts": "null", "url": quote_plus("https://passport.bilibili.com/login"), "proid": "3", "ptype": "2", "module": "game", "title": "哔哩哔哩弹幕视频网 - ( ゜- ゜)つロ 乾杯~ - bilibili", "ajaxtag": "", "ajaxid": "", "page_ref": ""})  # get buvid3 and buvid2
    fp = generateRandomHex(32).lower()  # generate fingerprint
    r.cookies.set("fingerprint", fp, path="/", domain=".bilibili.com", expires=round(time.time() + year), discard=False)
    re = r.get("https://api.bilibili.com/x/frontend/finger/fpfmc", data={"fp": fp})  # upload fingerprint
    try:
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
        else:
            if "buvid_fp" in re['data'] and re['data']['buvid_fp']:
                r.cookies.set("buvid_fp", re['data']['buvid_fp'], path="/", domain=".bilibili.com", expires=round(time.time() + year), discard=False)
            if 'buvid_fp_plain' in re['data'] and re['data']['buvid_fp_plain']:
                r.cookies.set("buvid_fp_plain", re['data']['buvid_fp_plain'], path="/", domain=".bilibili.com", expires=round(time.time() + year), discard=False)
    except:
        pass


def loginwithqrcode(r: requests.Session, logg=None):
    print(lan['WARN1'])
    prepareSession(r)
    year = 365 * 24 * 3600
    while True:
        url = "https://passport.bilibili.com/qrcode/getLoginUrl"
        if logg:
            logg.write(f"GET {url}", currentframe(), "getloginurl")
        re = r.get(url)
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']}")
            if logg:
                logg.write(f"content: {re}", currentframe(), "unknownerror")
            return -1
        ts = re['ts']
        oauthKey = re['data']['oauthKey']
        oauthUrl = re['data']['url']
        if not exists('Temp/'):
            mkdir('Temp/')
        qr = QRCode(version=1, error_correction=qrconst.ERROR_CORRECT_H, box_size=10)
        qr.add_data(oauthUrl)
        pn = f'Temp/{ts}.svg'
        qr.make_image(SvgImage).save(pn)
        print(lan['OUTPUT3'].replace("<path>", pn))  # 二维码已保存至
        if system() == "Windows":
            from win32com.shell import shell  # pylint: disable=import-error no-name-in-module
            d = shell.SHParseDisplayName(abspath(pn), 0)
            shell.SHOpenFolderAndSelectItems(d[0], [], 0)
        suc = False
        while not suc:
            re = r.post("https://passport.bilibili.com/qrcode/getLoginInfo", data={"oauthKey": oauthKey, "gourl": ""})
            re = re.json()
            if re['status']:
                url = re['data']['url']
                for (key, value) in parse_qsl(urlsplit(url).query):
                    if key != "gourl" and key != "Expires":
                        r.cookies.set(key, value, path="/", domain=".bilibili.com", expires=round(time.time() + year), discard=False)
                suc = True
                if exists(pn):
                    try:
                        remove(pn)
                    except:
                        pass
                break
            else:
                if re['data'] == -4:
                    time.sleep(3)
                    if time.time() > ts + 300:
                        if exists(pn):
                            try:
                                remove(pn)
                            except:
                                pass
                        input(lan['OUTPUT4'])
                        break
                elif re['data'] == -2:
                    if exists(pn):
                        try:
                            remove(pn)
                        except:
                            pass
                    input(lan['OUTPUT4'])
                    break
                else:
                    if exists(pn):
                        try:
                            remove(pn)
                        except:
                            pass
                    print(f"{re['data']} {re['message']}")
                    return -1
        if suc:
            sa = []
            for domain in r.cookies._cookies.keys():
                for path in r.cookies._cookies[domain].keys():
                    for cookiename in r.cookies._cookies[domain][path]:
                        cookie = r.cookies._cookies[domain][path][cookiename]
                        if not cookie.discard:
                            sa.append({"name": cookie.name, "value": cookie.value, 'domain': cookie.domain, 'path': cookie.path})
            return sa


def acCheckLogin(r: requests.Session, ud: dict, logg=None):
    "验证Acfun是否登录"
    try:
        url = "https://www.acfun.cn/rest/pc-direct/user/personalInfo"
        if logg:
            logg.write(f"Get {url}", currentframe(), "Acfun verify login request")
        re = r.get(url)
    except:
        if logg:
            logg.write(traceback.format_exc(), currentframe(), "Acfun verify login request failed")
        return False
    re.encoding = 'utf8'
    try:
        if logg:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Acfun verify login result")
        re = re.json()
        if re['result'] == 0:
            ud['d'] = re['info']
            return True
        if re['result'] != -401:
            print(f"{re['result']} {re['error_msg']}")
        return re
    except:
        if logg:
            logg.write(traceback.format_exc(), currentframe(), "Acfun verify login failed")
        return re.text


def acLogin(r: requests.Session, ud: dict, ip: dict, logg=None):
    '''登录Acfun
    0 登录成功
    1 网络错误
    2 登录失败'''
    global lan
    reurl = "https://www.acfun.cn/"
    url = f"https://www.acfun.cn/login/?returnUrl={quote_plus(reurl)}"
    try:
        option = webdriver.ChromeOptions()
        option.add_argument("disable-logging")
        option.add_argument('log-level=3')
        driver = webdriver.Chrome(options=option)
        if logg is not None:
            logg.write(f"OEPN {url} in ChromeDriver", currentframe(), "OPEN WEB")
        driver.get(url)
        aa = True
        while aa:
            time.sleep(1)
            if driver.current_url == reurl:
                aa = False
        sa = []
        for i in driver.get_cookies():
            r.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
            t = {'name': i['name'], 'value': i['value'], 'domain': i['domain'], 'path': i['path']}
            sa.append(t)
        driver.close()
    except Exception:
        if logg is not None:
            logg.write(traceback.format_exc(), currentframe(), "CHROME DRIVER FAILED")
        print(traceback.format_exc())
        try:
            driver = webdriver.Firefox()
            if logg is not None:
                logg.write(f"OEPN {url} in FirefoxDriver", currentframe(), "OPEN WEB")
            driver.get(url)
            aa = True
            while aa:
                time.sleep(1)
                if driver.current_url == reurl:
                    aa = False
            sa = []
            for i in driver.get_cookies():
                r.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
                t = {'name': i['name'], 'value': i['value'], 'domain': i['domain'], 'path': i['path']}
                sa.append(t)
            driver.close()
        except:
            if logg is not None:
                logg.write(traceback.format_exc(), currentframe(), "GECKO DRIVER FAILED")
            print(traceback.format_exc())
            return 2
    rr = acCheckLogin(r, ud, logg)
    if rr is True:
        if 's' not in ip:
            print(lan['OUTPUT1'])  # 登录成功！
        JSONParser.savecookie(sa, "acfun_cookies.json")
        return 0
    elif rr is False:
        print(lan['ERROR3'])  # 网络错误！
        return 1
    else:
        print(lan['ERROR4'] + str(rr['code']) + "," + str(rr['error_msg']))  # 登录失败：
        return 2
