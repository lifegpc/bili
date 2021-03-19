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
from time import time, sleep
from Logger import Logger
from json import dumps
from inspect import currentframe
from threading import Thread


def sendNicoHeartBeat(r: Session, session: dict, url: str, logg: Logger) -> (dict, int):
    '''NicoNico发送心跳包
    - session Session字典
    - url Session URL
    返回新Session'''
    url = f"{url}/{session['id']}?_format=json&_method=PUT"
    t = round(time() * 1000)
    session['modified_time'] = t
    para = {"session": session}
    if logg:
        logg.write(f"POST {url}\nPOST DATA: {dumps(para)}", currentframe(), "Send HeartBeat")
    re = r.post(url, json=para)
    if logg:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "HeartBeat Result")
    if re.status_code >= 400:
        return None, None
    return re.json()['data']['session'], t / 1000


class nicoNormalVideoHeartBeatThread(Thread):
    def __init__(self, threadName: str, r: Session, session: dict, url: str, logg: Logger):
        Thread.__init__(self, name=f"HeartBeat:{threadName}")
        self._r = r
        self._session = session
        self._url = url
        self._logg = logg
        self._stop = False

    def kill(self):
        self._stop = True
        if self._logg:
            self._logg.write(f"{self.name}: Get Kill Signial", currentframe(), "NicoNico Normal Video Heart Beat Thread Get Kill")

    def run(self):
        self._session, lastSendHeartBeat = sendNicoHeartBeat(self._r, self._session, self._url, self._logg)
        if self._session is None:
            return
        while True:
            if self._stop:
                break
            if time() < lastSendHeartBeat + 90:
                sleep(1)
            else:
                self._session, lastSendHeartBeat = sendNicoHeartBeat(self._r, self._session, self._url, self._logg)
                if self._session is None:
                    return
        if self._logg:
            self._logg.write(f"{self.name}: Exited", currentframe(), "NicoNico Normal Video Heart Beat Thread Killed")
