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
from . import apic, new_Session
import web
import hashlib
from requests import Session
import rsa
from base64 import b64encode, b64decode
from .rsa import decrypt
import traceback
from urllib.parse import quote_plus, urlsplit, parse_qs
from JSONParser import savecookie
import time


keyhash = None
pubkey = None
web_keyhash = None
web_pubkey = None


class loginapi(apic):
    _appkey = "bca7e84c2d947ac6"
    _salt = "60698ba2f68e01ce44738920a0ffe768"
    _r: Session = None

    def __init__(self, inp: str):
        apic.__init__(self, inp)
        self._r = new_Session(False)

    def _get_pubkey(self):
        re = self._r.post('https://passport.bilibili.com/api/oauth2/getKey', {
                          'appkey': self._appkey, 'sign': self._cal_sign("appkey=%s" % (self._appkey))})
        re = re.json()
        if re['code'] != 0:
            return {'code': -1, 'result': re}
        global keyhash, pubkey
        keyhash = re['data']['hash']
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(
            re['data']['key'].encode())
        return {'code': 0}

    def _captcha(self):
        "获取验证码图片"
        re = self._r.get('https://passport.bilibili.com/captcha')
        img = b64encode(re.content).decode('utf8')
        ct = re.headers['Content-type'] if 'Content-type' in re.headers else None
        cap = None
        try:
            re = self._r.post('https://bili.dev:2233/captcha',
                              json={'image': img})
            if re.status_code == 200:
                re = re.json()
                if re and re["code"] == 0:
                    cap = re['message']
        except:
            pass
        return {'code': 0, 'img': img, 'cap': cap, 'type': ct}

    def _login_with_user_pass(self):
        "使用用户名和密码登录"
        username = web.input().get('username')
        password = web.input().get('password')
        capt = web.input().get('capt')
        if username is None or password is None:
            return {'code': -1}
        try:
            username = decrypt(b64decode(username)).decode('utf8')
            password = decrypt(b64decode(password)).decode('utf8')
        except:
            return {'code': -2, 'e': traceback.format_exc()}
        if capt is None:
            pm = f"appkey={self._appkey}&password={self._encrypt(f'{keyhash}{password}')}&username={quote_plus(username)}"
        else:
            pm = f"appkey={self._appkey}&captcha={capt}&password={self._encrypt(f'{keyhash}{password}')}&username={quote_plus(username)}"
        pm2 = f"{pm}&sign={self._cal_sign(pm)}"
        re = self._r.post("https://passport.bilibili.com/api/v2/oauth2/login",
                          pm2, headers={'Content-type': "application/x-www-form-urlencoded"})
        re = re.json()
        if re['code'] == 0:
            sa = []
            for i in re['data']['cookie_info']['cookies']:
                sa.append({'name': i['name'], 'value': i['value'],
                           'domain': '.bilibili.com', 'path': '/'})
            savecookie(sa)
            return {'code': 0}
        elif re['code'] == -105:
            return {'code': -3}
        elif re['code'] == -449:
            pm = f"access_key=&actionKey=appkey&appkey={self._appkey}&build=6040500&captcha=&challenge=&channel=bili&cookies=&device=phone&mobi_app=android&password={self._encrypt(f'{keyhash}{password}')}&permission=ALL&platform=android&seccode=&subid=1&ts={int(time.time())}&username={quote_plus(username)}&validate="
            pm2 = f"{pm}&sign={self._cal_sign(pm)}"
            re = self._r.post('https://passport.bilibili.com/api/v3/oauth2/login',
                              pm2, headers={'Content-type': "application/x-www-form-urlencoded"})
            re = re.json()
            if re['code'] == 0:
                sa = []
                for i in re['data']['cookie_info']['cookies']:
                    sa.append({'name': i['name'], 'value': i['value'],
                               'domain': '.bilibili.com', 'path': '/'})
                savecookie(sa)
                return {'code': 0}
            return {'code': -4, 'result': re}
        elif re['code'] == -629:  # 用户名或密码错误
            return {'code': -6}
        else:
            return {'code': -5, 'result': re}
        return {'code': -7}

    def _qr_getloginurl(self):
        re = self._r.get('https://passport.bilibili.com/qrcode/getLoginUrl')
        re = re.json()
        return {'code': 0, 'result': re}

    def _qr_getlogininfo(self):
        key = web.input().get('key')
        if key is None:
            return {'code': -1}
        re = self._r.post('https://passport.bilibili.com/qrcode/getLoginInfo', {
                          'oauthKey': key, 'gourl': 'https://passport.bilibili.com/ajax/miniLogin/redirect'})
        re = re.json()
        if re['status']:
            self._save_cookie(re['data']['url'])
        return {'code': 0, 'status': re['status']}

    def _cal_sign(self, p):
        sh = hashlib.md5()
        sh.update(f"{p}{self._salt}".encode())
        return sh.hexdigest()

    def _encrypt(self, s: str):
        return quote_plus(b64encode(rsa.encrypt(s.encode(), pubkey)))

    def _encrypt_web(self, s: str):
        return b64encode(rsa.encrypt(s.encode(), web_pubkey)).decode()

    def _get_country_list(self):
        re = self._r.get(
            'https://passport.bilibili.com/web/generic/country/list')
        re = re.json()
        if re['code'] == 0:
            data = re['data']
            return {'code': 0, 'result': data['common'] + data['others']}
        return {'code': -1, 'result': re}

    def _get_captcha_combine(self):
        "获取网页验证的数据，调用initGeetest时使用。"
        re = self._r.get(f'https://passport.bilibili.com/web/captcha/combine?plat=6&t={round(time.time()*1000)}', headers={
                         'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
        re = re.json()
        if re['code'] == 0:
            return {'code': 0, 'data': re['data']}
        return {'code': -1, 'result': re}

    def _sendloginSMS(self):
        "发送验证短信请求"
        queries = web.ctx.query
        qr = parse_qs(queries[1:])
        for key in qr.keys():
            qr[key] = qr[key][0]
        try:
            qr['tel'] = decrypt(b64decode(qr['tel'])).decode('utf8')
        except:
            return {'code': -1, 'e': traceback.format_exc()}
        re = self._r.post(f'https://passport.bilibili.com/web/sms/general/v2/send', data=qr,
                          headers={'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
        re = re.json()
        if re['code'] == 0:
            return {'code': 0}
        else:
            return {'code': -2, 'result': re}

    def _login_with_SMS(self):
        queries = web.ctx.query
        qr = parse_qs(queries[1:])
        for key in qr.keys():
            qr[key] = qr[key][0]
        try:
            qr['tel'] = decrypt(b64decode(qr['tel'])).decode('utf8')
        except:
            return {'code': -1, 'e': traceback.format_exc()}
        re = self._r.post('https://passport.bilibili.com/web/login/rapid', data=qr,
                          headers={'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
        re = re.json()
        if re['code'] == 0:
            if 'data' in re and 'is_new' in re['data'] and re['data']['is_new']:
                re = self._r.post('https://passport.bilibili.com/web/reg/rapid', data=qr, headers={
                                  'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
                re = re.json()
                if re['code'] == 0:
                    self._save_cookie(re['data']['url'])
                    return {'code': 0}
                else:
                    return {'code': -2, 'result': re}
            self._save_cookie(re['data']['url'])
            return {'code': 0}
        else:
            return {'code': -2, 'result': re}

    def _get_pubkey_web(self):
        re = self._r.get(f'https://passport.bilibili.com/login?act=getkey&_={round(time.time()*1000)}', headers={
                         'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
        re = re.json()
        global web_keyhash, web_pubkey
        web_keyhash = re['hash']
        web_pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(re['key'].encode())
        return {'code': 0}

    def _login_with_user_pass_web(self):
        queries = web.ctx.query
        qr = parse_qs(queries[1:])
        for key in qr.keys():
            qr[key] = qr[key][0]
        try:
            pas = decrypt(b64decode(qr['password'])).decode('utf8')
            qr['username'] = decrypt(b64decode(qr['username'])).decode('utf8')
        except:
            return {'code': -1, 'e': traceback.format_exc()}
        qr['password'] = self._encrypt_web(web_keyhash + pas)
        re = self._r.post('https://passport.bilibili.com/web/mini/login', data=qr,
                          headers={'referer': 'https://passport.bilibili.com/ajax/miniLogin/minilogin'})
        re = re.json()
        if re['code'] == 0:
            self._save_cookie(re['data']['redirectUrl'])
            return {'code': 0}
        else:
            return {'code': -2, 'result': re}

    def _save_cookie(self, url):
        "保存来自URL的Cookie"
        urlp = urlsplit(url)
        urlp2 = parse_qs(urlp.query)
        sa = []
        for i in urlp2.keys():
            if i != "gourl":
                i2 = urlp2[i][0]
                sa.append({'name': i, 'value': i2,
                           'domain': '.bilibili.com', 'path': '/'})
        savecookie(sa)


class getpubkey(loginapi):
    _VALID_URI = r'^getpubkey$'

    def _handle(self):
        return self._get_pubkey()


class captcha(loginapi):
    _VALID_URI = r'^captcha$'

    def _handle(self):
        return self._captcha()


class login(loginapi):
    _VALID_URI = r'^login$'

    def _handle(self):
        t = web.input().get('type')
        if t is None:
            return {'code': -1}
        if t == "0":
            return self._login_with_user_pass()
        return {'code': -1}


class qrgetloginurl(loginapi):
    _VALID_URI = r'^qrgetloginurl$'

    def _handle(self):
        return self._qr_getloginurl()


class qrgetlogininfo(loginapi):
    _VALID_URI = r'^qrgetlogininfo$'

    def _handle(self):
        return self._qr_getlogininfo()


class getcountrylist(loginapi):
    _VALID_URI = r'^getcountrylist$'

    def _handle(self):
        return self._get_country_list()


class getcaptchacombine(loginapi):
    _VALID_URI = r'^getcaptchacombine$'

    def _handle(self):
        return self._get_captcha_combine()


class sendloginsms(loginapi):
    _VALID_URI = r'^sendloginsms$'

    def _handle(self):
        return self._sendloginSMS()


class loginwithsms(loginapi):
    _VALID_URI = r'^loginwithsms$'

    def _handle(self):
        return self._login_with_SMS()


class getpubkeyweb(loginapi):
    _VALID_URI = r'^getpubkeyweb$'

    def _handle(self):
        return self._get_pubkey_web()


class loginwithuserpassweb(loginapi):
    _VALID_URI = r'^loginwithuserpassweb$'

    def _handle(self):
        return self._login_with_user_pass_web()
