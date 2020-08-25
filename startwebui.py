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
from webui import index, gopt, translate, js, render, css, setting, loadset, pa, jsong, login
import sys
from lang import getdict, getlan
lan = None

urls = (
    r"/(index)?(\.html)?", "index",
    r"/translate/(.+)", "translate",
    r"/js/(.+)", "js",
    r"/css/(.+)", "css",
    r"/settings(\.html)?(/.+)?", "setting",
    r"/json/(.+)", "jsong",
    r"/login(\.html)?", "login"
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
    global se
    port = 8080
    if 'p' in se:
        port = int(se['p'])
    if 'p' in ip:
        port = ip['p']
    host = '127.0.0.1'
    if 's' in se:
        host = se['s']
    if 's' in ip:
        host = ip['s']
    sslc = None
    sslp = None
    sslcc = None
    if 'sslc' in se and 'sslp' in se:
        sslc = se['sslc']
        sslp = se['sslp']
        if 'sslcc' in se:
            sslcc = se['sslcc']
    if 'sslc' in ip:
        sslc = ip['sslc']
        sslp = ip['sslp']
    if (sslcc is not None or 'sslc' in ip) and 'sslcc' in ip:
        sslcc = se['sslcc']
    if sslc is not None and sslcc is not None:
        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate=sslc, private_key=sslp, certificate_chain=sslcc)
    elif sslc is not None:
        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate=sslc, private_key=sslp)
    if 'pas' in se:
        pa.pas = True
        re = pa.setpassword(se['pas'])
        if re == -1:
            print(lan['INVALPAS'])
            return -1
    if 'pas' in ip:
        pa.pas = True
        re = pa.setpassword(ip['pas'])
        if re == -1:
            print(lan['INVALPAS'])
            return -1
    app.run(host, port)


if __name__ == "__main__":
    ip = {}
    if len(sys.argv) > 1:
        ip = gopt(sys.argv[1:])
    se = loadset()
    if se == -1 or se == -2:
        se = {}
    lan = getdict('startwebui', getlan(se, ip), "webui")
    main(ip)
