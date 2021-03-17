# (C) 2019-2021 lifegpc
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
# 下列常量在 https://nicovideo.cdn.nimg.jp/web/scripts/pages/watch/modern/watch_dll_a111f699de384a78533e.js 中定义
from math import ceil
from json import loads as loadjson

DEFAULT_COMMENT_NUM_PER_LEAF = 100
MAX_COMMENT_NUM = 72000
LANG_MAP = {'ja-jp': 0, 'en-us': 1, 'zh-tw': 2}


class LeafExpression:
    def __init__(self):
        self.leafNum = 1
        self.commentNumPerLeaf = DEFAULT_COMMENT_NUM_PER_LEAF
        self.resFrom = 0
        self.withNewNicoru = False

    def __str__(self):
        t = f",{self.resFrom}" if self.resFrom > 0 else ''
        return f"0-{self.leafNum}:{self.commentNumPerLeaf}{t}{',nicoru:100' if self.withNewNicoru else ''}"

    def toStr(self):
        return str(self)


def calLeafExpression(videoLengthSec: int, **k) -> LeafExpression:
    r = LeafExpression()
    r.leafNum = ceil(videoLengthSec / 60)
    if k.get("commentNumPerLeaf") is not None:
        r.commentNumPerLeaf = k.get("commentNumPerLeaf")
    if k.get("resFrom") is not None:
        r.resFrom = k.get("resFrom")
    if k.get("withNewNicoru") is True:
        r.withNewNicoru = True
    if r.leafNum * r.commentNumPerLeaf > MAX_COMMENT_NUM:
        r.commentNumPerLeaf = ceil(MAX_COMMENT_NUM / r.leafNum)
    return r


def getResFromForVideo(duration: int) -> int:
    "duration 视频时长（单位：秒）"
    return 100 if duration < 60 else 250 if duration < 300 else 500 if duration < 600 else 1000


class CommentThread():
    id: int = -1
    fork: int = 0
    isActive: bool = False
    postkeyStatus: int = 0
    isDefaultPostTarget: bool = False
    isThreadkeyRequired: bool = False
    label: str = ''
    name: str = 'defaults'

    def __init__(self, d: dict):
        self.id = d['id']
        self.fork = d['fork']
        self.isActive = d['isActive']
        self.postkeyStatus = d['postkeyStatus']
        self.isDefaultPostTarget = d['isDefaultPostTarget']
        self.isThreadkeyRequired = d['isThreadkeyRequired']
        self.label = "defaults" if d['label'] in ["default", "mymemory"] else d['label']

    def isOwnerThread(self):
        return self.fork == 1

    def isEasyCommentThread(self):
        return self.fork == 2

    def commentPostable(self):
        return self.postkeyStatus == 0

    def genContent(self, duration: int, whenSec: int = None) -> str:
        """duration 视频时长（单位：秒）
        whenSec 哪个时间点的弹幕（历史弹幕？）"""
        if self.isEasyCommentThread():
            leaf = calLeafExpression(duration, commentNumPerLeaf=25, resFrom=0, withNewNicoru=True)
        elif whenSec is not None:
            leaf = calLeafExpression(duration, commentNumPerLeaf=0, resFrom=getResFromForVideo(duration), withNewNicoru=False)
        elif not self.isOwnerThread():
            leaf = calLeafExpression(duration, resFrom=getResFromForVideo(duration), withNewNicoru=True)
        else:
            return None
        return str(leaf)

    def genThread(self, data: dict, **k):
        lan = k.get("lan") if k.get("lan") is not None and k.get("lan") in LANG_MAP else 'ja-jp'
        return {"fork": self.fork, "language": LANG_MAP[lan], "nicoru": 3, "scores": 1, "thread": str(self.id), "user_id": str(data["viewer"]["id"]), "userkey": data['comment']['keys']['userKey'], "version": "20090904", "with_global": 1}

    def genThreadLeaves(self, data: dict, **k):
        d = self.genThread(data, **k)
        del d["version"]
        del d["with_global"]
        con = self.genContent(data['video']['duration'])
        if con is not None:
            d["content"] = con
        return d


def generatePara(l: list) -> list:  # noqa: E741
    r = [{"ping": {"content": "rs:0"}}]
    k = 0
    for i in l:
        r.append({"ping": {"content": f"ps:{k}"}})
        r.append(i)
        r.append({"ping": {"content": f"pf:{k}"}})
        k += 1
    r.append({"ping": {"content": "rf:0"}})
    return r


def genNicoDanmuPara(data: dict) -> list:
    commentThreadL = data["comment"]["threads"]
    rel = []
    for i in commentThreadL:
        com = CommentThread(i)
        if com.isActive:
            rel.append({"thread": com.genThread(data)})
            rel.append({"thread_leaves": com.genThreadLeaves(data)})
    return generatePara(rel)


def findAudioIndex(availableAudios: list, levelIndex: int) -> str:
    for i in availableAudios:
        if i['metadata']['levelIndex'] == levelIndex:
            return i['id']
    return availableAudios[0]['id']


def genNicoVideoPara(data: dict) -> dict:
    r = {}
    delivery = data['media']['delivery']
    movie = delivery['movie']
    availableVideos = [video for video in movie['videos'] if video['isAvailable'] is True]
    availableAudios = [audio for audio in movie['audios'] if audio['isAvailable'] is True]
    session = movie["session"]
    token = loadjson(session['token'])
    r['recipe_id'] = session['recipeId']
    r['content_id'] = token['content_ids'][0]
    r['content_type'] = "movie"
    contsrc = []
    vinfoids = [i['id'] for i in availableVideos]
    for vinfo in availableVideos:
        vsrcs = vinfoids[vinfoids.index(vinfo['id']):]
        asrcs = [findAudioIndex(availableAudios, vinfo['metadata']['recommendedHighestAudioLevelIndex'])]
        contsrc.append({"src_id_to_mux": {"video_src_ids": vsrcs, "audio_src_ids": asrcs}})
    r['content_src_id_sets'] = [{"content_src_ids": contsrc}]
    r['timing_constraint'] = 'unlimited'
    r['keep_method'] = {"heartbeat": {"lifetime": token['heartbeat_lifetime']}}
    r['protocol'] = {"name": token['protocols'][0]['name'], "parameters": {"http_parameters": {"parameters": {"hls_parameters": {"use_well_known_port": "yes", "use_ssl": "yes", "transfer_preset": "", "segment_duration": 6000}}}}}
    r['content_uri'] = ""
    r['session_operation_auth'] = {"session_operation_auth_by_signature": {"token": session['token'], "signature": session["signature"]}}
    r['content_auth'] = {"auth_type": token['protocols'][0]['auth_type'], "content_key_timeout": token['content_key_timeout'], "service_id": token['service_id'], "service_user_id": token["service_user_id"]}
    r['client_info'] = {"player_id": token["player_id"]}
    r['priority'] = round(token['priority'], 1)
    return {"session": r}
