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
from . import apic
import rsa
from base64 import b64encode

pubkey = None
privkey = None


def decrypt(s: bytes) -> bytes:
    "解密"
    return rsa.decrypt(s, privkey)


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


class apirsa(apic):
    _VALID_URI = r'^rsa$'

    def _handle(self):
        global pubkey, privkey
        if pubkey is None:
            pubkey, privkey = rsa.newkeys(2048)
        k = b64encode(int_to_bytes(pubkey.n)).decode('utf8')
        e = b64encode(int_to_bytes(pubkey.e)).decode('utf8')
        return {'code': '0', 'k': k, 'e': e}
