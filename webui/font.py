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
from . import web, getEtag, logincheck2, getrange, checkrange, getcontentbyrange
from os.path import exists, getsize
from file import spfn

mimetype = {'otf': 'font/otf', 'ttf': 'font/ttf',
            'woff': 'font/woff', 'woff2': 'font/woff'}


class font:
    def GET(self):
        h = web.cookies().get('section')
        if logincheck2(h):
            yield '403 Forbidden'
        t = web.input().get('l')
        if not exists(t):
            web.HTTPError('404')
            yield '404 Not Found'
        elif spfn(t)[1].lower() in mimetype:
            mime = mimetype[spfn(t)[1].lower()]
            web.header('Content-type', mime)
            et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            et2 = getEtag(t)
            if et == et2:
                web.HTTPError('304')
                yield ''
            else:
                web.header('Etag', et2)
                web.header('Content-Transfer-Encoding', 'BINARY')
                fs = getsize(t)
                ran = web.ctx.env.get('HTTP_RANGE')
                if ran is None:
                    web.header('Content-Length', str(fs))
                    f = open(t, 'rb', 1024)
                    while f.readable():
                        yield f.read(1024 * 1024)
                    f.close()
                else:
                    ran2 = getrange(ran)
                    if not checkrange(ran2, fs):
                        web.HTTPError('416')
                        yield '416 Range Not Satisfiable'
                    else:
                        f = open(t, 'rb', 1024)
                        web.HTTPError('206')
                        yield getcontentbyrange(ran2, f)
        else:
            web.HTTPError('400')
            yield '400 Bad Request'
