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
from . import apic
from ..page.extractorlist import getextractorlist
from urllib.parse import unquote_plus
from .checklogin import logincheck
import requests
from re import search
from . import InvalidInputEroor
import traceback

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
                re = requests.head(inp)
                if 'Location' in re.headers:
                    re = self._extract(re.headers['Location'])
                    if re is not None:
                        r = re
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
