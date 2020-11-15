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
from file import spfn
from requests import Session
from biliTime import tostr3, tostr5, comlrct
import os
from lang import getlan,getdict
import sys
from command import gopt
import JSONParser
from ASSWriter import ASSScript, parsefromCSSHex, ASSScriptEvent
import traceback
from iso639 import languages
from bstr import lg
from inspect import currentframe
from traceback import format_exc


lan=None
se=JSONParser.loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('biliSub',getlan(se,ip))


def getiso6392t(s: str) -> str:
    t = s.split('_')[0]
    t = s.split('-')[0]
    try:
        return languages.get(alpha2=t).part2t
    except:
        return s


def downsub(r: Session,fn: str,i: dict,ip: dict,se: dict,data: dict,pr: bool = False,pi: int = 1, width: int = None, height: int = None):
    "下载字幕"
    ass = False
    if JSONParser.getset(se, 'ass') == True:
        ass = True
    if 'ass' in ip:
        ass = ip['ass']
    global lan
    fq=spfn(fn)[0]
    if not ass:
        fn = f"{fq}.{i['lan']}.srt"
    else:
        fn = f"{fq}.{i['lan']}.ass"
    i['fn']=fn
    if os.path.exists(fn) :
        fg=False
        bs=True
        if 's' in ip:
            fg=True
            bs=False
        if 'y' in se:
            fg = se['y']
            bs = False
        if 'y' in ip :
            fg = ip['y']
            bs = False
        while bs:
            inp=input(f'{lan["INPUT1"]}(y/n)'.replace("<filename>",fn))#"<filename>"文件已存在，是否覆盖？
            if len(inp)>0 :
                if inp[0].lower()=='y' :
                    fg=True
                    bs=False
                elif inp[0].lower()=='n' :
                    bs=False
        if fg:
            try :
                os.remove('%s'%(fn))
            except :
                print(lan['OUTPUT1'])#删除原有文件失败，跳过下载
                return 0
    re=r.get(i['url'])
    re.encoding='utf8'
    re=re.json()
    if not ass:
        if assrt(fn, re['body']) == 0 and pr :
            print(lan['OUTPUT2'].replace('<number>', str(pi)).replace('<languagename>', i['land']))  # 第<number>P<languagename>字幕下载完毕！
    else:
        if width is None:
            width = 1920
        if height is None:
            height = 1080
        if asass(fn, re, width, height) == 0 and pr :
            print(lan['OUTPUT2'].replace('<number>', str(pi)).replace('<languagename>', i['land']))  # 第<number>P<languagename>字幕下载完毕！
    return 0
def assrt(fn:str,b:list):
    "保存至srt格式"
    try :
        f=open(fn,'w',encoding="utf8")
    except :
        print(lan['ERROR1'].replace('<filename>',fn))#保存"<filename>"失败！
        return -1
    i=1
    for k in b:
        try :
            f.write('%s\n'%(i))
            f.write('%s --> %s\n'%(tostr3(k['from']),tostr3(k['to'])))
            f.write('%s\n\n'%(k['content']))
        except :
            print(lan['ERROR2'].replace('<filename>',fn))#写入到文件"<filename>"时失败！
            f.close()
            return -1
        i=i+1
    f.close()
    return 0
def ffinputstr(i: list, n: int, m: int=-1) -> (str, str):
    "分别解析出ffmpeg输入参数和元数据参数"
    s=""
    r=""
    z=n
    c = 0
    for k in i :
        s=s+' -i "%s"'%(k['fn'])
        r = r + f' -metadata:s:s:{c} language="{getiso6392t(k["lan"])}" -metadata:s:s:{c} title="{k["land"]}" -metadata:s:s:{c} handler_name="{k["land"]}"'
        z=z+1
        c = c + 1
    for i in range(z) :
        if i != m:
            r = r + f' -map {i}'
    return s,r


def asass(fn: str, b: dict, width: int, height: int):
    d = ASSScript()
    d.Script_Info.Title = fn
    d.Script_Info.PlayResX = width
    d.Script_Info.PlayResY = height
    d.V4_Styles[0].Fontname = '微软雅黑'
    d.V4_Styles[0].set_Fontsize(28 * width / 1139)
    try:
        d.V4_Styles[0].PrimaryColour = parsefromCSSHex(b['font_color'])
    except:
        print(traceback.format_exc())
    d.Events = []
    loc = 2
    for i in b['body']:
        if loc != i['location']:
            t = "{\\an%s}%s" % (i['location'], i['content'])
        else:
            t = i['content']
        d.Events.append(ASSScriptEvent(i['from'] * 1000, i['to'] * 1000, t))
    try:
        f = open(fn, 'w', encoding = "utf8")
    except:
        print(lan['ERROR1'].replace('<filename>' ,fn))  # 保存"<filename>"失败！
        return -1
    try:
        f.write(d.dump())
    except:
        print(lan['ERROR2'].replace('<filename>', fn))  # 写入到文件"<filename>"时失败！
        f.close()
        return -1
    f.close()
    return 0


def downlrc(r: Session, fn: str, i: dict, ip: dict, se: dict, data: dict,pr: bool=False, pi: int=1, nal: bool=False):
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    global lan
    fq = spfn(fn)[0]
    if nal:
        fn = f"{fq}.lrc"
    else:
        fn = f"{fq}.{i['lan']}.lrc"
    if log:
        logg.write(f"fn = {fn}", currentframe(), "Download Lyrics Var1")
    i['fn'] = fn
    if os.path.exists(fn):
        fg = False
        bs = True
        if 's' in ip:
            fg = True
            bs = False
        if 'y' in se:
            fg = se['y']
            bs = False
        if 'y' in ip :
            fg = ip['y']
            bs = False
        while bs:
            inp = input(f'{lan["INPUT1"]}(y/n)'.replace("<filename>", fn))  # "<filename>"文件已存在，是否覆盖？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    fg = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if fg:
            try:
                os.remove('%s'%(fn))
            except:
                if log:
                    logg.write(format_exc(), currentframe(), "Download Lyrics Remove File Failed")
                print(lan['OUTPUT1'])  # 删除原有文件失败，跳过下载
                return 0
    if log:
        logg.write(f"GET {i['url']}", currentframe(), "Download Lyrics JSON")
    re = r.get(i['url'])
    re.encoding = 'utf8'
    if log:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Download Lyrics JSON Result")
    re = re.json()
    if aslrc(fn, re['body'], se, ip, data, pi) == 0 and pr:
        print(lan['OUTPUT3'].replace('<number>', str(pi)).replace('<languagename>', i['land']))  # 第<number>P<languagename>歌词下载完毕！
    return 0


def aslrc(fn: str, b: list, se: dict, ip: dict, data: dict, pi: int):
    log = False
    logg = None
    if 'logg' in ip:
        log = True
        logg = ip['logg']
    try :
        f = open(fn, 'w', encoding="utf8")
    except :
        if log:
            logg.write(format_exc(), currentframe(), "Convert To Lyrics Open File Failed")
        print(lan['ERROR1'].replace('<filename>', fn))  # 保存"<filename>"失败！
        return -1
    lmd = 10
    if 'lmd' in se:
        lmd = se['lmd']
    if 'lmd' in ip:
        lmd = se['ip']
    lmd = lmd / 1000
    if log:
        logg.write(f"lmd = {lmd}", currentframe(), "Convert To Lyrics Var")
    f.write("[re:Made by bili. https://github.com/lifegpc/bili]\n")
    tit = data['page'][pi - 1]['part']
    if tit == "":
        tit = data['title']
    f.write(f"[ti:{lg(tit)}]\n")
    f.write(f"[ar:{lg(data['name'])}]\n")
    f.write(f"[al:{lg(data['title'])}]\n")
    et = -1
    for k in b:
        if et != -1 and comlrct(et, k['from']) == -1:
            f.write(f"[{tostr5(et)}]\n")
        con = k['content']
        col = con.split('\n')
        t = 0
        for s in col:
            s = s.replace('\r', '')
            f.write(f"[{tostr5(k['from'] + lmd * t)}]{s}\n")
            t = t + 1
        et = k['to']
    f.close()
    return 0
