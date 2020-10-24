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
from . import web, getEtag
from os.path import exists


class js:
    def GET(self, n):
        web.header('Content-Type', 'application/javascript; charset=utf-8')
        if exists(f'webuihtml/js/{n}'):
            et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            et2 = getEtag(f'webuihtml/js/{n}')
            if et == et2 and et2 is not None:
                web.HTTPError('304')
                t = ''
            else:
                web.header('Etag', et2)
                f = open(f'webuihtml/js/{n}', 'r', encoding='utf8')
                t = f.read()
                f.close()
            return t
        elif exists(f'webuihtml/js(origin)/{n}'):
            et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            et2 = getEtag(f'webuihtml/js(origin)/{n}')
            if et == et2 and et2 is not None:
                web.HTTPError('304')
                t = ''
            else:
                web.header('Etag', et2)
                f = open(f'webuihtml/js(origin)/{n}', 'r', encoding='utf8')
                t = f.read()
                f.close()
            return t
        elif exists(f'webuihtml/jso/{n}'):
            et = web.ctx.env.get('HTTP_IF_NONE_MATCH')
            et2 = getEtag(f'webuihtml/jso/{n}')
            if et == et2 and et2 is not None:
                web.HTTPError('304')
                t = ''
            else:
                web.header('Etag', et2)
                f = open(f'webuihtml/jso/{n}', 'r', encoding='utf8')
                t = f.read()
                f.close()
            return t
        else:
            web.notfound()
            return ''
