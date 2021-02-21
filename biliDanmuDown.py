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
from inspect import currentframe
from traceback import format_exc


def downloadn(cid, r, logg=None):
    "下载当前弹幕"
    uri = f"https://comment.bilibili.com/{cid}.xml"
    try:
        if logg is not None:
            logg.write(f"GET {uri}", currentframe(), "Download Barrage Request")
        re = r.get(uri)
    except:
        if logg is not None:
            logg.write(format_exc(), currentframe(), "Download Barrage Failed")
        return -1
    re.encoding = 'utf8'
    if logg is not None:
        if re.ok:
            logg.write(f"status = {re.status_code}", currentframe(), "Download Barrage Result")
        else:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Download Barrage Result2")
    return re.text if re.ok else -1


def downloadh(cid, r, date, logg=None):
    "下载历史弹幕"
    uri = f"https://api.bilibili.com/x/v2/dm/history?type=1&date={date}&oid={cid}"
    if logg is not None:
        logg.write(f"GET {uri}", currentframe(), "Download History Barrage Request")
    try:
        re = r.get(uri)
    except:
        if logg is not None:
            logg.write(format_exc(), currentframe(), "Download History Barrage Failed")
        return -1
    if logg is not None:
        if re.ok:
            logg.write(f"status = {re.status_code}", currentframe(), "Download History Barrage Result")
        else:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Download History Barrage Result2")
    re.encoding = 'utf8'
    return re.text if re.ok else -1
