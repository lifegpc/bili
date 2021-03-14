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
from typing import List
from re import split, match
from hashl import crc32


COLORS = {"white": "#ffffff", "red": "#ff0000", "pink": "#ff8080", "orange": "#ffc000", "yellow": "#ffff00", "green": "#00ff00", "cyan": "#00ffff", "blue": "#0000ff", "purple": "#c000ff", "black": "#000000"}
DEFAULT_COLOR = "#ffffff"
DEFAULT_FONT = "defont"
DEFAULT_POSITION = "naka"  # 中
DEFAULT_SIZE = "medium"
FONTS_ARRAY = ["defont", "gothic", "mincho"]
POSITIONS_ARRAY = ["ue", "naka", "shita"]  # 上中下
PREMIUM_COLORS = {"white2": "#cccc99", "niconicowhite": "#cccc99", "red2": "#cc0033", "truered": "#cc0033", "orange2": "#ff6600", "passionorange": "#ff6600", "yellow2": "#999900", "madyellow": "#999900", "green2": "#00cc66", "elementalgreen": "#00cc66", "blue2": "#3399ff", "marineblue": "#3399ff", "purple2": "#6633cc", "nobleviolet": "#6633cc", "pink2": "#ff33cc", "cyan2": "#00cccc", "black2": "#666666"}
SIZES_ARRAY = ["big", "medium", "small"]


def isColorCodeCommand(s: str) -> bool:
    return match(r'^#([\da-fA-F]{6})$', s)


class NicoDanmu:
    thread: str = ''
    no: int = 0
    content: str = ''
    vpos: int = 0
    mail: List[str] = []
    date: int = 0
    dataUsec: int = 0
    userId: str = ''
    premium: int = 0
    nicoru: int = 0
    lastNicoruDate = None
    valhalla: bool = False
    deletedStatus: int = 0
    anonymous: bool = False
    score: int = 0
    fork: int = 0
    color: str = DEFAULT_COLOR
    size: str = DEFAULT_SIZE
    position: str = DEFAULT_POSITION

    def __init__(self, d: dict):
        self.thread = d['thread']
        self.no = d['no']
        self.content = d['content']
        self.vpos = d['vpos']
        if 'mail' in d:
            self.mail = split(r'\s+', d['mail'])
        self.date = d['date']
        self.dataUsec = d['date_usec']
        self.userId = d['user_id']
        if 'premium' in d:
            self.premium = d['premium']
        if 'nicoru' in d:
            self.nicoru = d['nicoru']
        if 'last_nicoru_date' in d:
            self.lastNicoruDate = d['last_nicoru_date']
        if 'valhalla' in d:
            self.valhalla = d['valhalla'] == 1
        if 'deleted' in d:
            self.deletedStatus = d['deleted']
        if 'anonymity' in d:
            self.anonymous = d['anonymity'] == 1
        if 'score' in d:
            self.score = d['score']
        self.fork = d['fork']
        for i in self.mail:
            if i in POSITIONS_ARRAY:
                self.position = i
            elif i in SIZES_ARRAY:
                self.size = i
            elif i in COLORS:
                self.color = COLORS[i]
            elif i in PREMIUM_COLORS:
                self.color = PREMIUM_COLORS[i]
            elif isColorCodeCommand(i):
                self.color = i

    def getColor(self):
        return int(self.color[1:], 16)

    def getDanmuType(self):
        if self.position == DEFAULT_POSITION:
            return 1
        elif self.position == "ue":
            return 5
        return 4

    def getSize(self):
        if self.size == DEFAULT_SIZE:
            return 25
        elif self.size == "small":
            return 18
        elif self.size == "big":
            return 40

    def toBiliVer(self):
        return {"t": self.content, "mod": self.getDanmuType(), "fs": self.getSize(), "fc": self.getColor(), "ut": self.date, "ti": self.dataUsec / 1000, "si": crc32(self.userId), "ri": self.no}
