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
from . import web, gettemplate, logincheck, getEtag, gopt, loadset
import sys



ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}


class dealwithcapcha:
    def GET(self, *t):
        h = web.cookies().get('section')
        if logincheck(h):
            return ''
        et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        et2 = getEtag(f'webuihtml/dealwithcapcha.html')
        if et == et2 and et2 is not None:
            web.HTTPError('304')
            t = ''
        else:
            web.header('Etag', et2)
            dea = gettemplate('dealwithcapcha')
            return dea(se, ip)
