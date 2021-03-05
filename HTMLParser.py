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
from html.parser import HTMLParser


class Myparser(HTMLParser):
    "解析B站HTML"
    script = 0
    videodata = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data):
        if self.script == 1 and data[0:24] == "window.__INITIAL_STATE__":
            self.videodata = data[25:len(data) - 122]


class Myparser2(HTMLParser):
    "解析B站HTML"
    script = 0
    videodata = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data):
        if self.script == 1 and data[0:19] == "window.__playinfo__":
            self.videodata = data[20:]


class Myparser3(HTMLParser):
    script = 0
    videodata = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data):
        if self.script == 1 and data[0:24] == "window.__INITIAL_STATE__":
            self.videodata = data[25:-122]


class AcfunParser(HTMLParser):
    script = 0
    videoInfo = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data: str):
        if self.script == 1:
            slist = data.splitlines(False)
            for i in slist:
                i = i.strip()
                if i.startswith("window.pageInfo"):
                    self.videoInfo = i[37:]
                    self.videoInfo = self.videoInfo.rstrip(";")


class AcfunBangumiParser(HTMLParser):
    script = 0
    bangumiData = ''
    bangumiList = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data: str):
        if self.script == 1:
            slist = data.splitlines(False)
            for i in slist:
                i = i.strip()
                if i.startswith("window.pageInfo"):
                    self.bangumiData = i[39:]
                    self.bangumiData = self.bangumiData.rstrip(";")
                if i.startswith("window.bangumiList"):
                    self.bangumiList = i[21:]
                    self.bangumiList = self.bangumiList.rstrip(";")


class NicoUserParser(HTMLParser):
    script = 0
    userData = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.script = 1
        else:
            self.script = 0

    def handle_data(self, data: str):
        if self.script == 1:
            slist = data.splitlines(False)
            for i in slist:
                i = i.strip()
                if i.startswith('user.'):
                    if self.userData != '':
                        self.userData += f'\n{i}'
                    else:
                        self.userData = i
