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
import file
try:
    from file import win32
except:
    pass
import biliPlayerXmlParser
from os.path import exists, abspath, split as splitfn
import biliDanmuXmlParser
from os import remove
import biliDanmuXmlFilter
import biliDanmuCreate
from PrintInfo import pr
from JSONParser import loadset, getset
import sys
from lang import getdict, getlan
from biliext import XMLFILE, ALLFILE
lan = None
se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
lan = getdict('filter', getlan(se, ip))
if __name__ != "__main__":
    print(lan['OUTPUT1'])  # 请运行"filter.py"。
else:
    pr()
    read = biliPlayerXmlParser.loadXML()
    xml = read  # 弹幕过滤列表
    if read == -1:
        print(lan['OUTPUT2'].replace('<filename>', 'tv.bilibili.plater.xml'))  # 找不到文件"<filename>"。
        sys.exit(-1)
    se = loadset()
    if not isinstance(se, dict):
        se = None
    o = 'Download/'
    read = getset(se, 'o')
    if read is not None:
        o = read
    bs = True
    try:
        fl = win32.getOpenFileName(defaultPath=abspath(o), extFilterList=[XMLFILE, ALLFILE], allowMultiSelect=True)
        if fl is None:
            fl = []
    except:
        while bs:
            inp = input(lan['INPUT1'])  # 请输入要过滤的文件数量：
            if len(inp) > 0:
                if inp.isnumeric():
                    g = int(inp)
                    bs = False
        fl = file.getfilen(l=o, g=g)
    for i in fl:
        if exists(i['a']):
            try:
                read = biliDanmuXmlParser.loadXML(i['a'])
            except:
                print(lan['INPUT2'])  # 此文件不是弹幕文件。
                continue
            r = read
            try:
                fn = win32.getSaveFileName(defaultPath=splitfn(i['a'])[0], defaultExt="xml", extFilterList=[XMLFILE, ALLFILE])
                if fn == '' or fn is None:
                    continue
            except:
                input(lan['INPUT3'])  # 按Enter开始选择输出文件。
                read = file.getfilen(l=o, save=True)
                if read == -1:
                    read = file.getfilen('.', save=True)
                fn = read[0]
            if exists(fn['a']):
                remove(fn['a'])
            try:
                f = open(fn['a'], mode='w', encoding='utf8')
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (r['chatserver'], r['chatid'], r['mission'], r['maxlimit'], r['state'], r['real_name'], r['source']))
                z = len(r['list'])
                g = 0
                for j in r['list']:
                    if biliDanmuXmlFilter.Filter(j, xml):
                        g = g + 1
                    else:
                        try:
                            f.write(biliDanmuCreate.objtoxml(j))
                        except:
                            print(lan['ERROR1'].replace('<filename>', fn['f']))  # 保存"<filename>"失败！
                            continue
                m = z - g
                print(lan['OUTPUT3'].replace('<all>', str(z)).replace('<fn>', str(g)).replace('<sn>', str(m)))  # 该文件中有<all>条弹幕，过滤了<fn>条，剩余<sn>条。
            except:
                print(lan['ERROR1'].replace('<filename>', fn['f']))  # 保存"<filename>"失败！
                continue
        else:
            print(lan['OUTPUT2'].replace('<filename>', i['f']))  # 找不到文件"<filename>"。
