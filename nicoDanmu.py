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
from typing import List
from re import split, match
from hashl import crc32
from threading import Thread, Lock
from enum import Enum, unique
from Logger import Logger
from traceback import format_exc
from inspect import currentframe
from urllib.parse import urlsplit
from biliDanmuCreate import objtoxml
from websocket import WebSocket
from websocket._exceptions import (
    WebSocketConnectionClosedException,
    WebSocketTimeoutException
)
from typing import Union
from time import time, sleep
from json import dumps, loads


COLORS = {"white": "#ffffff", "red": "#ff0000", "pink": "#ff8080", "orange": "#ffc000", "yellow": "#ffff00", "green": "#00ff00", "cyan": "#00ffff", "blue": "#0000ff", "purple": "#c000ff", "black": "#000000"}
DEFAULT_COLOR = "#ffffff"
DEFAULT_FONT = "defont"
DEFAULT_POSITION = "naka"  # 中
DEFAULT_SIZE = "medium"
FONTS_ARRAY = ["defont", "gothic", "mincho"]
POSITIONS_ARRAY = ["ue", "naka", "shita"]  # 上中下
PREMIUM_COLORS = {"white2": "#cccc99", "niconicowhite": "#cccc99", "red2": "#cc0033", "truered": "#cc0033", "orange2": "#ff6600", "passionorange": "#ff6600", "yellow2": "#999900", "madyellow": "#999900", "green2": "#00cc66", "elementalgreen": "#00cc66", "blue2": "#3399ff", "marineblue": "#3399ff", "purple2": "#6633cc", "nobleviolet": "#6633cc", "pink2": "#ff33cc", "cyan2": "#00cccc", "black2": "#666666"}
SIZES_ARRAY = ["big", "medium", "small"]


def isColorCodeCommand(s: str) -> bool:
    return match(r'^#([\da-fA-F]{6})$', s)


class NicoDanmu:
    thread: str = ''
    no: int = 0
    content: str = ''
    vpos: int = 0
    mail: List[str] = []
    date: int = 0
    dataUsec: int = 0
    userId: str = ''
    premium: int = 0
    nicoru: int = 0
    lastNicoruDate = None
    valhalla: bool = False
    deletedStatus: int = 0
    anonymous: bool = False
    score: int = 0
    fork: int = 0
    color: str = DEFAULT_COLOR
    size: str = DEFAULT_SIZE
    position: str = DEFAULT_POSITION

    def __init__(self, d: dict, offset: Union[int, float] = 0, no: int = 0):
        self.vposOffset = offset
        self.thread = d['thread']
        if 'no' in d:
            self.onlyno = False
            self.no = d['no']
        else:
            self.onlyno = True
            self.no = no
        if 'content' in d:
            self.content: str = d['content']
        self.vpos = d['vpos']
        if 'mail' in d:
            self.mail = split(r'\s+', d['mail'])
        self.date = d['date']
        self.dataUsec = d['date_usec']
        if 'user_id' in d:
            self.userId = d['user_id']
        if 'premium' in d:
            self.premium = d['premium']
        if 'nicoru' in d:
            self.nicoru = d['nicoru']
        if 'last_nicoru_date' in d:
            self.lastNicoruDate = d['last_nicoru_date']
        if 'valhalla' in d:
            self.valhalla = d['valhalla'] == 1
        if 'deleted' in d:
            self.deletedStatus = d['deleted']
        if 'anonymity' in d:
            self.anonymous = d['anonymity'] == 1
        if 'score' in d:
            self.score = d['score']
        if 'fork' in d:
            self.fork = d['fork']
        for i in self.mail:
            if i in POSITIONS_ARRAY:
                self.position = i
            elif i in SIZES_ARRAY:
                self.size = i
            elif i in COLORS:
                self.color = COLORS[i]
            elif i in PREMIUM_COLORS:
                self.color = PREMIUM_COLORS[i]
            elif isColorCodeCommand(i):
                self.color = i

    def getColor(self):
        return int(self.color[1:], 16)

    def getDanmuType(self):
        if self.position == DEFAULT_POSITION:
            return 1
        elif self.position == "ue":
            return 5
        return 4

    def getSize(self):
        if self.size == DEFAULT_SIZE:
            return 25
        elif self.size == "small":
            return 18
        elif self.size == "big":
            return 40

    def isInternalFiltered(self):
        if self.content.startswith("/"):
            return True
        if self.content.startswith("<a>") and self.content.endswith("</a>"):
            return True
        return False

    def toBiliVer(self):
        return {"t": self.content, "mod": self.getDanmuType(), "fs": self.getSize(), "fc": self.getColor(), "ut": self.date, "ti": round(self.vpos / 100 - self.vposOffset, 5), "si": crc32(self.userId), "ri": f"{self.no:#04}" if self.onlyno else f"{self.thread}{self.no:#04}", "dp": 0}


def getNicoDanmuList(l: list) -> list:  # noqa: E741
    r = []
    for i in l:
        if 'chat' in i:
            n = NicoDanmu(i['chat'])
            if not n.deletedStatus:
                r.append(n.toBiliVer())
    return r


@unique
class NicoDanmuFileStatus(Enum):
    INITIALIZE = 0
    OPENED = 1
    CLOSED = 2
    ERROR = 3


class NicoDanmuFile:
    def __init__(self, fn: str, data: dict, room: dict, logg: Logger):
        self.lock = Lock()
        self.status = NicoDanmuFileStatus.INITIALIZE
        self._fn = fn
        self._f = None
        self._logg = logg
        self._data = data
        self._room = room
        self.no = 1

    def open(self):
        with self.lock:
            self.__open()

    def __open(self):
        if self._f is not None or self.status != NicoDanmuFileStatus.INITIALIZE:
            return
        try:
            self._f = open(self._fn, 'w', encoding='utf8')
            self._f.write('<?xml version="1.0" encoding="UTF-8"?>')
            self._f.write(f"<i><chatserver>{urlsplit(self._room['messageServer']['uri']).hostname}</chatserver><chatid>{self._data['program']['nicoliveProgramId'][2:]}</chatid><mission>0</mission><maxlimit>8000</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>")
            self.status = NicoDanmuFileStatus.OPENED
        except:
            if self._logg:
                self._logg.write(format_exc(), currentframe(), "NicoNico Live Danmu File Open File Failed")
            self.status = NicoDanmuFileStatus.ERROR

    def write(self, data: dict, vposOffset: Union[int, float] = 0, no: int = 0):
        try:
            n = NicoDanmu(data, vposOffset, no)
            if n.isInternalFiltered():
                return False
            d = n.toBiliVer()
        except:
            if self._logg:
                self._logg.write(format_exc(), currentframe(), "NicoNico Live Danmu File Convert Failed")
            return False
        with self.lock:
            if self.status == NicoDanmuFileStatus.INITIALIZE:
                self.__open()
            if self.status in [NicoDanmuFileStatus.ERROR, NicoDanmuFileStatus.CLOSED]:
                return False
            try:
                self._f.write(objtoxml(d))
                self.no += 1
                return True
            except:
                if self._logg:
                    self._logg.write(format_exc(), currentframe(), "NicoNico Live Danmu File Write To File Failed")
                return False

    def close(self):
        with self.lock:
            if self._f is None or self.status != NicoDanmuFileStatus.OPENED:
                return
            try:
                self._f.write('</i>')
                self._f.close()
                self.status = NicoDanmuFileStatus.CLOSED
            except:
                if self._logg:
                    self._logg.write(format_exc(), currentframe(), "NicoNico Live Danmu File Close Failed")
                self.status = NicoDanmuFileStatus.ERROR


class NicoLiveDanmuHeartBeatThread(Thread):
    def __init__(self, name: str, logg: Logger, ws: WebSocket):
        Thread.__init__(self, name=f"DanmuHeartBeatThread:{name}")
        self._logg = logg
        self._ws = ws
        self._mystop = False

    def kill(self):
        self._mystop = True
        if self._logg:
            self._logg.write(f'{self.name}: Get Kill Signial', currentframe(), "NicoNico Live Danmu HeartBeat Thread Kill")

    def run(self):
        lastT = time()
        while True:
            try:
                if self._mystop:
                    break
                if time() < lastT + 60:
                    sleep(1)
                if time() >= lastT + 60:
                    lastT = time()
                    if self._logg:
                        self._logg.write(f'{self.name}: Send HeartBeat', currentframe(), "NicoNico Live Danmu HeartBeat Thread Send")
                    while True:
                        try:
                            self._ws.send('')
                            break
                        except WebSocketTimeoutException:
                            if self._mystop:
                                break
            except KeyboardInterrupt:
                break
            except WebSocketConnectionClosedException:
                break
            except:
                if self._logg:
                    self._logg.write(f"{self.name}\n{format_exc()}", currentframe(), "NicoNico Live Danmu HeartBeat Thread Error")


@unique
class NicoLiveDanmuRequestStatus(Enum):
    INITLDATA = 0
    INITLDATACOM = 1
    NEWDATA = 2


class NicoLiveDanmuRequestThread(Thread):
    def __init__(self, name: str, logg: Logger, ws: WebSocket, room: dict, data: dict, startpos: Union[int, float], speed: Union[int, float]):
        Thread.__init__(self, name=f"DanmuRequestThread:{name}")
        self._logg = logg
        self._ws = ws
        self._status = NicoLiveDanmuRequestStatus.INITLDATA
        self._room = room
        self._data = data
        self._i = 0
        self._startpos = startpos
        self._startT = time()
        self._lastT = self._startT
        self.__dataList = []
        self._lock = Lock()
        self._speed = speed
        self._mystop = False

    def addData(self, i: dict):
        with self._lock:
            self._status = NicoLiveDanmuRequestStatus.NEWDATA
            self.__dataList.append(i)

    def genPara(self, i: dict = None):
        p = [{"ping": {"content": f"rs:{self._i}"}}, {"ping": {"content": f"ps:{self._i * 5}"}}]
        d = {"nicoru": 0}
        d['res_from'] = -200 if self._status == NicoLiveDanmuRequestStatus.INITLDATA else i['last_res'] + 1
        d['scores'] = 1
        d['thread'] = self._room['threadId']
        d['user_id'] = self._data['user']['id']
        d['version'] = "20061206"
        d['waybackkey'] = self._room['waybackkey'] if self._room['waybackkey'] != 'waybackkey' else ''
        if self._data['program']['status'] == 'ENDED':
            startpos = self._startpos if self._startpos is not None else 0
            d['when'] = round((time() - self._startT) * self._speed + self._data['program']['openTime'] + startpos, 3)
        else:
            startpos = self._startpos
            if startpos is None:
                d['when'] = round(time(), 3)
            else:
                d['when'] = round(time() - self._startT + self._data['program']['beginTime'] + startpos, 3)
        d['with_global'] = 1
        p.append({"thread": d})
        p.append({"ping": {"content": f"pf:{self._i * 5}"}})
        p.append({"ping": {"content": f"rf:{self._i}"}})
        return p

    def getData(self):
        with self._lock:
            if self._status != NicoLiveDanmuRequestStatus.NEWDATA:
                return None
            if len(self.__dataList) < 1:
                return None
            return self.__dataList[0]

    def hasData(self):
        with self._lock:
            if self._status != NicoLiveDanmuRequestStatus.NEWDATA:
                return 0
            return len(self.__dataList)

    def removeData(self):
        with self._lock:
            if self._status != NicoLiveDanmuRequestStatus.NEWDATA or len(self.__dataList) < 1:
                return False
            del self.__dataList[0]
            return True

    def kill(self):
        self._mystop = True
        if self._logg:
            self._logg.write(f"{self.name}: Get Kill Signial", currentframe(), "NicoNico Live Danmu Request Thread Get Kill")

    def run(self):
        while True:
            if self._mystop:
                break
            if self._status == NicoLiveDanmuRequestStatus.INITLDATA:
                p = self.genPara()
                if not self.sendMess(p):
                    break
                else:
                    self._status = NicoLiveDanmuRequestStatus.INITLDATACOM
            elif self._status == NicoLiveDanmuRequestStatus.NEWDATA:
                if self.hasData():
                    i = self.getData()
                    if i is None:
                        sleep(1)
                    else:
                        if time() > self._lastT + (30 / self._speed):
                            p = self.genPara(i)
                            if not self.sendMess(p):
                                break
                            else:
                                self.removeData()
                        else:
                            sleep(1)
                else:
                    sleep(1)
            else:
                sleep(1)

    def sendMess(self, msg: Union[dict, str, list]):
        if isinstance(msg, (dict, list)):
            msg = dumps(msg, ensure_ascii=False, separators=(',', ':'))
        if self._logg:
            self._logg.write(f"{self.name}: Send Msg To WebSocket: {msg}", currentframe(), "NicoNico Danmu Live Request")
        while True:
            try:
                self._ws.send(msg)
                self._lastT = time()
                self._i += 1
                return True
            except WebSocketConnectionClosedException:
                return False
            except KeyboardInterrupt:
                return False
            except WebSocketTimeoutException:
                if self._mystop:
                    return False
            except:
                if self._logg:
                    self._logg.write(f"{self.name}:\n{format_exc()}", currentframe(), "NicoNico Live Danmu Request Thread Send Message Error")


class NicoLiveDanmuThread(Thread):
    def __init__(self, name: str, f: NicoDanmuFile, data: dict, room: dict, logg: Logger, speed: Union[int, float], headers: dict, op: dict, startpos: Union[int, float]):
        Thread.__init__(self, name=f"DanmuThread:{name}")
        self._tname = name
        self._file = f
        self._data = data
        self._room = room
        self._logg = logg
        self._speed = speed
        self._headers = headers
        self._op = op
        self._hb = None
        self._sr = None
        self._startpos = startpos
        self._mystop = False
        self._hasNoLastRes = False

    def kill(self):
        self._mystop = True
        if self._logg:
            self._logg.write(f"{self.name}: Get Kill Signial", currentframe(), "NicoNico Live Danmu Thread Get Kill")

    def killSubModule(self):
        if self._hb:
            self._hb.kill()
        if self._sr:
            self._sr.kill()
        while True:
            a = True if self._hb is None or not self._hb.is_alive() else False
            b = True if self._sr is None or not self._sr.is_alive() else False
            if a and b:
                break
            sleep(1)

    def run(self):
        try:
            self.openws()
            self._hb = NicoLiveDanmuHeartBeatThread(self._tname, self._logg, self._ws)
            self._hb.start()
            self._sr = NicoLiveDanmuRequestThread(self._tname, self._logg, self._ws, self._room, self._data, self._startpos, self._speed)
            self._sr.start()
            self.loop()
            self.killSubModule()
        except:
            if self._logg:
                self._logg.write(f"{self.name}:\n{format_exc()}", currentframe(), "NicoNico Live Danmu Thread Error")
            self.killSubModule()

    def openws(self):
        self._ws = WebSocket(enable_multithread=True)
        self._ws.connect(self._room["messageServer"]["uri"], headers=self._headers, **self._op)
        self._ws.settimeout(5)

    def loop(self):
        while True:
            try:
                if self._mystop:
                    break
                m = self._ws.recv()
                if isinstance(m, str):
                    if self._logg:
                        self._logg.write(f"{self.name}: Get Msg: {m}", currentframe(), "NicoNico Live Danmu Thread Get Message")
                    if m != '':
                        msg = loads(m)
                        if 'thread' in msg:
                            thread = msg['thread']
                            if 'last_res' in thread:
                                self._sr.addData(thread)
                            else:
                                self._hasNoLastRes = True
                        elif 'chat' in msg:
                            startpos = 0 if self._startpos is None else self._startpos
                            self._file.write(msg['chat'], startpos, self._file.no)
            except WebSocketConnectionClosedException:
                break
            except WebSocketTimeoutException:
                if self._mystop:
                    break
                elif self._data['program']['status'] == 'ENDED' and self._hasNoLastRes:
                    break
            except KeyboardInterrupt:
                break
            except:
                if self._logg:
                    self._logg.write(f"{self.name}:\n{format_exc()}", currentframe(), "NicoNico Live Danmu Thread Recive Data Error")
