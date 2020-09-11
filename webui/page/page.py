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
import web
from .. import logincheck, gettemplate, gopt, loadset
from . import getextractorlist, InvalidInputEroor
from ..api.checklogin import logincheck as bililogincheck
import traceback
from json import dumps
import sys
import requests
from re import search

extractorl = getextractorlist()

ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}


class page:
    def GET(self, t):
        h = web.cookies().get('section')
        if logincheck(h):
            return ''
        r = {'code': -404}
        if not bililogincheck():
            r = {'code': -1}  # 未登录
        else:
            re = self._extract(t)
            if re is None:
                re = search(r"[^:]+://", t)
                if re is None:
                    t = "https://"+t
                re = requests.head(t)
                if 'Location' in re.headers :
                    re = self._extract(re.headers['Location'])
                    if re is not None:
                        r = re
            else:
                r = re
        r = dumps(r)
        pag = gettemplate('page')
        return pag(ip, se, r)

    def _extract(self, t):
        for i in extractorl:
            try:
                e = i(t)
                return e._handle()
            except InvalidInputEroor:
                pass
            except Exception:
                return {'code': -500, 'e': traceback.format_exc()}
        return None
