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
import web
from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter
import os
from webui import index, gopt, translate, js, render, css
import sys

urls = (
    r"/(index)?(.html)?", "index",
    r"/translate/(.+)", "translate",
    r"/js/(.+)", "js",
    r"/css/(.+)", "css"
)


def notfound():
    return web.notfound(render.HTTP404())


class mywebapp(web.application):
    def run(self, host: str = "127.0.0.1", port: int = 8080, *middleware):
        "重写方法以支持指定host和port"
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (host, port))


def main(ip: dict):
    app = mywebapp(urls, globals())
    app.notfound = notfound
    port = 8080
    if 'p' in ip:
        port = ip['p']
    host = '127.0.0.1'
    if 's' in ip:
        host = ip['s']
    if 'sslc' in ip:
        if 'sslcc' in ip:
            HTTPServer.ssl_adapter = BuiltinSSLAdapter(
                certificate=ip['sslc'], private_key=ip['sslp'], certificate_chain=ip['sslcc'])
        else:
            HTTPServer.ssl_adapter = BuiltinSSLAdapter(
                certificate=ip['sslc'], private_key=ip['sslp'])
    app.run(host, port)


if __name__ == "__main__":
    ip = {}
    if len(sys.argv) > 1:
        ip = gopt(sys.argv[1:])
    main(ip)
