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
from . import render, web, loadset, gopt, sect, pa
import sys
from json import dumps


ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}


class login:
    def GET(self, *t):
        return render.login(ip, se)

    def POST(self, *t):
        web.header('Content-Type', 'text/json; charset=utf-8')
        r = {}
        i = web.input()
        ip = web.ctx.get('ip')
        if 'p' in i and pa.pas:
            h = sect.login(i['p'], ip)
            if h is not None:
                web.setcookie('section', h, 3600 * 24 * 30, secure=pa.https,
                              httponly=True, path='/', samesite="Strict")
                r['code'] = 0
            else:
                r['code'] = -1
        elif not pa.pas:
            r['code'] = -2
        else:
            r['code'] = -1
        return dumps(r)
