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
from . import apic
from typing import List
from .rsa import apirsa
from .checklogin import checklogin
from .loginapi import getpubkey, captcha, login, qrgetloginurl, qrgetlogininfo, getcountrylist, getcaptchacombine, sendloginsms, loginwithsms, getpubkeyweb, loginwithuserpassweb

apil = [value for key, value in globals().items() if type(
    value) == type(apic) and issubclass(value, apic) and key != "apic"]


def getapilist() -> List[apic]:
    return apil
