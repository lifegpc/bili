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
from . import pa, sect, web, urlencode


def logincheck(h: str):
    "检查是否登录（返回302）"
    if pa.pas:
        read = sect.check(h)
        if not read:
            web.HTTPError('302', {'Location': "/login?" + urlencode(
                {"p": web.ctx.get('homepath') + web.ctx.get('fullpath')})})
            return True
    return False


def apilogincheck(h: str):
    "检查是否登录（啥都不返回）"
    if pa.pas:
        read = sect.check(h)
        if not read:
            return True
    return False


def logincheck2(h: str):
    "检查是否登录（返回403）"
    if pa.pas:
        read = sect.check(h)
        if not read:
            web.HTTPError('403')
            return True
    return False
