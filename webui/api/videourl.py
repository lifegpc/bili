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
from . import apic, new_Session
from .checklogin import logincheck
from .session import NotLoginError
from ..extractor.normal import normalurle
from requests import Session
from time import time
import web


last_checktime: int = None  # 上次检查登录时间


class videourl(apic):
    _r: Session = None

    def __init__(self, inp: str):
        apic.__init__(self, inp)
        global last_checktime
        if last_checktime is None or last_checktime < (time()-60):
            last_checktime = time()
            if not logincheck():
                raise NotLoginError()
        self._r = new_Session()


class normalvideourl(videourl):
    _VALID_URI = r'^normalvideourl$'

    def _handle(self):
        aid: str = web.input().get('aid')
        bvid: str = web.input().get('bvid')
        cid: str = web.input().get('cid')
        p: str = web.input().get('p')
        vip: str = web.input().get('vip')
        vurl: str = web.input().get('vurl')
        vq: str = web.input().get('vq')
        vcodec: str = web.input().get('vcodec')
        aq: str =web.input().get('aq')
        if aid is None or bvid is None or cid is None or vip is None:
            return {'code': -1}
        if not aid.isnumeric() or not cid.isnumeric() or not vip.isnumeric():
            return {'code': -1}
        aid = int(aid)
        cid = int(cid)
        vip = int(vip)
        all = True
        if vq is not None and vq.isnumeric():
            vq = int(vq)
            all = False
        else:
            vq = 120
        if aq is not None and aq.isnumeric():
            aq = int(aq)
            all = False
        else:
            aq = 30280
        if vcodec is not None and vcodec in ['avc','hev']:
            all = False
        else:
            vcodec = None
        if vurl is None:
            vurl = False
        else:
            vurl = True
        if p is not None and not p.isnumeric():
            return {'code': -1}
        if p is None:
            p = 1
        else:
            p = int(p)
        if aid is not None:
            url = f'https://www.bilibili.com/video/av{aid}?p={p}'
        else:
            url = f'https://www.bilibili.com/video/{bvid}?p={p}'
        data = {'aid': aid, 'bvid': bvid, 'cid': cid, 'vip': vip}
        re, d = normalurle(self._r, url, data, all, vurl, vq, vcodec, aq)
        if re == -1:
            return d
        elif re == 0:
            return {'code': 0, 'data': d}
