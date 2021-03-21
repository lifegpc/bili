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
from typing import Tuple, List


HTMLAttrs = List[Tuple[str, str]]


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


class NicoVideoInfoParser(HTMLParser):
    apiData = ''

    def handle_starttag(self, tag, attrs: HTMLAttrs):
        if tag == 'div':
            eid = ''
            for t in attrs:
                if t[0] == 'id':
                    eid = t[1]
                    break
            if eid == 'js-initial-watch-data':
                for t in attrs:
                    if t[0] == 'data-api-data':
                        self.apiData = t[1]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


class NicoDescriptionParser(HTMLParser):
    data = ''
    style = False
    deepdata = []
    deepLevel = 0

    def handle_data(self, data: str):
        if not self.style and self.deepLevel == 0:
            self.data += data
        elif self.deepLevel > 0:
            self.deepdata[-1]["content"] += data

    def handle_starttag(self, tag: str, attrs: HTMLAttrs):
        if tag == "br":
            self.data += "\n"
        if tag == 'style':
            self.style = True
        if tag == 'a':
            self.deepLevel += 1
            t = {"type": "link", "href": "", "content": ""}
            for a in attrs:
                if a[0] == 'href':
                    t['href'] = a[1]
            self.deepdata.append(t)

    def handle_endtag(self, tag: str):
        if tag == 'style':
            self.style = False
        if tag == 'a':
            t = self.deepdata.pop()
            c = t['href'] if t["href"] == t["content"] or t["content"] == "" else f"{t['content']}({t['href']})"
            if self.deepLevel == 1:
                self.data += c
            elif self.deepLevel > 1:
                self.deepdata[-1]["content"] += c
            self.deepLevel -= 1

    def handle_startendtag(self, tag: str, attrs: HTMLAttrs):
        if tag == 'style':
            return
        self.handle_starttag(tag, attrs)
        if tag == 'href':
            self.handle_endtag('href')


class NicoLiveInfoParser(HTMLParser):
    data = ''

    def handle_starttag(self, tag, attrs: HTMLAttrs):
        if tag == 'script':
            eid = ''
            for t in attrs:
                if t[0] == 'id':
                    eid = t[1]
                    break
            if eid == 'embedded-data':
                for t in attrs:
                    if t[0] == 'data-props':
                        self.data = t[1]

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
