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
from requests import Session
from .. import http_headers
from JSONParser import loadcookie, loadset, getset


se = loadset()
if se == -1 or se == -2:
    se = {}


class NotLoginError(Exception):
    def __init__(self):
        Exception.__init__(self, "You are not login in.")


def new_Session(cookies: bool = True):
    "新建新会话，cookies为True则包含cookies"
    r = Session()
    r.headers.update(http_headers)
    if cookies:
        read = loadcookie(r)
        if read != 0:
            raise NotLoginError()
    if getset(se, 'te') == False:
        r.trust_env = False
    return r
