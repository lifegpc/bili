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
from websocket import WebSocket
from requests import Session
from Logger import Logger
from inspect import currentframe
from traceback import format_exc
from json import loads, dumps
from typing import Union
from threading import Lock, Thread
from time import time, sleep
from os import environ, devnull, system
from re import search, I
from JSONParser import getset
from M3UDownloader import (
    DownloadProcess,
    NicoLiveDownloaderThread,
    FfmpegM3UDownloader
)
from websocket._exceptions import (
    WebSocketTimeoutException,
    WebSocketConnectionClosedException
)
from os.path import splitext, exists
from autoopenlist import autoopenfilelist
from multithread import makeSureAllClosed


STREAM_QUALITY = {0: "BroadcasterHigh", 1: "BroadcasterLow", 2: "Abr", 3: "UltraHigh", 4: "SuperHigh", 5: "High", 6: "Normal", 7: "Low", 8: "SuperLow", 9: "AudioHigh", "BroadcasterHigh": 0, "BroadcasterLow": 1, "Abr": 2, "UltraHigh": 3, "SuperHigh": 4, "High": 5, "Normal": 6, "Low": 7, "SuperLow": 8, "AudioHigh": 9}
DEFAULT_STREAM_QUALITY = 2
QUALITY_LABEL = {"BroadcasterHigh": "broadcaster_high", "BroadcasterLow": "broadcaster_low", "Abr": "abr", "UltraHigh": "6Mbps1080p30fps", "SuperHigh": "super_high", "High": "high", "Normal": "normal", "Low": "low", "SuperLow": "super_low", "AudioHigh": "audio_high"}
QUALITY_LABEL2 = {}
for key in QUALITY_LABEL:
    QUALITY_LABEL2[QUALITY_LABEL[key]] = key


def genStartWatching(quality: int = DEFAULT_STREAM_QUALITY):
    return {"type": "startWatching", "data": {"reconnect": False, "room": {"commentable": True, "protocol": "webSocket"}, "stream": {"chasePlay": False, "latency": "low", "protocol": "hls", "quality": quality}}}


def sendMsg(w: WebSocket, lock: Lock, msg: Union[str, dict], logg: Logger):
    try:
        with lock:
            if isinstance(msg, dict):
                msg = dumps(msg, ensure_ascii=False, separators=(',', ':'))
            if logg:
                logg.write(f"send Msg to WebSocket: {msg}", currentframe(), "Send Msg To WebSocket")
            print(msg)
            w.send(msg)
        return True
    except:
        if logg:
            logg.write(format_exc(), currentframe(), "Can't send msg to websocket")
        return False


class KeepSeatThread(Thread):
    def __init__(self, name: str, keepIntervalSec: int, w: WebSocket, lock: Lock, logg: Logger):
        Thread.__init__(self, name=f"keepSeatThread:{name}")
        self._keepIntervalSec = keepIntervalSec
        self._w = w
        self._lock = lock
        self._stop = False
        self._logg = logg
        self._lastSend = 0

    def kill(self):
        self._stop = True
        if self._logg:
            self._logg.write(f"{self.name}: Get Kill Signial", currentframe(), "NicoNico Live Video Keep Seat Thread Get Kill")

    def run(self):
        while True:
            if self._stop:
                break
            if time() < self._lastSend + self._keepIntervalSec:
                sleep(1)
            else:
                self.send()

    def send(self) -> int:
        self._lastSend = time()
        sendMsg(self._w, self._lock, {"type": "keepSeat"}, self._logg)


def getProxyDict(pro: str) -> dict:
    r = {}
    if pro is None:
        return r
    re = search(r'(http://)?(([^:]+):([^@]+)@)?([^:]+)(:([0-9]+))?', pro, I)
    if re is None:
        return r
    re = re.groups()
    if re[1]:
        r['http_proxy_auth'] = (re[2], re[3])
    r['http_proxy_host'] = re[4]
    if re[5]:
        port = int(re[6])
        if port >= 0 and port < 2 ** 16:
            r['http_proxy_port'] = port
    return r


def downloadLiveVideo(r: Session, data: dict, threadMap: dict, se: dict, ip: dict, dirName: str, filen: str, imgs: int, imgf: str):
    """下载视频
    - data 数据字典
    - threadMap 线程Map
    - se 设置字典
    - ip 命令行字典
    - dirName 下载的目录
    - filen 最终视频文件名
    - imgs 图片下载状态
    - imgf 图片名称
    -1 建立WebSocket失败
    -2 发送startWatch失败
    -3 找不到ffmpeg
    -4 下载出现问题"""
    logg: Logger = ip['logg'] if 'logg' in ip else None
    oll: autoopenfilelist = ip['oll'] if 'oll' in ip else None
    nte = not ip['te'] if 'te' in ip else True if getset(se, 'te') is False else False
    useInternalDownloader = ip['imn'] if 'imn' in ip else True if getset(se, 'imn') is True else False
    ff = system(f"ffmpeg -h > {devnull} 2>&1") == 0
    if not ff and not useInternalDownloader:
        return -3
    websocket = WebSocket(enable_multithread=True)
    try:
        pro = None
        if not nte:
            if 'https_proxy' in environ:
                pro = environ['https_proxy']
        if 'httpsproxy' in ip:
            pro = ip['httpsproxy']
        op = getProxyDict(pro)
        headers = {"origin": "https://live.nicovideo.jp", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Language": "ja-JP"}
        websocket.connect(data['site']['relive']['webSocketUrl'], header=headers, **op)
    except:
        if logg:
            logg.write(format_exc(), currentframe(), "NicoNico Live Video Create WebSocket Failed")
        return -1
    lock = Lock()
    if not sendMsg(websocket, lock, genStartWatching(data['program']['stream']['maxQuality']), logg):
        return -2
    Ok = False
    keepThread: KeepSeatThread = None
    dl = []
    dp: DownloadProcess = None
    dpc = 0
    lvid = data['program']['nicoliveProgramId'][2:]
    websocket.settimeout(5)
    while not Ok:
        try:
            try:
                message = websocket.recv()
            except WebSocketTimeoutException:
                message = None
                if data['program']['status'] == 'ENDED':
                    if makeSureAllClosed(dl):
                        Ok = True
            except WebSocketConnectionClosedException:
                break
            if message is not None and logg:
                logg.write(f"String msg:\n{message}", currentframe(), "NicoNico Live Video WebSocket Get Message")
            if message is not None and message != '':
                msg = loads(message, strict=False)
                if msg["type"] == "ping":
                    sendMsg(websocket, lock, {"type": "pong"}, logg)
                elif msg["type"] == "seat":
                    if keepThread is None:
                        keepThread = KeepSeatThread(f"lv{lvid}", msg["data"]["keepIntervalSec"], websocket, lock, logg)
                        threadMap[f"lv{lvid}_{round(time())}"] = keepThread
                        keepThread.start()
                    else:
                        keepThread._keepIntervalSec = msg["data"]["keepIntervalSec"]
                elif msg["type"] == "statistics":
                    pass
                elif msg["type"] == "stream":
                    if dpc == 0:
                        startpos = max(data['program']['beginTime'] - data['program']['vposBaseTime'] - 5, 0) if data['program']['status'] == 'ENDED' else None
                    else:
                        startpos = None
                    if useInternalDownloader:
                        if dp is None:
                            dp = DownloadProcess()
                        dt = NicoLiveDownloaderThread(f"lv{lvid},{dpc}", data, msg["data"], dp, logg, r, dirName)
                        threadMap[f"lv{lvid},{dpc}_{round(time())}"] = dt
                        dl.append(dt)
                        dt.start()
                    else:
                        fn = filen if dpc == 0 else f"{splitext(filen)[0]}_{dpc}{splitext(filen)[1]}"
                        while exists(fn):  # 如果有重复的名字，自动修改名字
                            dpc += 1
                            fn = filen if dpc == 0 else f"{splitext(filen)[0]}_{dpc}{splitext(filen)[1]}"
                        dt2 = FfmpegM3UDownloader(f"lv{lvid},{dpc}", fn, data, msg["data"], logg, imgs, imgf, oll, startpos)
                        threadMap[f"lv{lvid},{dpc}_{round(time())}"] = dt2
                        dl.append(dt2)
                        dt2.start()
                elif msg["type"] == "disconnect" and msg["data"]["reason"] == "END_PROGRAM":
                    Ok = True
                    break
                else:
                    print(msg)
        except KeyboardInterrupt:
            if logg:
                logg.write("Get Keyboard Interrupt", currentframe(), "NicoNico Live Video WebSocket Get KILL")
            Ok = True
        except:
            if logg:
                logg.write(format_exc(), currentframe(), "NicoNico Live Video WebSocket Error")
    return 0 if Ok else -4
