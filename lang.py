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
import polib
from os.path import exists
import platform
import ctypes
dll=None
lan={'en':'English','zh_CN':'中文（中国）'}
def getdict(sn:str,lan:str) -> dict:
    """获取翻译词典
    sn 资源名称
    lan 语言代码"""
    if lan=="en" :
        fn=f"Language/bili.{sn}.pot"
    else :
        fn=f"Language/bili.{sn}.{lan}.po"
    if not exists(fn) :
        print(f'Can not find the language resource file:"{fn}"')
        fn=f'Language/bili.{sn}.pot'
        if not exists(fn) :
            print(f'Can not find the language resource file:"{fn}"')
            return -1
    po=polib.pofile(fn,encoding='utf8')
    r={}
    for i in po.translated_entries() :
        r[i.msgctxt]=i.msgstr
    for i in po.untranslated_entries() :
        r[i.msgctxt]=i.msgid
    return r
def getsyslan(d:bool=False) :
    """获取系统语言信息
    语言代码：https://docs.microsoft.com/zh-cn/previous-versions/system-center/system-center-2012-R2/dn281927(v=sc.12)
    d 是否为调试模式"""
    s=platform.system()
    if s=="Windows" :
        global dll
        if dll==None :
            dll=ctypes.windll.kernel32
        l=dll.GetSystemDefaultUILanguage()
        if d:
            print(f"SystemDefaultUILanguage:{hex(l)}")
        if l==2052:
            r="zh_CN"
        else :
            r="en"
        if d:
            global lan
            print(f'Choose {r} : {lan[r]}')
        return r
    else :
        return "en" #非Windows系统默认英文
def getlan(se:dict,ip:dict) :
    l=getsyslan()
    if 'lan' in se:
        l=se['lan']
    if 'lan' in ip:
        l=ip['lan']
    return l
if __name__ == "__main__":
    print(getdict('start','en'))
    print(getdict('start',getsyslan(True))) #测试是否工作
