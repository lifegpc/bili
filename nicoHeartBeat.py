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
from time import time
from Logger import Logger
from json import dumps
from inspect import currentframe


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
