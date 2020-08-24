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
from . import web, loadset, gopt
from lang import getlan, getdict
import sys
from json import dumps

se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])


class translate:
    def GET(self, n: str):
        web.header('Content-Type', 'text/json; charset=utf-8')
        l = n.split('.', 1)
        r = {}
        if len(l) == 1:
            la = getdict(l[0], getlan(se, ip))
        else:
            la = getdict(l[1], getlan(se, ip), l[0])
        if la == -1:
            r['code'] = -1
        else:
            r['code'] = 0
            r['dict'] = la
        return dumps(r)
