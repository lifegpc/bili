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
from platform import system
from JSONParser import loadset
from lang import getdict, getlan
import sys
from os.path import abspath, exists, split
if system() == "Windows":
    import winreg
    import ctypes
import traceback

lan = None
se = loadset()
if se == -1 or se == -2:
    se = {}
lan = getdict('bilischeme', getlan(se, {}))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def DeleteKey(key, sub_key):
    k = winreg.OpenKey(key, sub_key, access=winreg.KEY_ALL_ACCESS)
    i = 0
    while True:
        try:
            v = winreg.EnumKey(k, i)
        except OSError:
            break
        DeleteKey(k, v)
        i = i + 1
    winreg.CloseKey(k)
    try:
        winreg.DeleteKey(key, sub_key)
    except:
        DeleteKey(key, sub_key)


def main():
    classRoot = None
    try:
        classRoot = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
    except OSError:
        pass
    if classRoot:
        found = False
        try:
            bili = winreg.OpenKey(classRoot, 'bili')
            found = True
        except OSError:
            pass
        if found:
            try:
                DeleteKey(classRoot, 'bili')
            except OSError:
                traceback.print_exc()
                print(lan['CNOTDEL'])
                return -1
        try:
            winreg.SetValue(classRoot, 'bili', winreg.REG_SZ,
                            'URL:Bili Protocol')
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili'))
            return -2
        try:
            bili = winreg.OpenKey(
                classRoot, 'bili', access=winreg.KEY_ALL_ACCESS)
        except OSError:
            traceback.print_exc()
            print(lan['REGERR'])
            return -1
        try:
            winreg.SetValueEx(bili, 'URL Protocol', 0, winreg.REG_SZ, '')
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili/URL Protocol'))
            return -2
        iconf = sys.executable
        if exists('icon/favicon.ico'):
            iconf = abspath('icon/favicon.ico')
        elif sys.executable == abspath(sys.argv[0]):
            iconf = f"{split(sys.executable)[0]}\\start.exe"
        try:
            winreg.SetValue(bili, 'DefaultIcon', winreg.REG_SZ, f'"{iconf},1"')
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili/DefaultIcon'))
            return -2
        try:
            shell = winreg.CreateKey(bili, 'shell')
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili/shell'))
            return -2
        try:
            ropen = winreg.CreateKey(shell, 'open')
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili/shell/open'))
            return -2
        cm = f'"{sys.executable}"'
        if sys.executable != abspath(sys.argv[0]):
            fl = split(abspath(sys.argv[0]))[0]
            fl = f"{fl}\\start.py"
            cm = f'{cm} "{fl}"'
        else:
            cm = f'"{split(sys.executable)[0]}\\start.exe"'
        cm = f'{cm} -c -b "%1"'
        try:
            winreg.SetValue(ropen, 'command', winreg.REG_SZ, cm)
        except OSError:
            traceback.print_exc()
            print(lan['CNOTCRE'].replace('<key>', 'bili/shell/open/command'))
            return -2
    else:
        print(lan['REGERR'])
        return -1
    return 0


if __name__ == "__main__":
    if system() == "Windows":
        try:
            if is_admin():
                if main():
                    input()
            else:
                if sys.executable != abspath(sys.argv[0]):
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, f'"{abspath(sys.argv[0])}"', None, 1)
                else:
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, None, None, 1)
        except:
            traceback.print_exc()
            input()
    else:
        print(lan['UNSPT'].replace('<platform>', system()))
