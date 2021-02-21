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
from regex import search, I


class InvalidInputEroor(Exception):
    def __init__(self):
        Exception.__init__(self, 'Input is invalid.')


class apic:
    _VALID_URI = r''
    _groupdict = {}
    _inp = ""

    def __init__(self, inp: str):
        "对uri进行处理"
        re = search(self._VALID_URI, inp, I)
        if re is None:
            raise InvalidInputEroor()
        self._inp = inp
        self._groupdict = re.groupdict()

    def _handle(self):
        "具体处理"
        return {'code': 0}
