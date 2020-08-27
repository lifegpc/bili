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
from . import web, render, loadset, gopt, quote, mimetype, getEtag, getrange, checkrange, getcontentbyrange
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
            f = open('webuihtml/video.html', 'r', encoding='utf8')
            video2 = web.template.Template(f.read())
            f.close()
            yield video2(s, se, ip, se2, str)
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
                    f = open(fn, 'rb', 1024)
                    while f.readable():
                        yield f.read(1024 * 1024)
                    f.close()
                else:
                    ran2 = getrange(ran)
                    if not checkrange(ran2, fs):
                        web.HTTPError('416')
                        return '416 Range Not Satisfiable'
                    else:
                        f = open(fn, 'rb', 1024)
                        web.HTTPError('206')
                        yield getcontentbyrange(ran2, f)
        else:
            web.HTTPError('404')
            return render.HTTP404()
