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
from . import web, render, loadset, translate, getdfset, saveset, gopt, pa, logincheck
from lang import lan
from json import dumps, loads
import sys


ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])


class setting:
    def GET(self, *t):
        h = web.cookies().get('section')
        if logincheck(h):
            return ''
        se = loadset()
        if se == -1 or se == -2:
            se = {}
        return render.settings(t[1], lan, se, getdfset(), ip)

    def POST(self, *t):
        web.header('Content-Type', 'text/json; charset=utf-8')
        r = {}
        i = web.input()
        if 'type' in i and 'data' in i and int(i['type']) == 1:
            i2 = loads(i['data'])
            se = loadset()
            if se == -1 or se == -2:
                se = {}
            if 'pas' in se and 'pas' in i2 and i2['pas'] == 'c':
                i2['pas'] = se['pas']
            re = saveset(i2)
            r['code'] = re
        else:
            r['code'] = '-404'
        return dumps(r)