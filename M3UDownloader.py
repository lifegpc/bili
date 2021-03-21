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
from requests import Session
from M3UParser import parseSimpleMasterM3U
from Logger import Logger
from inspect import currentframe
from traceback import format_exc
from os.path import splitext, exists, split as splitfn
from time import time, sleep
from file.info import size as fsize
from file import mkdir, urlsplitfn
from autoopenlist import autoopenfilelist
from threading import Thread, Lock
from typing import List
from multithread import makeSureAllClosed
from urllib.parse import urlsplit, urlunsplit, SplitResult
from nicoPara import getLiveMetaFile
from os import system, remove


def downloadNicoM3U(r: Session, url: str, index: int, fn: str, se: dict, ip: dict):
    '''下载M3U媒体播放列表
    - url m3u地址
    - index 从几个segment开始
    - fn 文件名
    - se 设置字典
    - ip 名里字典
    -1 请求错误
    -2 写入文件错误'''
    logg: Logger = ip['logg'] if 'logg' in ip else None
    oll: autoopenfilelist = ip['oll'] if 'oll' in ip else None
    speed = 1
    if logg:
        logg.write(f"GET {url}", currentframe(), "M3U Downloader Get M3U File")
    re = r.get(url)
    if logg:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "M3U Downloader M3U Content")
    if re.status_code >= 400:
        return -1, index
    li = parseSimpleMasterM3U(re.text, url)
    if logg:
        logg.write(f"li = {li}", currentframe(), "M3U Downloader M3U List")
    li = li[index:]
    totalSize = 0
    le = len(li)
    dirName = splitext(fn)[0]
    if not exists(f"{dirName}/"):
        mkdir(dirName)
    startInd = index
    startTime = time()
    lastTime = startTime
    for link in li:
        ok = False
        tfn = f"{dirName}/{index+1}.ts"
        if exists(tfn):
            if logg:
                logg.write(f"Segement {index} already exist, skip. link: {link}", currentframe(), "M3U Downloader Skip")
            if startInd == index:
                startInd += 1
            index += 1
            continue
        for retry in range(4):
            if retry:
                print(retry)
            try:
                if logg:
                    logg.write(f"GET Segement {index}: {link}", currentframe(), "M3U Downloader Download Segement")
                re = r.get(link)
                if logg:
                    logg.write(f"status = {re.status_code}", currentframe(), "M3U Downloader Download Segement")
                if re.status_code >= 400:
                    return -1, index
                try:
                    with open(tfn, 'wb') as f:
                        s = f.write(re.content)
                        totalSize += s
                    if logg:
                        logg.write(f"Write {s} bytes to file \"{tfn}\".", currentframe(), "M3U Downloader Write File")
                    oll.add(tfn)
                    ok = True
                    break
                except:
                    if logg:
                        logg.write(format_exc(), currentframe(), "M3U Downloader Write File Error")
                    return -2, index
            except:
                if logg:
                    logg.write(format_exc(), currentframe(), "M3U Downloader Download Error")
        if not ok:
            return -1, index
        now = time()
        percent = round((index + 1) / le * 100, 2)
        speedn = totalSize / (now - startTime)
        print(f"\r{percent}%({index+1}/{le})\t{fsize(totalSize)}({totalSize}B)\t{round(now-startTime, 2)}s\t{fsize(speedn)}/s({round(speedn)}B/s)", end="")
        if index > startInd + 6 and now < lastTime + (6 / speed):
            sleepTime = lastTime + (6 / speed) - time()
            if sleepTime > 0.1:
                sleep(sleepTime)
            now = time()
        lastTime = now
        index += 1
    return 0, index


class DownloadProcess:
    def __init__(self):
        self._startTime = time()
        self._lock = Lock()
        self._count = 0
        self._totalSize = 0
        self._lastPrintTime = self._startTime

    def add(self, size: int):
        with self._lock:
            self._count += 1
            self._totalSize += size
            self.__print()

    def __print(self):
        now = time()
        if now < self._lastPrintTime + 1:
            return
        speed = self._totalSize / (now - self._startTime)
        print(f"\r{self._count},{fsize(self._totalSize)}({self._totalSize}B),{round(now-self._startTime, 2)}s,{fsize(speed)}/s({round(speed)}B/s)", end="")
        self._lastPrintTime = now

    def print(self):
        with self._lock:
            self.__print()


class NicoLiveDownloaderThread(Thread):
    def __init__(self, name: str, data: dict, stream: dict, dp: DownloadProcess, logg: Logger, r: Session, dirName: str):
        Thread.__init__(self, name=f"LiveDownload:{name}")
        self._tname = name
        self._data = data
        self._stream = stream
        self._dp = dp
        self._logg = logg
        self._r = r
        self._pl = []
        self._mts = -1
        self._dirName = dirName
        self._tc = 0
        self._threadMap = {}
        self._stop = False

    def kill(self):
        self._stop = True
        if self._logg:
            self._logg.write(f"{self.name}: Get Kill Signial", currentframe(), "NicoNico Live Video Download Thread Get Kill")

    def run(self):
        if not self.downloadMasterM3U():
            return -1
        lastUpdated = self.update()
        if lastUpdated is None:
            return -1
        while True:
            if self._stop:
                break
            if time() < lastUpdated + 0.2:
                st = lastUpdated + 0.2 - time()
                if st > 0.1:
                    sleep(st)
            lastUpdated = self.update()
            if lastUpdated is None:
                break
        while not makeSureAllClosed(self._threadMap):
            sleep(1)
        return

    def downloadMasterM3U(self) -> bool:
        if 'uri' in self._stream and self._stream['uri'] != '':
            if self._logg:
                self._logg.write(f"{self.name}: GET {self._stream['uri']}", currentframe(), "NicoNico Live Video Downloader Download Master Playlist")
            for i in range(4):
                try:
                    re = self._r.get(self._stream['uri'])
                    break
                except:
                    if self._logg:
                        self._logg.write(f"{self.name}:\nFailed {i+1} times.\n{format_exc()}", currentframe(), "NicoNico Video Live Downloader Download Failed")
                    if i == 3:
                        return False
            if self._logg:
                self._logg.write(f"{self.name}: status = {re.status_code}\n{re.text}", currentframe(), "NicoNico Live Video Downloader Master Playlist")
            if re.status_code >= 400:
                return False
            li = parseSimpleMasterM3U(re.text, self._stream['uri'])
            self._pl = li
            if self._logg:
                self._logg.write(f"{self.name}: li = {li}", currentframe(), "NicoNico Live Video Downloader Playlist")
            return True
        else:
            return False

    def downloadPlaylist(self) -> List[str]:
        if len(self._pl) > 0:
            url = self._pl[0]
            if self._logg:
                self._logg.write(f"{self.name}: GET {url}", currentframe(), "NicoNico Live Video Get Playlist")
            for i in range(4):
                try:
                    re = self._r.get(url)
                    break
                except:
                    if self._logg:
                        self._logg.write(f"{self.name}:\nFailed {i+1} times.\n{format_exc()}", currentframe(), "NicoNico Video Live Downloader Download Failed")
                    if i == 3:
                        return None
            if self._logg:
                self._logg.write(f"{self.name}: status = {re.status_code}\n{re.text}", currentframe(), "NicoNico Live Video Get Playlist Result")
            li = parseSimpleMasterM3U(re.text, url)
            if self._logg:
                self._logg.write(f"{self.name}: li = {li}", currentframe(), "NicoNico Live Video Get Playlist TS List")
            return li if len(li) > 0 else None
        else:
            return None

    def genUrl(self, startIndex: int, endIndex: int, url: str) -> List[str]:
        if endIndex < startIndex:
            return []
        base = urlsplit(url)
        bn = splitfn(base.path)[0]
        r = []
        for i in range(startIndex + 1, endIndex + 1):
            new = SplitResult(base.scheme, base.netloc, f"{bn}/{i}.ts", base.query, base.fragment)
            r.append(urlunsplit(new))
        return r

    def update(self) -> int:
        t = time()
        li = self.downloadPlaylist()
        if li is None:
            return None
        m = self._mts
        for i in li:
            t = urlsplitfn(i)
            if t[:-3].isnumeric():
                t = int(t[:-3])
                if m == -1:
                    m = t - 1
                    self._mts = t - 1
                if t > m:
                    m = t
        if m == self._mts:
            return t
        r = self.genUrl(self._mts, m, li[0])
        self._mts = m
        dirN = f"{self._dirName}/{self._stream['quality']}"
        if not exists(dirN):
            mkdir(dirN)
        ts = TSDownloader(f"{self._tname},{self._tc}", self._r, dirN, r, self._dp, self._logg)
        self._threadMap[self._tc] = ts
        ts.start()
        self._tc += 1
        return t


class TSDownloader(Thread):
    def __init__(self, name: str, r: Session, dirName: str, urls: List[str], dp: DownloadProcess, logg: Logger):
        Thread.__init__(self, name=f"TSDownloader:{name}")
        self._r = r
        self._dirName = dirName
        self._urls = urls
        self._dp = dp
        self._logg = logg

    def run(self):
        for url in self._urls:
            self.download(url)

    def download(self, url: str):
        if self._logg:
            self._logg.write(f"{self.name}: GET {url}", currentframe(), "TS Downloader Request TS")
        for i in range(4):
            try:
                re = self._r.get(url)
                break
            except:
                if self._logg:
                    self._logg.write(f"{self.name}:\nFailed {i+1} times.\n{format_exc()}", currentframe(), "TS Downloader Download Failed")
                    if i == 3:
                        return
        fn = f"{self._dirName}/{urlsplitfn(url)}"
        try:
            with open(fn, 'wb') as f:
                c = f.write(re.content)
            if self._logg:
                self._logg.write(f"{self.name}: write {c} bytes to \"{fn}\"", currentframe(), "TS Downloader Ok")
            self._dp.add(c)
        except:
            if self._logg:
                self._logg.write(f"{self.name}:\n{format_exc()}", currentframe(), "TS Downloader Write Failed")


class FfmpegM3UDownloader(Thread):
    def __init__(self, name: str, fileName: str, data: dict, streams: dict, logg: Logger, imgs: int, imgf: str, oll: autoopenfilelist):
        Thread.__init__(self, name=f"FfmpegDownloader:{name}")
        self._tname = name
        self._fileName = fileName
        self._streams = streams
        self._logg = logg
        self._data = data
        self._tempf = None
        self._imgs = imgs
        self._imgf = imgf
        self._oll = oll

    def run(self):
        try:
            self.callffmpeg()
        except KeyboardInterrupt:
            pass
        except:
            if self._logg:
                self._logg.write(format_exc(), currentframe(), "NicoNico Live Video Download Ffmpeg Downloader Error")
        if self._tempf:
            remove(self._tempf)

    def callffmpeg(self):
        vf = splitext(self._fileName)[1][1:]
        imga = ""
        imga2 = ""
        nss = ""
        if self._imgs == 0:
            if vf == "mkv":
                imga = f' -attach "{self._imgf}" -metadata:s:t mimetype=image/jpeg'
            else:
                imga = f' -i "{self._imgf}"'
                imga2 = ' -map 2 -c:v:1 mjpeg -disposition:v:1 attached_pic'
        self._tempf = getLiveMetaFile(self._tname, self._data, vf, self._streams['quality'])
        if vf == "mkv":
            ml = f"""ffmpeg -i "{self._streams['uri']}" -i "{self._tempf}"{imga} -map 0 -map_metadata 1 -c copy "{self._fileName}"{nss}"""
        elif vf == "mp4":
            ml = f"""ffmpeg -i "{self._streams['uri']}" -i "{self._tempf}"{imga} -map 0 -map_metadata 1 -c copy{imga2} "{self._fileName}"{nss}"""
        if self._logg:
            with open(self._tempf, 'r', encoding='utf8') as te:
                self._logg.write(f"{self.name}: METADATAFILE '{self._tempf}'\n{te.read()}", currentframe(), "NicoNico Live Video Download Metadata")
            self._logg.write(f"{self.name}: ml = {ml}", currentframe(), "NicoNico Live Video Download FFmpeg Command Line")
        re = system(ml)
        if self._logg:
            self._logg.write(f"re = {re}", currentframe(), "NicoNico Live Video Download FFmpeg Return")
        if re == 0 or re == 255:
            self._oll.add(self._fileName)
        tfn = self._tempf
        self._tempf = None
        remove(tfn)
