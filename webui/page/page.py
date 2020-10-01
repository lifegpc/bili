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
from re import search, I
from urllib.parse import unquote_plus
from urllib3.exceptions import MaxRetryError, NewConnectionError

extractorl = getextractorlist()

ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}


class page:
    def GET(self, t):
        t = unquote_plus(t)
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
                try:
                    ses = requests.Session()
                    ses.trust_env = False
                    re = ses.head(t)
                    if 'Location' in re.headers:
                        re = self._extract(re.headers['Location'])
                        if re is not None:
                            r = re
                except requests.models.ConnectionError as e:
                    ok = False
                    if len(e.args) > 0:
                        rea: MaxRetryError = e.args[0]
                        if type(rea) == MaxRetryError:
                            rea2: NewConnectionError = rea.reason  # pylint: disable=E1101
                            if type(rea2) == NewConnectionError:
                                if len(rea2.args) > 0:
                                    rea3: str = rea2.args[0]
                                    if type(rea3) == str:
                                        rs = search(
                                            r'\[errno ([0-9]+)\]', rea3, I)
                                        if rs is not None:
                                            errno = int(rs.groups()[0])
                                            if errno == 11001:
                                                ok = True
                    if not ok:
                        r = {'code': -500, 'e': traceback.format_exc()}
                except:
                    r = {'code': -500, 'e': traceback.format_exc()}
            else:
                r = re
        r = dumps(r, ensure_ascii=False)
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
