# (C) 2019-2020 lifegpc
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
from Logger import Logger
from inspect import currentframe


def checkCid(data: dict, r: Session, logg: Logger = None) -> bool:
    if 'cid' in data and data['cid'] > 0:  # 有CID并且应该是有效的
        return True
    uri = f"https://api.bilibili.com/x/player/pagelist?bvid={data['bvid']}&jsonp=jsonp"
    if logg is not None:
        logg.write(f"GET {uri}", currentframe(),
                   "Check Audio Cid Get Pagelist")
    re = r.get(uri)
    re.encoding = 'utf8'
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}",
                   currentframe(), "Check Audio Cid Get Pagelist Result")
    re = re.json()
    if re['code'] != 0:
        print(f"{re['code']} {re['message']}")
        return False
    re = re['data']
    if len(re) > 0:
        if len(re) == 1:
            if 'cid' in re[0] and re[0]['cid'] > 0:
                data['cid'] = re[0]['cid']
                return True
        drt = []
        for d in re:
            drt.append({d['cid']: d['duration']})
        tt = {-1: data['duration']}
        drt.append(tt)

        def taken(elem: dict):
            for i in elem.keys():
                return elem[i]
        drt.sort(key=taken)
        k = drt.index(tt)
        ind = 0
        if k == len(drt) - 1:
            ind = k - 1
        elif k == 0:
            ind = 1
        elif (taken(drt[k + 1]) - taken(tt)) >= (taken(tt) - taken(drt[k - 1])):
            ind = k - 1
        else:
            ind = k + 1
        if 'cid' in re[ind] and re[ind]['cid'] > 0:
            data['cid'] = re[ind]['cid']
            return True
    return False
