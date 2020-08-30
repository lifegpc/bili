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
import webui
from webui import gopt, loadset, pa, gettemplate
import sys
from lang import getdict, getlan
from re import search, I
import traceback

ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
se = loadset()
if se == -1 or se == -2:
    se = {}

un_safe_port_in_chrome = [1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 37, 42, 43, 53, 77, 79, 87, 95, 101, 102, 103, 104, 109, 110, 111, 113, 115, 117, 119, 123, 135,
                          139, 143, 179, 389, 427, 465, 512, 513, 514, 515, 526, 530, 531, 532, 540, 548, 556, 563, 587, 601, 636, 993, 995, 2049, 3659, 4045, 6000, 6665, 6666, 6667, 6668, 6669, 6697]

lan = None

urls = (
    r"/(index)?(\.html)?", "index",
    r"/translate/(.+)", "translate",
    r"/js/(.+)", "js",
    r"/css/(.+)", "css",
    r"/settings(\.html)?(/.+)?", "setting",
    r"/json/(.+)", "jsong",
    r"/login(\.html)?", "login",
    r"/font", "font",
    r"/video(.+)?", "video",
    r"/favicon.ico", "favicon",
    r"/about", "about"
)


def notfound():
    HTTP404 = gettemplate('HTTP404')
    return web.notfound(HTTP404(ip, se))


class mywebapp(web.application):
    def run(self, host: str = "127.0.0.1", port: int = 8080, *middleware):
        "重写方法以支持指定host和port"
        o_port = port
        pr = None
        if port == 0:
            port = 2
            pr = lan['ZEROPORT']
        while port in un_safe_port_in_chrome:
            port = port + 1
            pr = lan['UNSAFEPORT'].replace('<value1>', str(
                o_port)).replace('<value2>', str(port))
        if pr is not None:
            print(pr)
        func = self.wsgifunc(*middleware)
        bs = True
        while bs:
            bs = False
            try:
                return web.httpserver.runsimple(func, (host, port))
            except OSError as e:
                if len(e.args) < 1:
                    print(traceback.format_exc())
                else:
                    for i in e.args:
                        rs = search(r'\[winerror ([0-9]+)\]', i, I)
                        if rs is not None:
                            break
                    if rs is None:
                        for i in e.args:
                            rs = search(r'\[errno ([0-9]+)\]', i, I)
                            if rs is not None:
                                break
                        if rs is None:
                            print(traceback.format_exc())
                        else:
                            print(i)
                            pr = lan['UNAPORT'].replace('<value1>', str(port))
                            rn = int(rs.groups()[0])
                            if rn in [98]:
                                port = (port + 1) % 65536
                                if port == 0:
                                    port = 2  # 解决不识别端口0的情况
                                while port in un_safe_port_in_chrome:
                                    port = port + 1
                                print(pr.replace('<value2>', str(port)))
                                bs = True
                    else:
                        print(i)
                        pr = lan['UNAPORT'].replace('<value1>', str(port))
                        rn = int(rs.groups()[0])
                        if rn in [10013, 10048]:
                            port = (port + 1) % 65536
                            if port == 0:
                                port = 2  # 解决不识别端口0的情况
                            while port in un_safe_port_in_chrome:
                                port = port + 1
                            print(pr.replace('<value2>', str(port)))
                            bs = True


def main(ip: dict):
    app = mywebapp(urls, vars(webui))
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
        pa.https = True
    elif sslc is not None:
        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate=sslc, private_key=sslp)
        pa.https = True
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
    lan = getdict('startwebui', getlan(se, ip), "webui")
    main(ip)
