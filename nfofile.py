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
from xml.dom import minidom
from os.path import dirname, exists, splitext
from os import remove
from file import mkdir
from biliTime import tostr4, getDate
from time import strptime, mktime, struct_time, strftime
from re import match


class NFOActor:
    actorName = None
    actorRole = 'uploader'
    actorThumb = None


class NFOMetadata:
    def __init__(self):
        self._title = None
        self._premiered = None
        self._plot = None
        self.runtime = 0
        self._id = None
        self.genre = []
        self.actors = []

    @property
    def title(self) -> str:
        return self._title if self._title is not None else ''

    @title.setter
    def title(self, value):
        if value is not None:
            v = str(value)
            if v != '':
                self._title = v

    @property
    def premiered(self) -> str:
        "日期"
        return tostr4(self._premiered) if self._premiered is not None else ''

    @premiered.setter
    def premiered(self, value):
        if isinstance(value, int):
            self._premiered = value
        elif isinstance(value, str):
            if match(r'^[+-]?[0-9]$', value):
                self._premiered = int(value)
            elif match(r'^[0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}$', value):
                try:
                    self._premiered = int(mktime(strptime(value, '%Y-%m-%d')))
                except OverflowError:
                    self._premiered = None
        elif isinstance(value, struct_time):
            try:
                self._premiered = int(mktime(value))
            except OverflowError:
                self._premiered = None

    @property
    def year(self) -> str:
        return strftime('%Y', getDate(self._premiered)) if self._premiered is not None else ''

    @property
    def plot(self) -> str:
        "视频描述"
        return self._plot if self._plot is not None else ''

    @plot.setter
    def plot(self, value):
        if value is not None:
            v = str(value)
            if v != '':
                self._plot = v

    @property
    def id(self) -> str:
        return self._id if self._id is not None else ''

    @id.setter
    def id(self, value):
        if value is not None:
            v = str(value)
            if v != '':
                self._id = v


class NFOFile:
    def __init__(self):
        self.new()

    def new(self):
        self.metadata = NFOMetadata()
        self.doc = minidom.Document()
        self.root = self.doc.createElement("movie")

    def save(self, fn: str):
        self.update()
        pn = dirname(fn)
        if not exists(pn):
            mkdir(pn)
        a = splitext(fn)
        fn = a[0] + '.nfo'
        if exists(fn):
            remove(fn)
        with open(fn, 'w', encoding='utf8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>')
            f.write(self.root.toxml())

    def update(self):
        self.root.childNodes = []
        title = self.doc.createElement('title')
        title.appendChild(self.doc.createTextNode(self.metadata.title))
        self.root.appendChild(title)
        year = self.doc.createElement('year')
        year.appendChild(self.doc.createTextNode(self.metadata.year))
        self.root.appendChild(year)
        premiered = self.doc.createElement('premiered')
        premiered.appendChild(self.doc.createTextNode(self.metadata.premiered))
        self.root.appendChild(premiered)
        plot = self.doc.createElement('plot')
        plot.appendChild(self.doc.createTextNode(self.metadata.plot))
        self.root.appendChild(plot)
        runtime = self.doc.createElement('runtime')
        runtime.appendChild(self.doc.createTextNode(str(self.metadata.runtime)))
        self.root.appendChild(runtime)
        vid = self.doc.createElement('id')
        vid.appendChild(self.doc.createTextNode(self.metadata.id))
        self.root.appendChild(vid)
        for tag in self.metadata.genre:
            if isinstance(tag, str):
                genre = self.doc.createElement('genre')
                genre.appendChild(self.doc.createTextNode(tag))
                self.root.appendChild(genre)
        for actor in self.metadata.actors:
            if isinstance(actor, NFOActor):
                if actor.actorName is None:
                    continue
                actore = self.doc.createElement('actor')
                actorN = self.doc.createElement('name')
                actorN.appendChild(self.doc.createTextNode(actor.actorName))
                actore.appendChild(actorN)
                actorRole = '' if actor.actorRole is None else actor.actorRole
                actorR = self.doc.createElement('role')
                actorR.appendChild(self.doc.createTextNode(actorRole))
                actore.appendChild(actorR)
                actorThumb = '' if actor.actorThumb is None else actor.actorThumb
                actorT = self.doc.createElement('thumb')
                actorT.appendChild(self.doc.createTextNode(actorThumb))
                actore.appendChild(actorT)
                self.root.appendChild(actore)
