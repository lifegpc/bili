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
from re import search, I


def filterLRC(s: str) -> (str, int):
    "标准化LRC（鬼知道BiliBili还可能会出现不标准的LRC）"
    t = s.splitlines()
    r = ""
    n = 0
    for i in t:
        if i == "":
            continue
        a = search(r'^\[([^\]]+)\]', i, I)
        if a is None:
            r = r + '\n' + i
        else:
            b = a.groups()[0]  # 时间戳
            c = search(r':(\d{2,3})$', b, I)  # 匹配末尾的:000或:00
            if c is None:
                r = r + '\n' + i
            else:
                d = i[:c.start()+1] + "." + c.groups()[0] + \
                    i[c.end()+1:]  # 替换为.00或.000
                r = r + '\n' + d
                n = n + 1
    while r.startswith('\n') and len(r) > 0:
        r = r[1:]
    return r, n
