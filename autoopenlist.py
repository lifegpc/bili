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
from os.path import abspath, exists, isfile
from platform import system
from inspect import currentframe
if system() == "Windows":
    from win32com.shell import shell  # pylint: disable=import-error no-name-in-module


class autoopenfilelist:
    __fl = None
    __logg = None

    def __init__(self, logg=None):
        self.__fl = []
        self.__logg = logg

    def add(self, fn: str):
        r = abspath(fn)
        self.__fl.append(r)
        if self.__logg is not None:
            self.__logg.write(
                f"Add '{r}' to download file list.", currentframe(), "Auto Open File List Add")

    def open(self):
        i = len(self.__fl) - 1
        r = ""
        while i >= 0:
            fn = self.__fl[i]
            if exists(fn) and isfile(fn):
                r = fn
                break
            i = i - 1
        if r != "":
            if system() == "Windows":
                if self.__logg is not None:
                    self.__logg.write(
                        f"Try open '{r}'.", currentframe(), "Auto Open File List Open")
                d = shell.SHParseDisplayName(r, 0)
                shell.SHOpenFolderAndSelectItems(d[0], [], 0)
