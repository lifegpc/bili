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
from . import apic
from ..page.extractorlist import getextractorlist
from urllib.parse import unquote_plus
from .checklogin import logincheck
import requests
from re import search, I
from . import InvalidInputEroor
import traceback
from urllib3.exceptions import MaxRetryError, NewConnectionError

extractorl = getextractorlist()


class infoextractor(apic):
    _VALID_URI = r'^infoextractor/(?P<inp>.+)$'

    def _handle(self):
        inp = unquote_plus(self._groupdict['inp'])
        r = {'code': -404}
        if not logincheck():
            r = {'code': -1}
        else:
            re = self._extract(inp)
            if re is None:
                re = search(r"[^:]+://", inp)
                if re is None:
                    inp = "https://"+inp
                try:
                    ses = requests.Session()
                    ses.trust_env = False
                    re = ses.head(inp)
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
        return {'code': 0, 're': r}

    def _extract(self, inp):
        for i in extractorl:
            try:
                e = i(inp)
                return e._handle()
            except InvalidInputEroor:
                pass
            except Exception:
                return {'code': -500, 'e': traceback.format_exc()}
        return None
