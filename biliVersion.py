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
from os import system, popen
from os.path import exists
from re import search, I
import requests
from JSONParser import loadset
import sys
from lang import getlan, getdict
from command import gopt

lan = None
se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
lan = getdict('biliVersion', getlan(se, ip))

uri = "https://raw.githubusercontent.com/lifegpc/bili/master/version.txt"  # 检测更新用URI
backup_uri = "https://cdn.jsdelivr.net/gh/lifegpc/bili@master/version.txt"  # 备用URI


class UnknownVersionString(Exception):
    def __init__(self, s: str):
        self.s = s
        Exception.__init__(self, f"{lan['UNKNOWN_VER_STR']}{s}")


class version:
    def __init__(self, s: str):
        self.s = s
        r = search(
            r'v([0-9]+)\.([0-9]+)\.([0-9]+)(.([0-9]+))?([-\.]([0-9]+))?(-g([^-]+))?(-dirty)?', s, I)
        if r is not None:
            r = r.groups()
            self.v1 = int(r[0])
            self.v2 = int(r[1])
            self.v3 = int(r[2])
            self.v4 = 0
            if r[3]:
                self.v4 = self.v4 + int(r[4])
            if r[5]:
                self.v4 = self.v4 + int(r[6])
            self.sha = ""
            if r[7]:
                self.sha = r[8]
            self.dirty = False
            if r[9]:
                self.dirty = True
        else:
            raise UnknownVersionString(s)

    def tostr(self):
        s = f"{self.v1}.{self.v2}.{self.v3}"
        if self.v4 != 0:
            s = s + f".{self.v4}"
        if self.sha != "":
            if self.dirty:
                s = s + f"({self.sha},dirty)"
            else:
                s = s + f"({self.sha})"
        return s

    def compare(self, other):
        "当前版本高返回1，低返回-1，一样返回0"
        if self.v1 < other.v1:
            return -1
        elif self.v1 > other.v1:
            return 1
        if self.v2 < other.v2:
            return -1
        elif self.v2 > other.v2:
            return 1
        if self.v3 < other.v3:
            return -1
        elif self.v3 > other.v3:
            return 1
        if self.v4 < other.v4:
            return -1
        elif self.v4 > other.v4:
            return 1
        return 0


def checkver():
    git = False  # 是否存在git
    ver = None
    f = popen('git --version 2>&1', 'r', 10)
    o = f.read()
    f.close()
    if o.startswith('git version'):
        git = True
    if exists('.git/') and git:  # 优先从git仓库获取当前版本
        f = popen('git describe --long --dirty --tags', 'r', 10)
        ver = f.read()
        ver = ver.split('\n')[0]
        f.close()
    elif exists('version.txt'):
        f = open('version.txt', 'r', encoding='utf8')
        ver = f.read()
        ver = ver.split('\n')[0]
        f.close()
    try:
        if ver is not None:
            v = version(ver)
            print(f"{lan['CUR_VER']}{v.tostr()}")  # 当前版本：
            try:
                re = requests.get(uri, timeout=5)
            except:
                try:
                    re = requests.get(backup_uri, timeout=5)
                except:
                    print(lan['NETWORK_ERROR'])  # 网络错误：无法获取最新稳定版本字符串
                    return
            if re.ok:
                v2 = version(re.text.split('\n')[0])
                print(f"{lan['LATEST_STABLE_VER']}{v2.tostr()}")  # 最新稳定版本
                if v.compare(v2) == -1:
                    print(lan['GET_NEW_VER'])
            else:
                print(f"{lan['HTTP_STATUS_ERROR']}{re.status_code}")
    except UnknownVersionString as e:
        print(f"{lan['UNKNOWN_VER_STR']}{e.s}")


def getversion():
    """返回当前版本字符串
    如果无法获取当前版本，返回None"""
    ver = None
    f = popen('git --version 2>&1', 'r', 10)
    o = f.read()
    f.close()
    if o.startswith('git version'):
        git = True
    if exists('.git/') and git:  # 优先从git仓库获取当前版本
        f = popen('git describe --long --dirty --tags', 'r', 10)
        ver = f.read()
        ver = ver.split('\n')[0]
        f.close()
    elif exists('version.txt'):
        f = open('version.txt', 'r', encoding='utf8')
        ver = f.read()
        ver = ver.split('\n')[0]
        f.close()
    if ver is None:
        return None
    else:
        try:
            v = version(ver)
            return v.tostr()
        except:
            return None
