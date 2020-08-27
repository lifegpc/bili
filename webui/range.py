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
from re import search, I
from typing import List, Tuple, IO

Range = List[Tuple[int, int]]


def sortrange(l: Range):
    "排序getrange输出的列表"
    le = len(l)
    for i in range(le - 1):
        for j in range(le - 1 - i):
            if l[j][0] > l[j + 1][0]:
                t = l[j]
                l[j] = l[j + 1]
                l[j + 1] = t


def getrange(s: str) -> Range:
    """根据HTTP_RANGE头部返回内容
    为空是返回None"""
    t = s.strip()
    rs = search(r'^bytes=(.+)', t, I)
    if rs is not None:
        s2 = rs.groups()[0].strip()
        rs = search(r'^([0-9]+)-$', s2, I)
        if rs is not None:
            return [(int(rs.groups()[0]), None)]
        rs = search(r'^-([0-9]+)', s2, I)
        if rs is not None:
            return [(-int(rs.groups()[0]), None)]
        rs = search(r'^([0-9]+)-([0-9]+)$', s2, I)
        if rs is not None:
            t = rs.groups()
            if int(t[0]) <= int(t[1]):
                return [(int(t[0]), int(t[1]))]
            else:
                return None
        li = s2.split(',')
        r: Range = []
        for i in li:
            s3 = i.strip()
            rs = search(r'^([0-9]+)-([0-9]+)$', s3, I)
            if rs is None:
                return None
            t = rs.groups()
            if int(t[0]) <= int(t[1]):
                r.append((int(t[0]), int(t[1])))
            else:
                return None
        sortrange(r)
        le = len(r)
        if le == 0:
            return None
        r2: Range = []
        mi = r[0][0]
        ma = r[0][1]
        for i in range(le - 1):
            if r[i][1] < r[i+1][0]:
                r2.append((mi, ma))
                if i+1 < le:
                    mi = r[i+1][0]
                    ma = r[i+1][1]
            else:
                ma = max(r[i][1], r[i+1][1])
        r2.append((mi, ma))
        return r2
    return None


def checkrange(r: Range, l: int):
    "根据文件长度判断Range是否合法"
    if r is None:
        return False
    if len(r) == 1 and r[0][1] is None:
        if abs(r[0][0]) <= l:
            return True
        return False
    else:
        if r[len(r)-1][1] <= l:
            return True
        else:
            return False


def getcontentbyrange(r: Range, f: IO):
    "传输前需将Content-Transfer-Encoding设置为BINARY"
    if r is None or len(r) == 0:
        f.seek(0, 0)
        while f.readable():
            yield f.read(1024*1024)
        f.close()
    if len(r) == 1 and r[0][1] is None:
        if r[0][0] > 0:
            f.seek(r[0][0]-1, 0)
            while f.readable():
                yield f.read(1024 * 1024)
            f.close()
        else:
            f.seek(r[0][0], 2)
            while f.readable():
                yield f.read(1024 * 1024)
            f.close()
    else:
        for i in r:
            f.seek(i[0]-1, 0)
            l = f.tell()
            while l < i[1]:
                le = min(i[1] - l, 1024 * 1024)
                yield f.read(le)
                l = f.tell()
        f.close()
