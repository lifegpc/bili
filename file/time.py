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
from time import strftime,localtime
def ttos(tm) :
    "将时间戳转换为字符串（当地时间）"
    if tm=='N/A':
        return 'N/A'
    elif tm>=0:
        return strftime('%Y-%m-%d %H:%M:%S',localtime(tm))
    else :
        return str(tm)