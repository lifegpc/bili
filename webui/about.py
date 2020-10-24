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
from . import web, loadset, gopt, gettemplate
import sys
from biliVersion import getversion


ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}
ver = getversion()
if ver is None:
    ver2 = "bili"
ver2 = f"bili v{ver}"


class about:
    def GET(self, *t):
        abo = gettemplate('about')
        return abo(ip, se, ver)


def server_ver(handler):
    web.header('Server', ver2)
    return handler()
