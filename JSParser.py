# (C) 2019-2021 lifegpc
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
from js2py import eval_js
from HTMLParser import NicoUserParser
from Logger import Logger
from inspect import currentframe
from traceback import format_exc


def toDict(obj) -> dict:
    r = {}
    for i in obj:
        r[i] = obj[i]
    return r


def getNicoUser(p, logg: Logger = None) -> dict:
    data = None
    if isinstance(p, str):
        data = p
    elif isinstance(p, NicoUserParser):
        data = p.userData
    if data is None or data == '':
        return None
    try:
        t = 'function(){var user={};' + data + ';return user;}'
        f = eval_js(t)
        return toDict(f())
    except:
        if logg:
            logg.write(format_exc(), currentframe(), "Get Niconico User Data")
        return None
