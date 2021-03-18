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
from os.path import splitext, exists
from time import time, sleep
from file.info import size as fsize
from file import mkdir
from autoopenlist import autoopenfilelist
from nicoHeartBeat import sendNicoHeartBeat


def downloadNicoM3U(r: Session, url: str, index: int, fn: str, se: dict, ip: dict, session: dict, sessionurl: str):
    '''下载M3U媒体播放列表（NMD要心跳包）
    - url m3u地址
    - index 从几个segment开始
    - fn 文件名
    - se 设置字典
    - ip 名里字典
    - session Session字典
    - sessionurl Session地址
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
    session, lastSendHeartBeat = sendNicoHeartBeat(r, session, sessionurl, logg)
    if session is None:
        return -1, index
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
        if now > lastSendHeartBeat + 90:
            session, lastSendHeartBeat = sendNicoHeartBeat(r, session, sessionurl, logg)
            if session is None:
                return -1, index
        percent = round((index + 1) / le * 100, 2)
        speedn = totalSize / (now - startTime)
        print(f"\r{percent}%({index+1}/{le})\t{fsize(totalSize)}({totalSize}B)\t{round(now-startTime, 2)}s\t{fsize(speedn)}/s({round(speedn)}B/s)", end="")
        if index > startInd + 6 and now < lastTime + (6 / speed):
            sleepTime = lastTime + (6 / speed) - now()
            if sleepTime > 0.1:
                sleep(sleepTime)
            now = time()
        lastTime = now
        index += 1
    return 0, index
