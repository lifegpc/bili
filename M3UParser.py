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
from typing import List
from urllib.parse import urljoin


def parseSimpleMasterM3U(data: str, base: str) -> List[str]:
    r = []
    li = data.splitlines(False)
    for s in li:
        s = s.strip()
        if s.startswith('#'):
            continue
        if len(s) == 0:
            continue
        r.append(urljoin(base, s))
    return r
