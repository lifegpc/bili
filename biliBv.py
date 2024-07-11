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
table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608


def debv(x):
    if len(x) == 11:
        x = "BV1" + x[2:]
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58**i
    return (r - add) ^ xor


def enbv(x):
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58**i % 58]
    return ''.join(r)

###########################################################
#                   NEW VERSION                           #
###########################################################

XOR_CODE = 23442827791579
MASK_CODE = 2251799813685247
MAX_AID = 1 << 51

data = [b'F', b'c', b'w', b'A', b'P', b'N', b'K', b'T', b'M', b'u', b'g', b'3', b'G', b'V', b'5', b'L', b'j', b'7', b'E', b'J', b'n', b'H', b'p', b'W', b's', b'x', b'4', b't', b'b', b'8', b'h', b'a', b'Y', b'e', b'v', b'i', b'q', b'B', b'z', b'6', b'r', b'k', b'C', b'y', b'1', b'2', b'm', b'U', b'S', b'D', b'Q', b'X', b'9', b'R', b'd', b'o', b'Z', b'f']

BASE = 58
BV_LEN = 12
PREFIX = "BV1"

def av2bv(aid):
    bytes = [b'B', b'V', b'1', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0', b'0']
    bv_idx = BV_LEN - 1
    tmp = (MAX_AID | aid) ^ XOR_CODE
    while int(tmp) != 0:
        bytes[bv_idx] = data[int(tmp % BASE)]
        tmp /= BASE
        bv_idx -= 1
    bytes[3], bytes[9] = bytes[9], bytes[3]
    bytes[4], bytes[7] = bytes[7], bytes[4]
    return "".join([i.decode() for i in bytes])

def bv2av(bvid: str):
    bvid = list(bvid)
    bvid[3], bvid[9] = bvid[9], bvid[3]
    bvid[4], bvid[7] = bvid[7], bvid[4]
    bvid = bvid[3:]
    tmp = 0
    for i in bvid:
        idx = data.index(i.encode())
        tmp = tmp * BASE + idx
    return (tmp & MASK_CODE) ^ XOR_CODE