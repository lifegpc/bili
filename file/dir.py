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
from file.info import getinfox, printinfo
from os.path import abspath
from os import listdir
from file.str import width
from file import lan, la


def getinfod(filelist):
    "从listd获得的列表得到信息"
    j = 1
    ar = []
    for i in filelist:
        r = getinfox(i, j)
        if r != -1:
            j = j + 1
            ar.append(r)
    return ar


def printinfod(filelist):
    "打印整个filelist"
    m = maxwidth(filelist)
    j = 1
    print(lan['OUTPUT1'], end='')  # 序号\t文件名\t
    if la == "en":
        n = 12
    else:
        n = 8
    while m > n:
        print('\t', end='')
        m = m - 8
        j = j + 1
    print(lan['OUTPUT2'])  # 类型\t上次访问时间\t\t创建时间\t\t上次修改时间\t\t文件大小
    for i in filelist:
        printinfo(i, j * 8)


def listd(l='.'):  # noqa: E741
    '获取列表'
    d = listdir(l)
    r = []
    for i in d:
        if l != '.':  # noqa: E741
            r.append({'a': abspath('%s/%s' % (l, i)), 'f': i})
        else:
            r.append({'a': abspath(i), 'f': i})
    return r


def maxwidth(l):  # noqa: E741
    m = 0
    for i in l:
        n = width(i['f'])
        if n > m:
            m = n
    return m


def listc(l, s=0, e='True'):  # noqa: E741
    "截取listinfo中的一部分"
    if e == 'True':
        e = len(l)
    r = []
    j = 1
    for i in l[s:e]:
        i['x'] = j
        r.append(i)
        j = j + 1
    return r
