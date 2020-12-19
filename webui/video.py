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
from . import web, loadset, gopt, quote, mimetype, getEtag, getrange, checkrange, getcontentbyrange, gettemplate, DashRange, logincheck
from JSONParser import loadset as loadset2
import sys
from os.path import exists, isdir, isfile, getsize
from file import spfn

ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}
se2 = loadset2()
if se2 == -1 or se2 == -2:
    se2 = {}


class video:
    def GET(self, *t):
        if 'dcvideo' in se and se['dcvideo']:
            h = web.cookies().get('section')
            if logincheck(h):
                return ''
        s: str = t[0]
        if s == None:
            s = ''
        o = 'Download/'
        if 'o' in se2:
            o = se2['o']
        if exists(o + s[1:]) and isdir(o + s[1:]):
            if not s.endswith('/'):
                web.HTTPError('301', {'location': quote(web.ctx.get(
                    'homepath') + web.ctx.get('path') + '/') + web.ctx.get('query')})
                return ''
            web.header('Content-Type', 'text/html; charset=utf-8')
            video2 = gettemplate('video')
            return video2(s, se, ip, se2, str)
        elif exists(o + s[1:]) and isfile(o + s[1:]):
            fn = o + s[1:]
            mime = 'application/octet-stream'
            ex = spfn(fn)[1]
            if ex.lower() in mimetype:
                mime = mimetype[ex.lower()]
            web.header('Content-type', mime)
            et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            et2 = getEtag(fn)
            if et == et2:
                web.HTTPError('304')
                return ''
            else:
                web.header('Etag', et2)
                web.header('Content-Transfer-Encoding', 'BINARY')
                fs = getsize(fn)
                ran = web.ctx.env.get('HTTP_RANGE')
                if ran is None:
                    web.header('Content-Length', str(fs))
                    return getcontentbyrange(None, fn)
                else:
                    ran2 = getrange(ran)
                    if not checkrange(ran2, fs):
                        web.HTTPError('416')
                        return '416 Range Not Satisfiable'
                    else:
                        web.header('Content-Range', DashRange(ran2, fs))
                        web.HTTPError('206')
                        return getcontentbyrange(ran2, fn)
        else:
            web.HTTPError('404')
            HTTP404 = gettemplate('HTTP404')
            return HTTP404(ip, se)
