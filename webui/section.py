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
from . import pa
from os.path import exists
from json import loads, dumps
from hashl import sha256
import time
from os import remove
import traceback


class sectionlist:
    __list = []

    def __init__(self):
        if exists('sections.json'):
            try:
                f = open('sections.json', 'r', encoding='utf8')
                t = f.read()
                f.close()
                self.__list = loads(t)
            except:
                self.__list = []

    def login(self, h, ip) -> (str, int):
        "登录"
        if pa.pas and pa.password() == h:
            now = int(time.time())
            self.__checklist(now)
            now = now + 30 * 24 * 3600  # 保留1个月
            has = sha256(f"{pa.password()}{now}{ip}")
            self.__list.append({"hash": has, "time": now, "ip": ip})
            self.__save()
            return has
        else:
            return None

    def check(self, h):
        "检查是否登录成功"
        if pa.pas and h is not None:
            now = int(time.time())
            read = self.__checklist(now)
            for i in self.__list:
                if i['hash'] == h:
                    if read:
                        self.__save()
                    return True
            if read:
                self.__save()
            return False
        else:
            return False

    def __checklist(self, time: int):
        k = 0
        de = False
        for i in self.__list:
            if time >= i['time'] or sha256(f"{pa.password()}{i['time']}{i['ip']}") != i['hash']:
                del self.__list[k]
                de = True
            k = k + 1
        return de

    def __save(self):
        try:
            if exists('sections.json'):
                remove('sections.json')
            f = open('sections.json', 'w', encoding='utf8')
            f.write(dumps(self.__list))
            f.close()
        except:
            print(traceback.format_exc())
