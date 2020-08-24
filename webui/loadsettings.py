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
from json import loads, dumps
from os.path import exists
from os import remove


def loadset():
    "加载webui.json设置"
    try:
        obj = open('webui.json', mode='r')
    except:
        return -1
    try:
        obj.seek(0, 2)
        si = obj.tell()
        obj.seek(0, 0)
        s = obj.read(si)
        o = loads(s)
    except:
        return -2
    return o


def getdfset():
    "获取默认设置"
    o = {}
    o['lan'] = 'en'
    o['s'] = '127.0.0.1'
    o['p'] = '8080'
    return o


def saveset(d: dict):
    "保存设置到webui.json"
    try:
        if exists('webui.json'):
            remove('webui.json')
        obj = open('webui.json', mode='w')
    except:
        return -1
    try:
        obj.write(dumps(d))
        obj.close()
    except:
        return -2
    return 0
