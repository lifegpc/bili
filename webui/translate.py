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
from . import web, loadset, gopt, getlanEtag, getacceptlanguage
from lang import getlan, getdict, lan
import sys
from json import dumps

se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])


def islanin(l:str) -> str:
    """检查是否存在该语种
    是返回字符串，否返回None"""
    li = l.split('-')
    if li[0] == 'zh':
        te = 'zh_CN'
    else:
        te = li[0]
    if te in lan:
        return te
    return None


class translate:
    def GET(self, n: str):
        web.header('Content-Type', 'text/json; charset=utf-8')
        et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        l = n.split('.', 1)
        la2 = None
        hl = web.input().get('hl')
        if hl is not None and hl in lan:
            la2 = hl
        elif 'lan' in ip or 'lan' in se:
            la2 = getlan(se, ip)
        acl = getacceptlanguage(web.ctx.env.get('HTTP_ACCEPT_LANGUAGE'))
        if la2 is None and acl is not None:
            for q in acl.keys():
                acl2 = acl[q]
                ia = False
                for la3 in acl2:
                    la4 = islanin(la3)
                    if la4 is not None:
                        la2 = la4
                        ia = True
                        break
                if ia:
                    break
        if la2 is None:
            la2 = getlan(se, ip)
        if len(l) == 1:
            et2 = getlanEtag(l[0], la2)
        else:
            et2 = getlanEtag(l[1], la2, l[0])
        if et == et2 and et2 is not None:
            web.HTTPError('304')
            t = ''
        else:
            if et2 is not None:
                web.header('Etag', et2)
            r = {}
            if len(l) == 1:
                la = getdict(l[0], la2)
            else:
                la = getdict(l[1], la2, l[0])
            if la == -1:
                r['code'] = -1
            else:
                r['code'] = 0
                r['dict'] = la
            t = dumps(r)
        return t

    def resetse(self):
        global se
        se = loadset()
        if se == -1 or se == -2:
            se = {}
