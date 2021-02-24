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
from hashl import crc32
from requests import Session
from Logger import Logger
from inspect import currentframe


def convertToBiliVer(dm: dict) -> dict:
    return {"t": dm["body"], "mod": dm["mode"], "fs": dm["size"], "fc": dm["color"], "ut":
            round(dm["createTime"] / 1000), "dp": dm["danmakuType"], "ti":
            dm["position"] / 1000, "si": crc32(dm["userId"]), "ri": dm["danmakuId"]}


def getDanmuList(r: Session, rid: str, totalCount: int, logg: Logger = None) -> list:
    rel = []
    for page in range(0, 200):
        url = "https://www.acfun.cn/rest/pc-direct/new-danmaku/list"
        data = {"resourceId": rid, "resourceType": "9", "enableAdvanced": "true",
                "pcursor": str(page), "count": "200", "sortType": "1", "asc": "false"}
        if logg:
            logg.write(f"POST {url}\ndata = {data}", currentframe(), "Get Acfun Danmu Page")
        re = r.post(url, data)
        re.encoding = 'utf8'
        if logg:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Acfun Danme Page Result")
        re = re.json()
        if re['result'] != 0:
            print(f"{re['result']} {re['error_msg']}")
            break
        rel += re['danmakus']
        if len(rel) >= totalCount:
            break
    rel2 = []
    for i in rel:
        rel2.append(convertToBiliVer(i))
    return rel2
