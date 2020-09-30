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
from .extractor import extractor
from ..api.checklogin import logincheck
from HTMLParser import Myparser
from JSONParser import Myparser as JMyparser
from re import search, I
import json
import traceback


class normal(extractor):
    _VALID_URI = r'^(av)?(?P<av>\d+)$|^(?P<bv>BV\w+)$|^([^:]+://)?(www\.)?(m\.)?bilibili\.com/video/(av(?P<av>\d+)|(?P<bv>BV\w+)).*$|^([^:]+://)?(www\.)?b23\.tv/(av(?P<av>\d+)|(?P<bv>BV\w+)).*$'
    r: dict = {}

    def _handle(self):
        self._addcookies()
        self.r = {'code': 0, 'type': self.__class__.__name__}
        aid = self._groupdict['av']
        bvid = self._groupdict['bv']
        if aid is None:
            url = f'https://www.bilibili.com/video/{bvid}'
        else:
            url = f'https://www.bilibili.com/video/av{aid}'
        re = self._r.get(url)
        parser = Myparser()
        parser.feed(re.text)
        try:
            data = json.loads(parser.videodata, strict=False)
            if 'error' in data and 'code' in data['error'] and 'message' in data['error']:
                self.r['data'] = {'code': -1, 're': data['error']}
                return self.r
            data = JMyparser(parser.videodata)
            hd = False  # 互动视频
            uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['page'][0]['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={self._r.cookies.get('buvid3')}"
            re = self._r.get(uri, headers={'referer': url})
            re.encoding = 'utf8'
            rs = search(r"<interaction>(.+)</interaction>", re.text, I)
            if rs is not None:
                rs = rs.groups()[0]
                rs = json.loads(rs)
                data['gv'] = rs['graph_version']
                hd = True
            if hd:
                read = self._gethdinfo(data)
                if read == -1:
                    return self.r
            self.r['data'] = {'code': 0, 'data': data}
            r2 = logincheck(True)[1]
            if r2 is None:
                self.r = {'code': -1}
            else:
                if 'vipStatus' in r2:
                    self.r['vip'] = r2['vipStatus']
                else:
                    self.r['vip'] = 0
        except Exception:
            if aid is None:
                uri = f"https://api.bilibili.com/x/web-interface/view/detail?bvid={bvid}&aid=&jsonp=jsonp"
            else:
                uri = f"https://api.bilibili.com/x/web-interface/view/detail?bvid=&aid={aid}&jsonp=jsonp"
            re = self._r.get(uri)
            re.encoding = 'utf8'
            re = re.json()
            if re['code'] != 0:
                self.r['data'] = {'code': -1, 're': re}
                return self.r
            if 'data' in re and 'View' in re['data'] and 'redirect_url' in re['data']['View']:
                self.r['type'] = 'redirect'
                self.r['url'] = re['data']['View']['redirect_url']
                return self.r
            self.r['code'] = -500
            self.r['e'] = traceback.format_exc()
            if 'type' in self.r:
                del self.r['type']
        return self.r

    def _gethdinfo(self, d: dict) -> int:
        uri = f"https://api.bilibili.com/x/stein/edgeinfo_v2?bvid={d['bvid']}&graph_version={d['gv']}&platform=pc&portal=0&screen=0&buvid={self._r.cookies.get('buvid3')}"
        re = self._r.get(uri)
        re.encoding = 'utf8'
        re = re.json()
        if re['code'] != 0:
            self.r['data'] = {'code': -1, 're': re}
            return -1
        q = []
        if 'questions' in re['data']['edges']:
            q = re['data']['edges']['questions']
        e = []
        self._addninfo(re, e)
        for a in q:
            for b in a['choices']:
                read = self._getnch(b, d, e)
                if read == -1:
                    return -1
        d['page'] = e
        return 0

    def _getnch(self, b: dict, d: dict, e: list):
        uri = f"https://api.bilibili.com/x/stein/edgeinfo_v2?bvid={d['bvid']}&edge_id={b['id']}&graph_version={d['gv']}&platform=pc&portal=0&screen=0&buvid={self._r.cookies.get('buvid3')}&choice={b['native_action']}"
        re = self._r.get(uri)
        re.encoding = 'utf8'
        re = re.json()
        if re['code'] != 0:
            self.r['data'] = {'code': -1, 're': re}
            return -1
        q = []
        if 'questions' in re['data']['edges']:
            q = re['data']['edges']['questions']
        self._addninfo(re, e)
        for a in q:
            for b in a['choices']:
                read = self._getnch(b, d, e)
                if read == -1:
                    return -1

    def _addninfo(self, d: dict, l: list):
        d = d['data']
        e = {}
        e['page'] = len(l)+1
        e['part'] = d['title']
        i = d['edge_id']
        for k in d['story_list']:
            if k['edge_id'] == i:
                e['cid'] = k['cid']
                if self._infoqc(e['cid'], l):  # 发现重复，跳过
                    return
                l.append(e)
                break

    def _infoqc(self, c: int, l: list):
        "对互动视频列表进行去重"
        for i in l:
            if i['cid'] == c:
                return True
        return False
