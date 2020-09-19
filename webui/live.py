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
from . import logincheck2, web, loadset
from .api import new_Session
from urllib.parse import unquote_plus
from requests.models import Response

se = loadset()
if se == -1 or se == -2:
    se = {}


class live:
    "反代B站视频资源"

    def GET(self, t):
        if not 'dclive' in se or se['dclive']:
            h = web.cookies().get('section')
            if logincheck2(h):
                return '403 Forbidden'
        t2 = web.input().get('s')
        if t2 is not None:
            t = t2
        t = unquote_plus(t)
        refer = web.input().get('r')
        contenttype = web.input().get('t')
        if refer is None:
            web.HTTPError('400')
            return 'No Referer.'
        refer = unquote_plus(refer)
        he = {'referer': refer}
        et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
        if et is not None:
            he['If-None-Match'] = et
        ra = web.ctx.env.get('HTTP_RANGE')
        if ra is not None:
            he['Range'] = ra
        r = new_Session()
        re = r.get(unquote_plus(t), headers=he, stream=True)
        if re.ok:
            if contenttype is not None:
                web.header('Content-Type', unquote_plus(contenttype))
            elif 'Content-Type' in re.headers:
                web.header('Content-Type', re.headers['Content-Type'])
            else:
                web.header('Content-Type', 'video/mp4')
            if et is not None and re.status_code == 304:
                web.HTTPError('304')
                return ''
            web.header('Content-Transfer-Encoding', 'BINARY')
            if 'ETag' in re.headers:
                web.header('ETag', re.headers['ETag'])
            if ra is None:
                if 'Content-Length' in re.headers:
                    web.header('Content-Length', re.headers['Content-Length'])
                return self.returnc(re)
            else:
                if re.status_code == 206:
                    web.HTTPError('206')
                    web.header('Content-Length', re.headers['Content-Length'])
                    web.header('Content-Range', re.headers['Content-Range'])
                    return self.returnc(re)
                elif re.status_code == 200:
                    if 'Content-Length' in re.headers:
                        web.header('Content-Length',
                                   re.headers['Content-Length'])
                    return self.returnc(re)
                else:
                    web.HTTPError(str(re.status_code))
                    return self.returnc(re)
        else:
            web.HTTPError(str(re.status_code))
            return self.returnc(re)

    def returnc(self, re: Response):
        for c in re.iter_content(chunk_size=1024):
            if c:
                yield c
        re.close()
