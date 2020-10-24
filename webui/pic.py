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
from . import logincheck2, web
from .api import new_Session
from urllib.parse import unquote_plus


class pic:
    "反代B站图片资源"

    def GET(self, t):
        h = web.cookies().get('section')
        if logincheck2(h):
            return '403 Forbidden'
        t2 = web.input().get('s')
        if t2 is not None:
            t = t2
        he = {'referer': unquote_plus(t)}
        et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        if et is not None:
            he['If-None-Match'] = et
        ra = web.ctx.env.get('HTTP_RANGE')
        if ra is not None:
            he['Range'] = ra
        r = new_Session()
        re = r.get(unquote_plus(t), headers=he)
        if re.ok:
            if 'Content-Type' in re.headers:
                web.header('Content-Type', re.headers['Content-Type'])
            else:
                web.header('Content-Type', 'image/jpeg')
            if et is not None and re.status_code == 304:
                web.HTTPError('304')
                return ''
            web.header('Content-Transfer-Encoding', 'BINARY')
            web.header('ETag', re.headers['ETag'])
            if ra is None:
                web.header('Content-Length', re.headers['Content-Length'])
                return re.content
            else:
                if re.status_code == 206:
                    web.HTTPError('206')
                    web.header('Content-Length', re.headers['Content-Length'])
                    web.header('Content-Range', re.headers['Content-Range'])
                    return re.content
                elif re.status_code == 200:
                    web.header('Content-Length', re.headers['Content-Length'])
                    return re.content
                else:
                    web.HTTPError(str(re.status_code))
                    return re.content
        else:
            web.HTTPError(str(re.status_code))
            return re.content
