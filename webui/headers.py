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
from re import search, I
from typing import List, Tuple

Headers = List[Tuple[str, str]]
ContentType = Tuple[str, str, str]
mimetype = {"xml": "text/xml", "txt": "text/plain", "png": "image/png", "mp4": "video/mp4",
            "m4a": "audio/mp4", "mkv": "video/mp4", "jpeg": "image/jpeg", "jpg": "image/jpeg", "webp": "image/webp"}


def getstatus(s: str) -> int:
    "返回状态码"
    t = s.strip()
    rs = search(r'^([0-9]+)', t)
    if rs is not None:
        return int(rs.groups()[0])
    return -1


def getheader(h: Headers, s: str) -> str:
    "在Headers寻找某个值"
    for i in h:
        if i[0].lower() == s.lower():
            return i[1]
    return None


def getcontenttype(s: str) -> ContentType:
    "获取Content-Type，分别为mimetype,charset,boundary"
    t = s.strip()
    rs = search(r'^([^;]+);( )*charset=(.*)', t, I)
    if rs is not None:
        t = rs.groups()
        return (t[0], t[2], None)
    rs = search(r'^([^;]+);( )*boundary=(.*)', t, I)
    if rs is not None:
        t = rs.groups()
        return (t[0], None, t[2])
