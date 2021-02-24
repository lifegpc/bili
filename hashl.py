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
import hashlib
from zlib import crc32 as crc32f


def sha256(s):
    t = str(s)
    h = hashlib.sha256()
    h.update(t.encode('utf8'))
    return h.hexdigest()


def md5(s):
    t = str(s)
    h = hashlib.md5()
    h.update(t.encode('utf8'))
    return h.hexdigest()


def crc32(s):
    t = str(s)
    te = hex(crc32f(t.encode('utf8')))[2:]
    return '0' * (8 - len(te)) + te
