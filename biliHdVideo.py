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
from requests import Session
from inspect import currentframe


class HDVideoParser:

    def __init__(self, r: Session, d: dict, logg=None):
        self.r = r
        self.d = d
        self.logg = logg

    def parser(self):
        uri = f"https://api.bilibili.com/x/stein/edgeinfo_v2?bvid={self.d['bvid']}&graph_version={self.d['gv']}&platform=pc&portal=0&screen=0&buvid={self.r.cookies.get('buvid3')}"
        if self.logg:
            self.logg.write(f"GET {uri}", currentframe(),
                            "HD VIDEO GET EDGEINFO")
        re = self.r.get(uri)
        re.encoding = 'utf8'
        if self.logg:
            self.logg.write(f"status = {re.status_code}\n{re.text}", currentframe(
            ), "HD VIDEO GET EDGEINFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            return -1
        pages = callen(re)
        if self.logg:
            self.logg.write(f"pages = {pages}",
                            currentframe(), "HD Video Var5")
        if pages == self.d['videos']:
            e = []
            p = []
            k = 1
            for i in re['data']['story_list']:
                if not i['cid'] in p:
                    p.append(i['cid'])
                    e.append({'page': k, 'part': i['title'], 'cid': i['cid']})
                    k = k + 1
            self.d['page'] = e
            if self.logg:
                self.logg.write(f"e = {e}", currentframe(), "HD Video Var6")
            return 0
        self.edge_list = []
        q = []
        if 'questions' in re['data']['edges']:
            q = re['data']['edges']['questions']
        if self.logg:
            self.logg.write(f"q = {q}", currentframe(), "HD VIDEO VAR1")
        self.page_list = []
        self.addninfo(re)
        if self.logg:
            self.logg.write(
                f"self.page_list = {self.page_list}", currentframe(), "HD VIDEO VAR2")
        for a in q:
            for b in a['choices']:
                read = self.getnch(b)
                if self.logg:
                    self.logg.write(f"read = {read}", currentframe(
                    ), "HD Video Get More EdgeInfo Return")
                if read == -1:
                    return -1
        self.d['page'] = self.page_list
        return 0

    def addninfo(self, re: dict):
        d = re['data']
        e = {}
        e['page'] = len(self.page_list)+1
        e['part'] = d['title']
        i = d['edge_id']
        for k in d['story_list']:
            if k['edge_id'] == i:
                e['cid'] = k['cid']
                if infoqc(e['cid'], self.page_list):  # 发现重复，跳过
                    return
                self.page_list.append(e)
                break

    def getnch(self, b: dict):
        if b['id'] in self.edge_list:
            return 0
        self.edge_list.append(b['id'])
        uri = f"https://api.bilibili.com/x/stein/edgeinfo_v2?bvid={self.d['bvid']}&edge_id={b['id']}&graph_version={self.d['gv']}&platform=pc&portal=0&screen=0&buvid={self.r.cookies.get('buvid3')}&choice={b['native_action']}"
        if self.logg:
            self.logg.write(f"GET {uri}", currentframe(),
                            "HD VIDEO GET EDGEINFO")
        re = self.r.get(uri)
        re.encoding = 'utf8'
        if self.logg:
            self.logg.write(f"status = {re.status_code}\n{re.text}", currentframe(
            ), "HD Video Get EdgeInfo Result")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            return -1
        q = []
        if 'questions' in re['data']['edges']:
            q = re['data']['edges']['questions']
        if self.logg:
            self.logg.write(f"q = {q}", currentframe(), "HD Video Var3")
        self.addninfo(re)
        if self.logg:
            self.logg.write(
                f"self.page_list = {self.page_list}", currentframe(), "HD Video Var4")
        for a in q:
            for b in a['choices']:
                read = self.getnch(b)
                if self.logg:
                    self.logg.write(f"read = {read}", currentframe(
                    ), "HD Video Get More EdgeInfo Return 2")
            if read == -1:
                return -1
        return 0


def infoqc(c: int, l: list):
    "对互动视频列表进行去重"
    for i in l:
        if i['cid'] == c:
            return True
    return False


def callen(re: dict) -> int:
    "计算story_list长度"
    if not 'data' in re or not 'story_list' in re['data']:
        return 0
    t = re['data']['story_list']
    p = []
    for i in t:
        if not i['cid'] in p:
            p.append(i['cid'])
    return len(p)
