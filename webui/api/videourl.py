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
from . import apic, new_Session
from .checklogin import logincheck
from .session import NotLoginError
from requests import Session
from time import time


last_checktime: int = None  # 上次检查登录时间


class videourl(apic):
    _r: Session = None

    def __init__(self, inp: str):
        apic.__init__(self, inp)
        global last_checktime
        if last_checktime is None or last_checktime < (time()-60):
            last_checktime = time()
            if not logincheck():
                raise NotLoginError()
        self._r = new_Session()
