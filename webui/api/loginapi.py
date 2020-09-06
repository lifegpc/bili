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
import hashlib
from requests import Session
import rsa


keyhash = None
pubkey = None


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

    def _cal_sign(self, p):
        sh = hashlib.md5()
        sh.update(f"{p}{self._salt}".encode())
        return sh.hexdigest()


class getpubkey(loginapi):
    _VALID_URI = r'^getpubkey$'

    def _handle(self):
        return self._get_pubkey()
