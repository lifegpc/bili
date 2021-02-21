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
from time import gmtime, strftime, time, strptime, timezone, mktime, struct_time, localtime
from math import floor


def getDate(s):
    "获取时间戳对应日期 UTF+8"
    i = float(s)
    return gmtime(i + 3600 * 8)


def getNowDate():
    "获取当前日期 UTF+8"
    return getDate(time())


def tostr(fa):
    "转化为字符串"
    return strftime("%Y-%m-%d", fa)


def equal(a, b):
    "比较是否同一天，同一天0，前面大1，后面大-1"
    if a[0] > b[0]:
        return 1
    elif a[0] < b[0]:
        return -1
    else:
        if a[1] > b[1]:
            return 1
        elif a[1] < b[1]:
            return -1
        else:
            if a[2] > b[2]:
                return 1
            elif a[2] < b[2]:
                return -1
            else:
                return 0


def checktime(s: str):
    """检查时间是否无问题\n
    True 无问题\n
    False 有问题"""
    try:
        s = strptime(s, '%Y-%m-%d')
        return True
    except:
        return False


def mkt(t):
    "将UTC+8 时间返回为UTC时间戳（忽略本地）"
    return mktime(t) - timezone - 8 * 3600


def tostr2(s=None):
    if s is None:
        return strftime('%Y-%m-%d %H:%M:%S', localtime())
    elif isinstance(s, struct_time):
        return strftime('%Y-%m-%d %H:%M:%S', s)
    else:
        return strftime('%Y-%m-%d %H:%M:%S', getDate(s))


def tostr3(i: int):
    "转换为适合srt的时间"
    return "%02d:%02d:%02d,%03d" % (floor(i / 3600), floor(i % 3600 / 60), floor(i % 60), floor(i * 1000 % 1000))


def tostr4(s):
    if isinstance(s, struct_time):
        return strftime('%Y-%m-%d', s)
    else:
        return strftime('%Y-%m-%d', getDate(s))


def tostr5(i: int):
    "转换为适合lrc的时间"
    return "%02d:%02d.%02d" % (floor(i / 60), floor(i % 60), floor(i * 100 % 100))


def tostr6(i: int):
    "时长转换"
    if i < 0:
        i = 0
    if i < 3600:
        return f"{floor(i / 60):02d}:{i % 60:02d}"
    return f"{floor(i / 3600):02d}:{floor(i % 3600 / 60):02d}:{floor(i % 60):02d}"


def comlrct(i: int, i2: int) -> int:
    "i大1，i2大-1，相等0"
    e = floor(i * 100)
    e2 = floor(i2 * 100)
    if e > e2:
        return 1
    elif e == e2:
        return 0
    else:
        return -1


if __name__ == '__main__':
    print(getNowDate())
