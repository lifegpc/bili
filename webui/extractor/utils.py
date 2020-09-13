# (C) 2019-2020 lifegpc
# This file is part of bili.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from requests import Session
import traceback


def addcookies(r: Session, vq: int = 120):
    "增加具体的cookies,vq为视频画质"
    r.cookies.set('CURRENT_QUALITY', str(vq), domain='.bilibili.com', path='/')
    r.cookies.set('CURRENT_FNVAL', '16', domain='.bilibili.com', path='/')
    r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
    r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')


def geturllength(r: Session, url: str) -> int:
    "获取URI的长度"
    try:
        re = r.get(url, stream=True)
        try:
            if re.headers.get('Content-Length') is not None:
                a = int(re.headers.get('Content-Length'))
                re.close()
                return a
            else:
                re.close()
                return 0
        except:
            re.close()
            print(traceback.format_exc())
            return 0
    except:
        print(traceback.format_exc())
        return 0
