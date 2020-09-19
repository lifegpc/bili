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
from .utils import addcookies, geturllength
from requests import Session
from re import search
from json import loads
from dict import delli, dellk


def normalurle(r: Session, url: str, data: dict, all: bool = True, vurl: bool = True, vq: int = 120, vcodec: str = None, aq: int = 30280) -> (int, dict):
    """解析视频链接
    data 存储有aid,bvid,cid的字典
    all 是否解析出所有格式
    vurl 是否在返回值中包括具体视频链接
    vq 指定具体画质（仅在all为false时生效）
    vcodec 指定具体编码器（hev或avc）
    aq 指定具体音质（仅在all为false并且流类型为dash时生效）"""
    if all:
        addcookies(r)
    else:
        addcookies(r, vq)
    r.headers.update({'referer': url})
    re = r.get(url)
    re.encoding = 'utf8'
    rs = search(r'__playinfo__=([^<]+)', re.text)
    napi = True  # 新API
    if rs is not None:
        re = loads(rs.groups()[0])
    else:
        uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn={vq}&otype=json&bvid={data['bvid']}&fnver=0&fnval=16&session="
        re = r.get(uri)
        re.encoding = 'utf8'
        re = re.json()
        if re['code'] != 0:
            return -1, {'code': -2, 're': re}
        napi = False
    d = {'referer': url}
    if 'data' in re and 'durl' in re['data']:
        re = re['data']
        d['type'] = 'durl'
        d['timelength'] = re['timelength']
        accept_description = re['accept_description']
        quality = re['quality']
        accept_quality = re['accept_quality']
        d['accept_description'] = accept_description
        d['accept_quality'] = accept_quality
        accept_description_dict = {}
        k = 0
        for i in accept_quality:
            accept_description_dict[i] = accept_description[k]
            k = k + 1
        d['accept_description_dict'] = accept_description_dict
        if not all:
            d['quality'] = quality
        durl = {}
        d['data'] = durl
        d2 = {'id': quality, 'desc': accept_description_dict[quality]}
        if all:
            durl[quality] = d2
        else:
            d['data'] = d2
        if vurl:
            d2['durl'] = re['durl']
        size = 0
        for i in re['durl']:
            size = size + i['size']
        d2['size'] = size
        if all and len(accept_quality) > 1:
            for i in accept_quality:
                if not i in durl:
                    if napi:
                        addcookies(r, i)
                        re = r.get(url)
                        re.encoding = 'utf8'
                        rs = search(r'__playinfo__=([^<]+)', re.text)
                        if rs is not None:
                            re = loads(rs.groups()[0])
                        else:
                            napi = False
                            uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn={i}&otype=json&bvid={data['bvid']}&fnver=0&fnval=16&session="
                            re = r.get(uri)
                            re.encoding = 'utf8'
                            re = re.json()
                            if re['code'] != 0:
                                return -1, {'code': -2, 're': re}
                    else:
                        uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn={i}&otype=json&bvid={data['bvid']}&fnver=0&fnval=16&session="
                        re = r.get(uri)
                        re.encoding = 'utf8'
                        re = re.json()
                        if re['code'] != 0:
                            return -1, {'code': -2, 're': re}
                    re = re['data']
                    if not re['quality'] in durl:
                        d2 = {
                            'id': re['quality'], 'desc': accept_description_dict[re['quality']]}
                        durl[re['quality']] = d2
                        if vurl:
                            d2['durl'] = re['durl']
                        for i in re['durl']:
                            size = size + i['size']
                        d2['size'] = size
                    if data['vip'] < 1 and (quality > 80 or quality == 74):
                        accept_quality, ii = delli(accept_quality, quality)
                        if ii > -1:
                            accept_description = dellk(accept_description, ii)
                        continue
            addcookies(r)
    elif 'data' in re and 'dash' in re['data']:
        re = re['data']
        d['type'] = 'dash'
        d['timelength'] = re['timelength']
        accept_description = re['accept_description']
        accept_quality = re['accept_quality']
        accept_description_dict = {}
        k = 0
        for i in accept_quality:
            accept_description_dict[i] = accept_description[k]
            k = k + 1
        d['accept_quality'] = accept_quality
        d['accept_description_dict'] = accept_description_dict
        has_audio = False
        if 'audio' in re['dash']:
            has_audio = True
            accept_audio_quality = []
            for i in re['dash']['audio']:
                if i['id'] not in accept_audio_quality:
                    accept_audio_quality.append(i['id'])
            accept_audio_quality.sort(reverse=True)
        else:
            accept_audio_quality = None
        d['accept_audio_quality'] = accept_audio_quality
        dash = {}
        d['data'] = dash
        if all:
            vid = []
            accept_video_quality = []
            accept_videoc_quality = []
            dash['video'] = vid
            for i in re['dash']['video']:
                if not f"{i['id']}{i['codecs']}" in accept_videoc_quality:
                    if not i['id'] in accept_video_quality:
                        accept_video_quality.append(i['id'])
                    accept_videoc_quality.append(f"{i['id']}{i['codecs']}")
                    t = {'id': i['id'], 'desc': accept_description_dict[i['id']], 'codecs': i['codecs'],
                         'width': i['width'], 'height': i['height'], 'frame_rate': i['frame_rate']}
                    if vurl:
                        if 'backup_url' in i and i['backup_url'] is not None:
                            t['url'] = [i['base_url']] + i['backup_url']
                        else:
                            t['url'] = [i['base_url']]
                    t['size'] = geturllength(r, i['base_url'])
                    vid.append(t)
            bs = True
            while bs:
                bs = False
                for i in accept_quality:
                    if i not in accept_video_quality:
                        if data['vip'] < 1 and i <= 80 and i != 74:
                            bs = True
                        elif data['vip'] > 0:
                            bs = True
                        if napi:
                            addcookies(r, i)
                            re = r.get(url)
                            re.encoding = 'utf8'
                            rs = search(r'__playinfo__=([^<]+)', re.text)
                            if rs is not None:
                                re = loads(rs.groups()[0])
                            else:
                                napi = False
                                uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn={i}&otype=json&bvid={data['bvid']}&fnver=0&fnval=16&session="
                                re = r.get(uri)
                                re.encoding = 'utf8'
                                re = re.json()
                                if re['code'] != 0:
                                    return -1, {'code': -2, 're': re}
                        else:
                            uri = f"https://api.bilibili.com/x/player/playurl?cid={data['cid']}&qn={i}&otype=json&bvid={data['bvid']}&fnver=0&fnval=16&session="
                            re = r.get(uri)
                            re.encoding = 'utf8'
                            re = re.json()
                            if re['code'] != 0:
                                return -1, {'code': -2, 're': re}
                        re = re['data']
                        for i in re['dash']['video']:
                            if not f"{i['id']}{i['codecs']}" in accept_videoc_quality:
                                if not i['id'] in accept_video_quality:
                                    accept_video_quality.append(i['id'])
                                accept_videoc_quality.append(
                                    f"{i['id']}{i['codecs']}")
                                t = {'id': i['id'], 'desc': accept_description_dict[i['id']], 'codecs': i['codecs'],
                                     'width': i['width'], 'height': i['height'], 'frame_rate': i['frame_rate']}
                                if vurl:
                                    if 'backup_url' in i and i['backup_url'] is not None:
                                        t['url'] = [i['base_url']] + \
                                            i['backup_url']
                                    else:
                                        t['url'] = [i['base_url']]
                                t['size'] = geturllength(r, i['base_url'])
                                vid.append(t)
            if has_audio:
                aid = []
                dash['audio'] = aid
                for j in accept_audio_quality:
                    k = 0
                    for i in re['dash']['audio']:
                        if i['id'] == j:
                            break
                        k = k + 1
                    i = re['dash']['audio'][k]
                    t = {'id': i['id'],  'codecs': i['codecs']}
                    if vurl:
                        if 'backup_url' in i and i['backup_url'] is not None:
                            t['url'] = [i['base_url']] + i['backup_url']
                        else:
                            t['url'] = [i['base_url']]
                    t['size'] = geturllength(r, i['base_url'])
                    aid.append(t)
            else:
                dash['audio'] = None
    return 0, d
