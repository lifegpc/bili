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
from re import search


def Filter(s, l):  # noqa: E741
    "过滤弹幕"
    for i in l:
        if i['e'] == 'true':
            if i['t'] == 't':
                if s['t'].find(i['w']) > -1:
                    return True
            elif i['t'] == 'r':
                if search(i['w'], s['t']) is not None:
                    return True
            elif i['t'] == 'u':
                if i['w'] == s['si']:
                    return True
    return False
