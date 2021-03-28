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
from ctypes.wintypes import HWND, DWORD, HINSTANCE, WORD, LPARAM, WPARAM, LPVOID
from ctypes import Structure, windll, c_wchar_p, c_int, c_uint, WINFUNCTYPE, sizeof, byref, create_unicode_buffer, cast
from typing import List, Tuple
from os.path import split as splitfn
LPCTSTR = LPTSTR = c_wchar_p
LPOFNHOOKPROC = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
OFN_ENABLESIZING = 0x00800000
OFN_PATHMUSTEXIST = 0x00000800
OFN_OVERWRITEPROMPT = 0x00000002
OFN_NOCHANGEDIR = 0x00000008
OFN_ALLOWMULTISELECT = 0x00000200
OFN_EXPLORER = 0x00080000
MAXPATH = 10240
ExtFilterList = List[Tuple[str]]


class OPENFILENAMEW(Structure):
    _fields_ = [("lStructSize", DWORD), ("hwndOwner", HWND), ("hInstance", HINSTANCE), ("lpstrFilter", LPCTSTR), ("lpstrCustomFilter", LPTSTR), ("nMaxCustFilter", DWORD), ("nFilterIndex", DWORD), ("lpstrFile", LPTSTR), ("nMaxFile", DWORD), ("lpstrFileTitle", LPTSTR), ("nMaxFileTitle", DWORD), ("lpstrInitialDir", LPCTSTR), ("lpstrTitle", LPCTSTR), ("Flags", DWORD), ("nFileOffset", WORD), ("nFileExtension", WORD), ("lpstrDefExt", LPCTSTR), ("lCustData", LPARAM), ("lpfnHook", LPOFNHOOKPROC), ("lpTemplateName", LPCTSTR), ("pvReserved", LPVOID), ("dwReserved", DWORD), ("FlagsEx", DWORD)]


def extFilterListToStr(extFilterList: ExtFilterList):
    s = ""
    for i in extFilterList:
        s += f"{i[0]}({i[1]})\0{i[1]}\0"
    s += "\0"
    return s


def getOpenFileName(defaultPath: str = None, defaultExt: str = None, extFilterList: ExtFilterList = None, allowMultiSelect: bool = False):
    try:
        w = OPENFILENAMEW()
        w.lStructSize = sizeof(OPENFILENAMEW)
        w.nMaxFile = MAXPATH
        w.nMaxFileTitle = MAXPATH
        w.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR
        if allowMultiSelect:
            w.Flags = w.Flags | OFN_ALLOWMULTISELECT | OFN_EXPLORER
        fn = create_unicode_buffer("", MAXPATH)
        if extFilterList is not None:
            efs = extFilterListToStr(extFilterList)
            eft = create_unicode_buffer(efs, MAXPATH)
            w.lpstrFilter = cast(eft, LPCTSTR)
        w.lpstrFile = cast(fn, LPTSTR)
        if defaultExt is not None:
            w.lpstrDefExt = defaultExt
        if defaultPath is not None:
            tifn = create_unicode_buffer(defaultPath, MAXPATH)
            w.lpstrInitialDir = cast(tifn, LPCTSTR)
        if not windll.comdlg32.GetOpenFileNameW(byref(w)):
            return None
        if w.lpstrFile == '':
            if allowMultiSelect:
                return []
            else:
                return ''
        elif not allowMultiSelect:
            return {"a": w.lpstrFile, "f": splitfn(w.lpstrFile)[1]}
        else:
            r = []
            nunum = 0
            tfn = ''
            for i in fn:
                if nunum == 2:
                    break
                if i == '\0':
                    nunum += 1
                    if tfn != '':
                        r.append(tfn)
                        tfn = ''
                else:
                    nunum = 0
                    tfn += i
            if len(r) == 1:
                return [{"a": r[0], "i": splitfn(r[0])[1]}]
            else:
                r2 = []
                for i in r[1:]:
                    r2.append({"a": f"{r[0]}\\{i}", "f": i})
                return r2
    except:
        return None


def getSaveFileName(defaultPath: str = None, defaultName: str = None, defaultExt: str = None, extFilterList: ExtFilterList = None):
    try:
        w = OPENFILENAMEW()
        w.lStructSize = sizeof(OPENFILENAMEW)
        w.nMaxFile = MAXPATH
        w.nMaxFileTitle = MAXPATH
        w.Flags = OFN_ENABLESIZING | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR | OFN_OVERWRITEPROMPT
        ofn = '' if defaultName is None else defaultName
        fn = create_unicode_buffer(ofn, MAXPATH)
        if extFilterList is not None:
            efs = extFilterListToStr(extFilterList)
            eft = create_unicode_buffer(efs, MAXPATH)
            w.lpstrFilter = cast(eft, LPCTSTR)
        w.lpstrFile = cast(fn, LPTSTR)
        if defaultExt is not None:
            w.lpstrDefExt = defaultExt
        if defaultPath is not None:
            tifn = create_unicode_buffer(defaultPath, MAXPATH)
            w.lpstrInitialDir = cast(tifn, LPCTSTR)
        if not windll.comdlg32.GetSaveFileNameW(byref(w)):
            return None
        if w.lpstrFile != '':
            return {"a": w.lpstrFile, "f": splitfn(w.lpstrFile)[1]}
    except:
        return None
