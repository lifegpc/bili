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
from file import filtern, spfln, mkdir, filterd, spfn
from os.path import exists, abspath
from biliVersion import getversion
import sys
from typing import TextIO
from inspect import getframeinfo
from biliTime import tostr2
try:
    import winreg
except ModuleNotFoundError:
    pass


class Logger:
    __f: TextIO = None
    __temstr = None
    __index = None
    __fn = None
    __fsize = None
    __tsize = None
    limit_size = 20 * 2 ** 20
    temp_limit = 2 ** 10

    def __init__(self, s: str = None, fn: str = None):
        if fn is not None:
            self.openf(fn)
        self.__temstr = []
        self.__initinfo()
        self.__index = 1
        if s is not None:
            pass

    def write(self, s: str, c=None, c2: str = None):
        if c is not None:
            z = '' if c2 is None else f" ({c2})"
            t = getframeinfo(c)
            self.__temstr.append(
                f"LOG {tostr2()} File \"{t.filename}\" Line {t.lineno} Function {t.function}{z}:")
        elif c is not None:
            self.__temstr.append(f"LOG {tostr2()} {c2}:")
        else:
            self.__temstr.append(f"LOG {tostr2()}:")
        self.__temstr.append(s)
        self.__writetof()
        if self.__f and self.__tsize > self.temp_limit:
            self.flush()

    def openf(self, fn: str):
        if self.__f is not None:
            self.__f.close()
            self.__f = None
        rfd, rfn = spfln(fn)
        rfd = filterd(rfd)
        rfn = filtern(rfn)
        if not exists(rfd):
            mkdir(rfd)
        self.__f = open(f"{rfd}{rfn}", 'w', encoding='utf8')
        if self.__index == 1:
            self.__fn = f"{rfd}{rfn}"
        self.__fsize = 0
        self.__tsize = 0

    def closef(self):
        if self.__f is not None:
            self.flush()
            self.__f.close()
            if self.__f.closed:
                self.__f = None
                return True
            return False
        return False

    def flush(self):
        if self.__f is None:
            return False
        self.__writetof()
        self.__f.flush()
        self.__tsize = 0
        return True

    def hasf(self):
        return False if self.__f is None else True

    def __writetof(self):
        if self.__f is None:
            return
        for s in self.__temstr:
            i = self.__f.write(f'{s}\n')
            self.__fsize = self.__fsize + i
            self.__tsize = self.__tsize + i
            if self.__fsize >= self.limit_size:
                fn, fd = spfn(self.__fn)
                self.__index = self.__index + 1
                fn = f"{fn}_{self.__index}"
                if fd != "":
                    fn = f"{fn}.{fd}"
                self.openf(fn)
        self.__temstr = []

    def __issetupbili(self):
        ue = exists('unins000.exe')
        self.__temstr.append(f'Unins000.exe exists: {ue}')
        self.__getsetupinfo(
            "9007D20E-3623-49D5-B70D-3538417517DC", "Have setup bili")
        self.__getsetupinfo(
            "5F2B56DE-6400-4AF2-944A-C740BC1A526B", "Have setup bili x86")
        self.__getsetupinfo(
            "B886A88E-C946-411B-A171-6EC7A1752626", "Have setup bili x64")

    def __getsetupinfo(self, key: str, out: str):
        if winreg:
            localmach = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            found = False
            try:
                re = winreg.OpenKey(
                    localmach, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{%s}_is1' % (key))
                found = True
            except FileNotFoundError:
                pass
            if not found:
                try:
                    re = winreg.OpenKey(
                        localmach, "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{%s}_is1" % (key))
                    found = True
                except FileNotFoundError:
                    pass
            self.__temstr.append(f'{out}: {found}')
            if found:
                i = 0
                bs = True
                while bs:
                    try:
                        v = winreg.EnumValue(re, i)
                        self.__temstr.append(f"{v[0]} ({v[2]}): {v[1]}")
                        i = i + 1
                    except OSError:
                        bs = False

    def __initinfo(self):
        self.__temstr.append(f"bili Version: {getversion()}")
        self.__temstr.append(f"Execuble: {sys.executable}")
        self.__temstr.append(f"Python Version: {sys.version}")
        syst = sys.platform
        self.__temstr.append(f"System Platform: {syst}")
        if syst == "win32":
            wv = sys.getwindowsversion()
            self.__temstr.append(
                f"Windows Version: Windows {wv.major}.{wv.minor} build {wv.build} platform {wv.platform} pack {wv.service_pack}")
            self.__issetupbili()
        self.__temstr.append(f"Current Directory: {abspath('.')}")
        self.__temstr.append(f"Argv: {sys.argv}")
