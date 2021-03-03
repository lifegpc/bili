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
from re import search
from os.path import isdir, isfile
import platform
import regex


def listf(filelist, lx=0, ft=["xml"]):
    "对listd获得列表进行过滤，文件夹都将保留"
    r = []
    for i in filelist:
        if isdir(i['f']):
            r.append(i)
            continue
        for j in ft:
            if lx == 0 or lx == 2:
                r2 = i['f'].rfind('.')
                if r2 > -1:
                    if i['f'][r2 + 1:] == j:
                        r.append(i)
                        break
                elif lx == 2:
                    r.append(i)
                    break
            else:
                if search(j, i['f']) is not None:
                    r.append(i)
                    break
    return r


def listfd(filelist):
    "对listd列表进行过滤，只保留文件夹"
    r = []
    for i in filelist:
        if isdir(i['f']):
            r.append(i)
    return r


def listff(filelist):
    "对listd列表进行过滤，只保留文件"
    r = []
    for i in filelist:
        if isfile(i['f']):
            r.append(i)
    return r


def filtern(filen: str):
    "对文件名进行去除不应该字符"
    filen = str(filen)
    re = regex.search(r'[^[:print:]]', filen)
    while re is not None:
        filen = filen.replace(re.group(), '_')
        re = regex.search(r'[^[:print:]]', filen)
    filen = filen.replace('/', '_')
    filen = filen.replace('\\', '_')
    if platform.system() == "Windows":
        filen = filen.replace(':', '_')
        filen = filen.replace('*', '_')
        filen = filen.replace('?', '_')
        filen = filen.replace('"', '_')
        filen = filen.replace('<', '_')
        filen = filen.replace('>', '_')
        filen = filen.replace('|', '_')
    elif platform.system() == "Linux":
        filen = filen.replace('!', '_')
        filen = filen.replace('$', '_')
        filen = filen.replace('"', '_')
    filen = filen.replace('\t', '_')
    while len(filen) > 0 and filen[0] == ' ':
        filen = filen[1:]
    return filen


def filterd(dir: str) -> str:
    "对文件夹去除不应该出现的字符"
    p = platform.system()
    if p == "Windows":
        f = ""
        r = search(r'^[A-Z]:[\\/]?', dir)
        if r is not None:
            f = r.group()
            dir = dir[len(f):]
            if f[-1] != "/" and f[-1] != '\\':
                f = f + '/'
            if dir == "":
                return f
    if dir[-1] != '/' and dir[-1] != '\\':
        dir = dir + '/'
    re = regex.search(r'[^[:print:]]', dir)
    while re is not None:
        dir = dir.replace(re.group(), '_')
        re = regex.search(r'[^[:print:]]', dir)
    if p == "Windows":
        dir = dir.replace(':', '_')
        dir = dir.replace('*', '_')
        dir = dir.replace('?', '_')
        dir = dir.replace('"', '_')
        dir = dir.replace('<', '_')
        dir = dir.replace('>', '_')
        dir = dir.replace('|', '_')
    elif p == "Linux":
        dir = dir.replace('!', '_')
        dir = dir.replace('$', '_')
        dir = dir.replace('"', '_')
    if p == 'Windows':
        dir = f + dir
    return dir
