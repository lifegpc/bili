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
import sys
import os
import traceback
if '-c' in sys.argv:
    try:
        os.chdir(os.path.abspath(os.path.split(sys.argv[0])[0]))
    except:
        traceback.print_exc()
        input()
import requests
import HTMLParser
import JSONParser
import PrintInfo
import biliLogin
import biliPlayerXmlParser
import biliDanmu
import biliTime
import chon
import videodownload
import biliBv
from re import search, I, match
import os
import sys
from command import gopt
import json
from math import ceil
from dictcopy import copyip, copydict
from biliHdVideo import HDVideoParser
import biliLiveDanmu
from lang import getlan, getdict
import JSONParser2
from threading import Thread
from biliVersion import checkver
from time import sleep, time
from Logger import Logger
from inspect import currentframe
from autoopenlist import autoopenfilelist
from urllib.parse import parse_qs, urljoin
from bstr import hasPar

# 远程调试用代码
# import ptvsd
# ptvsd.enable_attach(("0.0.0.0", 44123))
# ptvsd.wait_for_attach()


NOT_FOUND = -404

lan = None
se = JSONParser.loadset()
if se == -1 or se == -2:
    se = {}
ip = {}


def main(ip={}, menuInfo=None):
    """ip 命令行参数字典
    menuInfo AU号专辑/歌单信息"""
    logg: Logger = ip['logg'] if 'logg' in ip else None
    log = logg is not None
    global se
    global lan
    uc = True  # 是否检测更新
    if JSONParser.getset(se, 'uc') is True:
        uc = False
    if 'uc' in ip:
        uc = ip['uc']
    if uc:
        checkver(logg)
    ns = True
    if 's' in ip:
        ns = False
    if not isinstance(se, dict):
        se = None
        print(f'{lan["RUN_SETTINGS_TIPS"]}')
    nte = False
    if JSONParser.getset(se, 'te') is False:
        nte = True
    if 'te' in ip:
        nte = not ip['te']
    if 'i' in ip:
        inp = ip['i']
    elif ns:
        inp = input(f"{lan['INPUT1']}{lan['OUTPUT13']}")
    else:
        print(f'{lan["ERROR1"]}')
        return -1
    inpl = inp.split(',')
    if log:
        logg.write(f"inp = '{inp}'\ninpl = {inpl}", currentframe(), 'Input URL')
    mt = False
    if JSONParser.getset(se, 'mt') is True:
        mt = True
    if 'mt' in ip:
        mt = ip['mt']
    if len(inpl) != 1:
        for inp2 in inpl:
            ip2 = copydict(ip)
            ip2['i'] = inp2
            ip2['uc'] = False  # 禁用重复检测
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), 'multi-input parameters')
            if mt:
                ru = mains(ip2)
                ru.start()
            else:
                read = main(ip2)
                if read == NOT_FOUND:
                    continue
                if read != 0:
                    return read
        return 0
    acfun = False  # Acfun网站
    acvideo = False  # Acfun Video acxxxxx
    acbangumi = False  # Acfun Bangumi
    av = False
    ss = False
    ep = False
    pl = False  # 收藏夹
    hd = False  # 互动视频
    ch = False  # 频道
    uv = False  # 投稿
    md = False  # 番剧信息页
    sm = False  # 小视频
    lr = False  # 直播回放
    che = False  # B站课程
    chel = False  # B站课程已购列表
    live = False  # 直播
    au = False  # 音频区音乐
    ac = False  # 音频区收藏夹/专辑/歌单
    uid = -1  # 收藏夹/频道主人id
    fid = -1  # 收藏夹id
    cid = -1  # 频道id
    uvd = {}  # 投稿查询信息
    pld = {}  # 收藏夹扩展信息
    chd = {}  # 频道扩展信息
    mid = -1  # md号
    sid = -1  # 小视频id
    rid = ""  # 直播回放id
    ssid = -1  # B站课程SS号
    epid = -1  # B站课程EP号
    auid = -1  # AU号
    roomid = -1  # 直播房间ID
    menuid = -1  # 音频区AM号
    collid = -1  # 音频区收藏夹ID
    acvideoid = -1  # Acfun AC号
    acbangumiid = -1  # Acfun AA号
    acepisodeid = -1  # Acfun 剧集号（EP号
    if inp[0:2].lower() == 'ss' and inp[2:].isnumeric():
        s = "https://www.bilibili.com/bangumi/play/ss" + inp[2:]
        ss = True
        if log and not logg.hasf():
            logg.openf(f"log/SS{inp[2:]}_{round(time())}.log")
    elif inp[0:2].lower() == 'ep' and inp[2:].isnumeric():
        s = "https://www.bilibili.com/bangumi/play/ep" + inp[2:]
        ep = True
        if log and not logg.hasf():
            logg.openf(f"log/EP{inp[2:]}_{round(time())}.log")
    elif inp[0:2].lower() == 'av' and inp[2:].isnumeric():
        s = "https://www.bilibili.com/video/av" + inp[2:]
        av = True
        if log and not logg.hasf():
            logg.openf(f"log/AV{inp[2:]}_{round(time())}.log")
    elif inp[0:2].lower() == 'bv':
        inp = str(biliBv.debv(inp))
        s = "https://www.bilibili.com/video/av" + inp
        av = True
        if log and not logg.hasf():
            logg.openf(f"log/AV{inp}_{round(time())}.log")
    elif inp[0:2].lower() == 'md' and inp[2:].isnumeric():
        md = True
        mid = int(inp[2:])
        if log and not logg.hasf():
            logg.openf(f"log/MD{inp}_{round(time())}.log")
    elif inp[0:2].lower() == "au" and inp[2:].isnumeric():
        au = True
        auid = int(inp[2:])
        if log and not logg.hasf():
            logg.openf(f"log/AU{auid}_{round(time())}.log")
    elif inp[0:2].lower() == "am" and inp[2:].isnumeric():
        ac = True
        menuid = int(inp[2:])
        if log and not logg.hasf():
            logg.openf(f"log/AM{menuid}_{round(time())}.log")
    elif inp[:2].lower() == "ac" and inp[2:].isnumeric():
        acfun = True
        acvideo = True
        acvideoid = int(inp[2:])
        if log and not logg.hasf():
            logg.openf(f"log/AC{acvideoid}_{round(time())}.log")
    elif inp[:2].lower() == "aa" and inp[2:].isnumeric():
        acfun = True
        acbangumi = True
        acbangumiid = int(inp[2:])
        if log and not logg.hasf():
            logg.openf(f"log/AA{acbangumiid}_{round(time())}.log")
    elif inp[:2].lower() == "aa" and match(r'\d+_36188_\d+', inp[2:]):
        rs = search(r'(\d+)_36188_(\d+)', inp[2:])
        rs = rs.groups()
        acfun = True
        acbangumi = True
        acbangumiid = int(rs[0])
        acepisodeid = int(rs[1])
        if log and not logg.hasf():
            logg.openf(f"log/AA{acbangumiid}_{round(time())}.log")
    elif inp.isnumeric():
        s = "https://www.bilibili.com/video/av" + inp
        av = True
        if log and not logg.hasf():
            logg.openf(f"log/AV{inp}_{round(time())}.log")
    else:
        re = search(r'([^:]+://)?(www\.)?(space\.)?(vc\.)?(m\.)?(live\.)?bilibili\.com/(s?/?video/av([0-9]+))?(s?/?video/(bv[0-9A-Z]+))?(bangumi/play/(ss[0-9]+))?(bangumi/play/(ep[0-9]+))?(([0-9]+)/favlist(\?(.+)?)?)?(([0-9]+)/channel/(index)?(detail\?(.+))?)?((([0-9]+)/video|medialist/play/([0-9]+))(\?.+)?)?(bangumi/media/md([0-9]+))?(video/([0-9]+))?(mobile/detail\?vc=([0-9]+))?(record/([^\?]+))?(cheese/play/ss([0-9]+))?(cheese/play/ep([0-9]+))?(v/cheese/mine/list)?(cheese/mine/list)?([0-9]+)?(audio/au([0-9]+))?(audio/mycollection/([0-9]+))?(audio/am([0-9]+))?(festival/[^/\?]+\?(.+))?', inp, I)
        if re is None:
            re = search(r'([^:]+://)?(www\.)?b23\.tv/(av([0-9]+))?(bv[0-9A-Z]+)?(ss[0-9]+)?(ep[0-9]+)?(au([0-9]+))?', inp, I)
            if re is None:
                re = search(r'([^:]+://)?(www\.)?acfun\.cn/(v/ac([0-9]+))?(bangumi/aa(\d+)(_36188_(\d+))?)?', inp)
                if re is None:
                    re = search(r"[^:]+://", inp)
                    if re is None:
                        inp = "https://" + inp
                    re = requests.head(inp)
                    if 'Location' in re.headers:
                        ip['i'] = re.headers['Location']
                        ip['uc'] = False
                        return main(ip)
                    else:
                        print(f'{lan["ERROR2"]}')  # 输入有误
                        return -1
                else:
                    re = re.groups()
                    if log:
                        logg.write(f"re = {re}", currentframe(), "Input Regex 3")
                    if re[2]:
                        acfun = True
                        acvideo = True
                        acvideoid = int(re[3])
                        if log and not logg.hasf():
                            logg.openf(f"log/AC{acvideoid}_{round(time())}.log")
                    elif re[4]:
                        acfun = True
                        acbangumi = True
                        acbangumiid = int(re[5])
                        if re[6]:
                            acepisodeid = int(re[7])
                        if log and not logg.hasf():
                            logg.openf(f"log/AA{acbangumiid}_{round(time())}.log")
                    else:
                        print(f'{lan["ERROR2"]}')  # 输入有误
                        return -1
            else:
                re = re.groups()
                if log:
                    logg.write(f"re = {re}", currentframe(), "INPUT REGEX 2")
                if re[3]:
                    inp = re[3]
                    s = "https://www.bilibili.com/video/av" + inp
                    av = True
                    if log and not logg.hasf():
                        logg.openf(f"log/AV{inp}_{round(time())}.log")
                elif re[4]:
                    inp = str(biliBv.debv(re[4]))
                    s = "https://www.bilibili.com/video/av" + inp
                    av = True
                    if log and not logg.hasf():
                        logg.openf(f"log/AV{inp}_{round(time())}.log")
                elif re[5]:
                    inp = re[5]
                    s = "https://www.bilibili.com/bangumi/play/" + inp
                    ss = True
                    if log and not logg.hasf():
                        logg.openf(f"log/SS{inp}_{round(time())}.log")
                elif re[6]:
                    inp = re[6]
                    s = "https://www.bilibili.com/bangumi/play/" + inp
                    ep = True
                    if log and not logg.hasf():
                        logg.openf(f"log/EP{inp}_{round(time())}.log")
                elif re[7]:
                    au = True
                    auid = int(re[8])
                    if log and not logg.hasf():
                        logg.openf(f"log/AU{auid}_{round(time())}.log")
                else:
                    re = search(r"[^:]+://", inp)
                    if re is None:
                        inp = "https://" + inp
                    re = requests.head(inp)
                    if 'Location' in re.headers:
                        ip['i'] = re.headers['Location']
                        ip['uc'] = False
                        return main(ip)
                    else:
                        print(f'{lan["ERROR2"]}')  # 输入有误
                        return -1
        else:
            re = re.groups()
            if log:
                logg.write(f"re = {re}", currentframe(), "INPUT REGEX 1")
            if re[7]:
                inp = re[7]
                s = "https://www.bilibili.com/video/av" + inp
                av = True
                if log and not logg.hasf():
                    logg.openf(f"log/AV{inp}_{round(time())}.log")
            elif re[9]:
                inp = str(biliBv.debv(re[9]))
                s = "https://www.bilibili.com/video/av" + inp
                av = True
                if log and not logg.hasf():
                    logg.openf(f"log/AV{inp}_{round(time())}.log")
            elif re[11]:
                inp = re[11]
                s = "https://www.bilibili.com/bangumi/play/" + inp
                ss = True
                if log and not logg.hasf():
                    logg.openf(f"log/SS{inp}_{round(time())}.log")
            elif re[13]:
                inp = re[13]
                s = "https://www.bilibili.com/bangumi/play/" + inp
                ep = True
                if log and not logg.hasf():
                    logg.openf(f"log/EP{inp}_{round(time())}.log")
            elif re[15]:
                pl = True
                uid = int(re[15])
                pld['k'] = ''
                pld['t'] = 0
                if re[17]:
                    sl = parse_qs(re[17])
                    if 'fid' in sl:
                        for s in sl['fid']:
                            if s.isnumeric():
                                fid = int(s)
                                break
                    if 'keyword' in sl:
                        pld['k'] = sl['keyword'][0]
                    if 'type' in sl:
                        for s in sl['type']:
                            if s.isnumeric():
                                pld['t'] = int(s)
                                break
                    if 'tid' in sl:
                        for s in sl['tid']:
                            if s.isnumeric():
                                pld['tid'] = int(s)
                                break
                    if 'order' in sl:
                        pld['order'] = sl['order'][0]
                    if 't' not in pld:  # 如果没有指定使用默认值
                        pld['t'] = 0
                    if 'tid' not in pld:
                        pld['tid'] = 0
                    if 'order' not in pld:
                        pld['order'] = 'mtime'
                if log and not logg.hasf():
                    if fid == -1:
                        logg.openf(f"log/UID{uid}_FAV_{round(time())}.log")
                    else:
                        logg.openf(f"log/FAV{fid}_{round(time())}.log")
                if log:
                    logg.write(f"uid = {uid}\nfid = {fid}\npld = {pld}", currentframe(), "FAVLIST Parser")
            elif re[18] and (re[20] or (re[22] and hasPar(re[22], 'cid', r'^([0-9]+)$'))):
                ch = True
                uid = int(re[19])
                if re[22]:
                    ls = parse_qs(re[22])
                    if 'cid' in ls:
                        for v in ls['cid']:
                            if v.isnumeric():
                                cid = int(v)
                                break
                    if 'order' in ls:
                        for v in ls['order']:
                            if v.isnumeric():
                                chd['order'] = int(v)
                                break
                if 'order' not in chd:
                    chd['order'] = 0
                if log and not logg.hasf():
                    if cid == -1:
                        logg.openf(f"log/UID{uid}_CHID_{round(time())}.log")
                    else:
                        logg.openf(f"log/CHID{cid}_{round(time())}.log")
                if log:
                    logg.write(f"uid = {uid}\ncid = {cid}", currentframe(), "CHANNEL Parser")
            elif re[23]:
                uv = True
                uid = int(re[25]) if re[25] else int(re[26])
                uvd['t'] = 0
                uvd['k'] = ''
                uvd['o'] = 'pubdate'
                if re[27]:
                    sl = parse_qs(re[27][1:])
                    if 'tid' in sl:
                        for v in sl['tid']:
                            if v.isnumeric():
                                uvd['t'] = int(v)
                                break
                    if 'keyword' in sl:
                        uvd['k'] = sl['keyword'][0]
                    if 'order' in sl:
                        uvd['o'] = sl['order'][0]
                if log and not logg.hasf():
                    logg.openf(f"log/UID{uid}_{round(time())}.log")
                if log:
                    logg.write(f"uid = {uid}\nuvd = {uvd}", currentframe(), "UPLOADER VIDEO Parser")
            elif re[28]:
                md = True
                mid = int(re[29])
                if log and not logg.hasf():
                    logg.openf(f"log/MD{mid}_{round(time())}.log")
            elif re[30]:
                sm = True
                sid = int(re[31])
                if log and not logg.hasf():
                    logg.openf(f"log/SID{sid}_{round(time())}.log")
            elif re[32]:
                sm = True
                sid = int(re[33])
                if log and not logg.hasf():
                    logg.openf(f"log/SID{sid}_{round(time())}.log")
            elif re[34]:
                lr = True
                rid = re[35]
                if log and not logg.hasf():
                    logg.openf(f"log/RID{rid}_{round(time())}.log")
            elif re[36]:
                ss = True
                che = True
                ssid = int(re[37])
                if log and not logg.hasf():
                    logg.openf(f"log/SS{ssid}_{round(time())}.log")
            elif re[38]:
                ep = True
                che = True
                epid = int(re[39])
                if log and not logg.hasf():
                    logg.openf(f"log/EP{epid}_{round(time())}.log")
            elif re[40] or re[41]:
                chel = True
            elif re[5] and re[42]:
                live = True
                roomid = int(re[42])
                if log and not logg.hasf():
                    logg.openf(f"log/LIVEROOM{roomid}_{round(time())}.log")
            elif re[43]:
                au = True
                auid = int(re[44])
                if log and not logg.hasf():
                    logg.openf(f"log/AU{auid}_{round(time())}.log")
            elif re[45]:
                ac = True
                collid = int(re[46])
                if log and not logg.hasf():
                    logg.openf(f"log/COLL{collid}_{round(time())}.log")
            elif re[47]:
                ac = True
                menuid == int(re[48])
                if log and not logg.hasf():
                    logg.openf(f"log/AM{menuid}_{round(time())}.log")
            elif re[49]:
                para = parse_qs(re[50])
                if 'bvid' in para:
                    inp = str(biliBv.debv(para['bvid'][0]))
                    s = "https://www.bilibili.com/video/av" + inp
                    av = True
                    if log and not logg.hasf():
                        logg.openf(f"log/AV{inp}_{round(time())}.log")
                else:
                    print(f'{lan["ERROR2"]}')
                    return -1
            else:
                print(f'{lan["ERROR2"]}')
                return -1
    section = requests.session()
    section.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36", "Connection": "keep-alive", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8"})
    if 'httpproxy' in ip or 'httpsproxy' in ip:
        pr = {}
        if 'httpproxy' in ip:
            pr['http'] = ip['httpproxy']
        if 'httpsproxy' in ip:
            pr['https'] = ip['httpsproxy']
        section.proxies = pr
    if nte:
        section.trust_env = False
    ckfn = "acfun_cookies.json" if acfun else "cookies.json"
    read = JSONParser.loadcookie(section, logg, ckfn)
    ud = {}
    login = 0
    if read == 0:
        if acfun:
            read = biliLogin.acCheckLogin(section, ud, logg)
        else:
            read = biliLogin.tryok(section, ud, logg)
        if read is True:
            if ns:
                print(f"{lan['OUTPUT1']}")  # 登录校验成功！
            login = 1
        elif read is False:
            print(f'{lan["ERROR3"]}')  # 网络错误！校验失败！
            return -1
        else:
            print(f"{lan['WARN1']}")  # 登录信息已过期！
            login = 2
    elif read == -1:
        login = 2
    else:
        print(f"{lan['ERROR4']}")  # 文件读取错误！
        login = 2
    if login == 2:
        if os.path.exists(ckfn):
            os.remove(ckfn)
        if acfun:
            read = biliLogin.acLogin(section, ud, ip, logg)
        else:
            read = biliLogin.login(section, ud, ip, logg)
        if read == 0:
            login = 1
        elif read == 1:
            return -1
        else:
            return -1
    if 'd' not in ud:
        return -1
    if not acfun:
        ud['vip'] = ud['d']['vipStatus']
    if log:
        logg.write(f"read = {read}\nlogin = {login}\nud = {ud}", currentframe(), "VERIFY LOGIN 2")
    if sm:
        if log:
            logg.write(f"GET https://api.vc.bilibili.com/clip/v1/video/detail?video_id={sid}&need_playurl=1", currentframe(), "GET SMALL VIDEO INFO")
        re = section.get('https://api.vc.bilibili.com/clip/v1/video/detail?video_id=%s&need_playurl=1' % (sid))
        re.encoding = "utf8"
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "SMALL VIDEO INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print('%s %s' % (re['code'], re['message']))
            if re['code'] == 65531:
                return NOT_FOUND
            return -1
        inf = JSONParser2.getsmi(re)
        if log:
            logg.write(f"inf = {inf}", currentframe(), "READ SMALL VIDEO INFO")
        if ns:
            PrintInfo.printInfo9(inf)
        cho5 = False
        bs = True
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'cd')
        if read is True:
            bs = False
            cho5 = True
        elif read is False:
            bs = False
        if 'ac' in ip:
            if ip['ac']:
                bs = False
                cho5 = True
            else:
                bs = False
                cho5 = False
        while bs:
            inp = input(f'{lan["INPUT2"]}(y/n)')  # 是否开启继续下载功能？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    cho5 = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"cho5 = {cho5}", currentframe(), "SMALL VIDEO para")
        videodownload.smdownload(section, inf, cho5, se, ip)
        return 0
    if md:
        if log:
            logg.write(f"GET https://www.bilibili.com/bangumi/media/md{mid}", currentframe(), "GET MD WEBPAGE")
        re = section.get('https://www.bilibili.com/bangumi/media/md%s' % (mid))
        re.encoding = "utf8"
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "MD WEBPAGE CONTENT")
        rs = search(r'__INITIAL_STATE__=([^;]+)', re.text, I)
        if rs is not None:
            rs = rs.groups()[0]
            if log:
                logg.write(f"rs = {rs}", currentframe(), "MD WEBPAGE REGEX CONTENT")
            try:
                re = json.loads(rs)
            except json.JSONDecodeError:
                if log:
                    logg.write(traceback.format_exc(), currentframe(), "MD WEBPAGE LOAD JSON ERROR")
                pa = HTMLParser.Myparser3()
                pa.feed(re.text)
                if log:
                    logg.write(f"pa.videodata = {pa.videodata}", currentframe(), "MD WABPAGE JSON CONTENT")
                try:
                    re = json.loads(pa.videodata)
                except json.JSONDecodeError:
                    if log:
                        logg.write(traceback.format_exc(), currentframe(), "MD WEBPAGE LOAD JSON ERROR 2")
                    print(f'{lan["ERROR5"]}')  # md号解析失败
                    return -1
            ip2 = copyip(ip)
            if 'p' in ip:
                ip2['p'] = ip['p']
            ip2['i'] = 'ss%s' % (re['mediaInfo']['season_id'])
            ip2['uc'] = False
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "MD REDIRECT PARAMETERS")
            read = main(ip2)
            if log:
                logg.write(f"read = {read}", currentframe(), "MD REDIRECT RETURN")
            if read != 0 and read != NOT_FOUND:
                return read
        else:
            print(f'{lan["ERROR5"]}')  # md号解析失败
            return -1
        return 0
    if pl:
        if fid == -1:
            af = False
            if JSONParser.getset(se, 'af') is True:
                af = True
            if 'af' in ip:
                af = ip['af']
            if log:
                logg.write(f"af = {af}\nGET https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid={uid}&jsonp=jsonp", currentframe(), "PL PARAMETERS & GET LIST")
            re = section.get('https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=%s&jsonp=jsonp' % (uid))
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "PL GET LIST RETURN")
            re = re.json()
            if re['code'] != 0:
                print('%s %s' % (re['code'], re['message']))
                return -1
            else:
                if 'data' in re and re['data'] is not None and 'list' in re['data'] and re['data']['count'] > 0:
                    if af:
                        dc = re['data']['count']
                        if ns:
                            PrintInfo.printInfo8(re)
                        bs = True
                        f = True
                        while bs:
                            if f and 'afp' in ip:
                                f = False
                                inp = ip['afp']
                            elif ns:
                                inp = input(f'{lan["INPUT3"]}')
                            else:
                                print(f'{lan["ERROR6"]}')
                                return -1
                            cho = []
                            if len(inp) > 0 and inp[0] == 'a':
                                if ns:
                                    print(f'{lan["OUTPUT2"]}')
                                for i in range(1, dc + 1):
                                    cho.append(i)
                                    bs = False
                            elif len(inp) > 0:
                                inp = inp.split(',')
                                bb = True
                                for i in inp:
                                    if i.isnumeric() and int(i) > 0 and int(i) <= dc and (not (int(i) in cho)):
                                        cho.append(int(i))
                                    else:
                                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                                        if rrs is not None:
                                            rrs = rrs.groups()
                                            i1 = int(rrs[0])
                                            i2 = int(rrs[1])
                                            if i2 < i1:
                                                tt = i1
                                                i1 = i2
                                                i2 = tt
                                            for i in range(i1, i2 + 1):
                                                if i > 0 and i <= dc and (not (i in cho)):
                                                    cho.append(i)
                                        else:
                                            bb = False
                                if bb:
                                    bs = False
                                    for i in cho:
                                        if ns:
                                            print(lan['OUTPUT3'] + str(i) + "," + re['data']['list'][i - 1]['title'])
                        for i in cho:
                            ip2 = copyip(ip)
                            ip2['i'] = "https://space.bilibili.com/%s/favlist?fid=%s" % (uid, re['data']['list'][i - 1]['id'])
                            ip2['uc'] = False
                            if log:
                                logg.write(f"ip2 = {ip2}", currentframe(), "PL MULTPLY-PL PRARMETERS")
                            read = main(ip2)
                            if read != 0:
                                return read
                            if log:
                                logg.write(f"read = {read}", currentframe(), "PL MULTPLY-PL RETURN")
                        return 0
                    else:
                        fid = re['data']['list'][0]['id']
                else:
                    print(lan["ERROR7"])
                    return NOT_FOUND
        if log:
            logg.write(f"fid = {fid}", currentframe(), "PL FID OUT")
        if 'ltid' in ip:
            re = JSONParser2.getpltid(section, fid, uid, logg)
            if re == -1:
                return -1
            if len(re) > 0:
                print(lan['PLITID'])
                PrintInfo.printplitid(re)
            else:
                print(lan['PLITIDNUL'])
            return 0
        i = 1
        re = JSONParser2.getpli(section, fid, i, pld, logg)
        if re == -1:
            return -1
        pli = JSONParser2.getplinfo(re)
        if log:
            logg.write(f"pli = {pli}", currentframe(), "PL INFO RESULT")
        if ns:
            PrintInfo.printInfo3(pli)
        n = ceil(pli['count'] / 20)
        plv = []
        JSONParser2.getpliv(plv, re)
        while i < n:
            i = i + 1
            re = JSONParser2.getpli(section, fid, i, pld, logg)
            if re == -1:
                return -1
            JSONParser2.getpliv(plv, re)
        if log:
            logg.write(f"plv = {plv}", currentframe(), "PL VIDEO LIST RESULT")
        if len(plv) != pli['count']:
            print(lan['ERROR8'])  # 视频数量与预计数量不符，貌似BUG了。
            return -1
        if ns:
            PrintInfo.printInfo4(plv)
        bs = True
        f = True
        while bs:
            if f and 'p' in ip:
                f = False
                inp = ip['p']
            elif ns:
                inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
            else:
                print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                return -1
            cho = []
            if inp[0] == 'a':
                if ns:
                    print(lan['OUTPUT5'])  # 您全选了所有视频
                for i in range(1, pli['count'] + 1):
                    cho.append(i)
                bs = False
            else:
                inp = inp.split(',')
                bb = True
                for i in inp:
                    if i.isnumeric() and int(i) > 0 and int(i) <= pli['count'] and (not (int(i) in cho)):
                        cho.append(int(i))
                    else:
                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                        if rrs is not None:
                            rrs = rrs.groups()
                            i1 = int(rrs[0])
                            i2 = int(rrs[1])
                            if i2 < i1:
                                tt = i1
                                i1 = i2
                                i2 = tt
                            for i in range(i1, i2 + 1):
                                if i > 0 and i <= pli['count'] and (not (i in cho)):
                                    cho.append(i)
                        else:
                            bb = False
                if bb:
                    bs = False
                    for i in cho:
                        if ns:
                            print(lan['OUTPUT6'] + str(i) + ',' + plv[i - 1]['title'])  # 您选中了视频：
        bs = True
        c1 = False
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'da')
        if read is not None:
            c1 = read
            bs = False
        if 'da' in ip:
            c1 = ip['da']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT4']}(y/n)")  # 是否自动下载每一个视频的所有分P？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    c1 = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"c1 = {c1}", currentframe(), "PLI PARAMETERS")
        for i in cho:
            ip2 = copyip(ip)
            ip2['i'] = str(plv[i - 1]['id'])
            ip2['uc'] = False
            if c1:
                ip2['p'] = 'a'
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "PLI PARAMETERS 2")
            read = main(ip2)
            if log:
                logg.write(f"read = {read}", currentframe(), "PLI RETURN")
            if read != 0 and read != NOT_FOUND:
                return read
        return 0
    if ch:
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        if cid == -1:
            r.headers.update({'referer': 'https://space.bilibili.com/%s/channel/index' % (uid)})
            if log:
                logg.write(f"GET https://api.bilibili.com/x/space/channel/list?mid={uid}&guest=false&jsonp=jsonp", currentframe(), "GET CHANNEL LIST")
            re = r.get("https://api.bilibili.com/x/space/channel/list?mid=%s&guest=false&jsonp=jsonp" % (uid))
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET CHANNEL LIST RESULT")
            re = re.json()
            if re['code'] != 0:
                print('%s %s' % (re['code'], re['message']))
                return -1
            chl = JSONParser2.getchl(re)
            if log:
                logg.write(f"chl = {chl}", currentframe(), "CHANNEL LIST RESULT")
            if len(chl) == 0:
                return NOT_FOUND
            if ns:
                PrintInfo.printInfo5(chl)
            bs = True
            f = True
            while bs:
                if f and 'p' in ip:
                    f = False
                    inp = ip['p']
                elif ns:
                    inp = input(lan['INPUT5'])  # 请输入你想下载的频道（每两个编号间用,隔开，全部下载可输入a）：
                else:
                    print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                    return -1
                cho = []
                if inp[0] == 'a':
                    if ns:
                        print(lan['OUTPUT7'])  # 您全选了所有频道
                    for i in range(1, len(chl) + 1):
                        cho.append(i)
                    bs = False
                else:
                    inp = inp.split(',')
                    bb = True
                    for i in inp:
                        if i.isnumeric() and int(i) > 0 and int(i) <= len(chl) and (not (int(i) in cho)):
                            cho.append(int(i))
                        else:
                            rrs = search(r"([0-9]+)-([0-9]+)", i)
                            if rrs is not None:
                                rrs = rrs.groups()
                                i1 = int(rrs[0])
                                i2 = int(rrs[1])
                                if i2 < i1:
                                    tt = i1
                                    i1 = i2
                                    i2 = tt
                                for i in range(i1, i2 + 1):
                                    if i > 0 and i <= len(chl) and (not (i in cho)):
                                        cho.append(i)
                            else:
                                bb = False
                    if bb:
                        bs = False
                        for i in cho:
                            if ns:
                                print(lan['OUTPUT8'] + str(i) + ',' + chl[i - 1]['name'])  # 您选中了频道：
                for i in cho:
                    ip2 = copyip(ip)
                    ip2['i'] = 'https://space.bilibili.com/%s/channel/detail?cid=%s' % (uid, chl[i - 1]['cid'])
                    ip2['uc'] = False
                    if log:
                        logg.write(f"ip2 = {ip2}", currentframe(), "CHANNLE LIST PARAMETERS")
                    read = main(ip2)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "CHANNLE LIST RESULT")
                    if read != 0 and read != NOT_FOUND:
                        return read
            return 0
        r.headers.update({'referer': 'https://space.bilibili.com/%s/channel/detail?cid=%s' % (uid, cid)})
        re = JSONParser2.getchi(r, uid, cid, 1, chd, logg)
        if re == -1:
            return -1
        chi = JSONParser2.getchn(re)
        if log:
            logg.write(f"chi = {chi}", currentframe(), "CHANNLE INFO RESULT")
        n = ceil(chi['count'] / 30)
        i = 1
        chv = []
        JSONParser2.getchs(chv, re)
        while i < n:
            i = i + 1
            re = JSONParser2.getchi(r, uid, cid, i, chd, logg)
            if re == -1:
                return -1
            JSONParser2.getchs(chv, re)
        if log:
            logg.write(f"chv = {chv}", currentframe(), "CHANNLE VIDEO LIST RESULT")
        if len(chv) == 0:
            return NOT_FOUND
        if chi['count'] != len(chv):
            print(lan['ERROR8'])  # 视频数量与预计数量不符，貌似BUG了。
            return -1
        if ns:
            PrintInfo.printInfo6(chv, chi)
        bs = True
        f = True
        while bs:
            if f and 'p' in ip:
                f = False
                inp = ip['p']
            elif ns:
                inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
            else:
                print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                return -1
            cho = []
            if inp[0] == 'a':
                if ns:
                    print(lan['OUTPUT5'])  # 您全选了所有视频
                for i in range(1, chi['count'] + 1):
                    cho.append(i)
                bs = False
            else:
                inp = inp.split(',')
                bb = True
                for i in inp:
                    if i.isnumeric() and int(i) > 0 and int(i) <= chi['count'] and (not (int(i) in cho)):
                        cho.append(int(i))
                    else:
                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                        if rrs is not None:
                            rrs = rrs.groups()
                            i1 = int(rrs[0])
                            i2 = int(rrs[1])
                            if i2 < i1:
                                tt = i1
                                i1 = i2
                                i2 = tt
                            for i in range(i1, i2 + 1):
                                if i > 0 and i <= chi['count'] and (not (i in cho)):
                                    cho.append(i)
                        else:
                            bb = False
                if bb:
                    bs = False
                    for i in cho:
                        if ns:
                            print(lan['OUTPUT6'] + str(i) + ',' + chv[i - 1]['title'])  # 您选中了视频：
        bs = True
        c1 = False
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'da')
        if read is not None:
            c1 = read
            bs = False
        if 'da' in ip:
            c1 = ip['da']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT4']}(y/n)")  # 是否自动下载每一个视频的所有分P？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    c1 = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"c1 = {c1}", currentframe(), "CHANNLE VIDEO PARAMETERS")
        for i in cho:
            ip2 = copyip(ip)
            ip2['i'] = str(chv[i - 1]['aid'])
            ip2['uc'] = False
            if c1:
                ip2['p'] = 'a'
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "CHANNLE VIDEO PARAMETERS 2")
            read = main(ip2)
            if log:
                logg.write(f"read = {read}", currentframe(), "CHANNLE VIDEO RESULT")
            if read != 0 and read != NOT_FOUND:
                return read
        return 0
    if uv:
        re = JSONParser2.getup(uid, section, logg)
        if re == -1:
            return -1
        up = JSONParser2.getupi(re)
        if log:
            logg.write(f"up = {up}", currentframe(), "UPLOADER INFO")
        re = JSONParser2.getuvi(uid, 1, uvd, section, logg)
        if re == -1:
            return -1
        vn = re['data']['page']['count']
        if vn == 0:
            return NOT_FOUND
        if 'ltid' in ip:
            tre = re['data']['list']['tlist']
            re = []
            for tid in tre.keys():
                re.append(tre[tid])
            if len(re) > 0:
                print(lan['UPLTID'])
                PrintInfo.printplitid(re)
            else:
                print(lan['PLITIDNUL'])
            return 0
        n = ceil(vn / 30)
        i = 1
        vl = []
        JSONParser2.getuvl(re, vl)
        while i < n:
            i = i + 1
            re = JSONParser2.getuvi(uid, i, uvd, section, logg)
            if re == -1:
                return -1
            JSONParser2.getuvl(re, vl)
        if log:
            logg.write(f"vl = {vl}", currentframe(), "UPLOAD VIDEO LIST RESULT")
        if len(vl) != vn:
            print(lan['ERROR8'])  # 视频数量与预计数量不符，貌似BUG了。
            return -1
        if ns:
            PrintInfo.printInfo7(up, vl)
        bs = True
        f = True
        while bs:
            if f and 'p' in ip:
                f = False
                inp = ip['p']
            elif ns:
                inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
            else:
                print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                return -1
            cho = []
            if inp[0] == 'a':
                if 'ns':
                    print(lan['OUTPUT5'])  # 您全选了所有视频
                for i in range(1, vn + 1):
                    cho.append(i)
                bs = False
            else:
                inp = inp.split(',')
                bb = True
                for i in inp:
                    if i.isnumeric() and int(i) > 0 and int(i) <= vn and (not (int(i) in cho)):
                        cho.append(int(i))
                    else:
                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                        if rrs is not None:
                            rrs = rrs.groups()
                            i1 = int(rrs[0])
                            i2 = int(rrs[1])
                            if i2 < i1:
                                tt = i1
                                i1 = i2
                                i2 = tt
                            for i in range(i1, i2 + 1):
                                if i > 0 and i <= vn and (not (i in cho)):
                                    cho.append(i)
                        else:
                            bb = False
                if bb:
                    bs = False
                    for i in cho:
                        if ns:
                            print(lan['OUTPUT6'] + str(i) + ',' + vl[i - 1]['title'])  # 您选中了视频：
        bs = True
        c1 = False
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'da')
        if read is not None:
            c1 = read
            bs = False
        if 'da' in ip:
            c1 = ip['da']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT4']}(y/n)")  # 是否自动下载每一个视频的所有分P？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    c1 = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"c1 = {c1}", currentframe(), "UPLOADER VIDEO PARAMETERS")
        for i in cho:
            ip2 = copyip(ip)
            ip2['i'] = str(vl[i - 1]['aid'])
            ip2['uc'] = False
            if c1:
                ip2['p'] = 'a'
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "UPLOADER VIDEO PARAMETERS 2")
            read = main(ip2)
            if log:
                logg.write(f"read = {read}", currentframe(), "UPLOADER VIDEO RETURN")
            if read != 0 and read != NOT_FOUND:
                return read
        return 0
    xml = 0
    xmlc = []
    read = biliPlayerXmlParser.loadXML()
    if read == -1:
        xml = 2
    else:
        xml = 1
        xmlc = read
    if xml == 1:
        bs = True
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'dmgl')
        if read is True:
            bs = False
        elif read is False:
            bs = False
            xml = 2
        if 'dm' in ip:
            if ip['dm']:
                bs = False
                xml = 1
            else:
                bs = False
                xml = 2
        while bs:
            yn = input(f"{lan['INPUT6']}(y/n)")  # 是否启用弹幕过滤？
            if yn[0].lower() == 'y':
                bs = False
            if yn[0].lower() == 'n':
                bs = False
                xml = 2
    if log:
        logg.write(f"xml = {xml}\nxmlc = {xmlc}", currentframe(), "BARRAGE FILTER PARAMETERS")
    if lr:  # 直播回放
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        if log:
            logg.write(f"GET https://api.live.bilibili.com/xlive/web-room/v1/record/getInfoByLiveRecord?rid={rid}", currentframe(), "GET LIVE RECORD INFO")
        re = r.get('https://api.live.bilibili.com/xlive/web-room/v1/record/getInfoByLiveRecord?rid=%s' % (rid))  # 直播回放信息
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE RECORD INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print('%s %s' % (re['code'], re['message']))
            if re['code'] == 1003902:
                return NOT_FOUND
            return -1
        ri = JSONParser2.getlr1(re)
        if log:
            logg.write(f"GET https://api.live.bilibili.com/room/v1/Room/get_info?room_id={ri['roomid']}&from=room", currentframe(), "GET LIVE ROOM INFO")
        re = r.get('https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s&from=room' % (ri['roomid']))  # 直播房间信息
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE ROOM INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print('%s %s' % (re['code'], re['message']))
            return -1
        JSONParser2.getlr2(re, ri)
        if log:
            logg.write(f"GET https://api.bilibili.com/x/space/acc/info?mid={ri['uid']}&jsonp=jsonp", currentframe(), "GET LIVE UPLOADER INFO")
        re = r.get('https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp' % (ri['uid']))  # UP主信息
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE UPLOADER INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print('%s %s' % (re['code'], re['message']))
            return -1
        JSONParser2.getlr3(re, ri)
        if log:
            logg.write(f"ri = {ri}", currentframe(), "LIVE RECORD INFO RESULT")
        if ns:
            PrintInfo.printlr(ri)
        bs = True
        f = True
        while bs:
            if f and 'd' in ip:
                inp = str(ip['d'])
                f = False
            elif ns:
                inp = input(lan['INPUT7'])  # 请输入你要下载的方式：\n1.视频下载\n2.弹幕下载\n3.视频+弹幕下载
            else:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            if inp[0].isnumeric() and int(inp[0]) > 0 and int(inp[0]) < 4:
                cho = int(inp[0])
                bs = False
        if cho > 1:
            read = biliLiveDanmu.lrdownload(ri, section, ip, se, xml, xmlc)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE RECORD BARRAGE RETURN")
            if read == -1:
                return -1
        if cho == 1 or cho == 3:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                if ip['m']:
                    bs = False
                    cho3 = True
                else:
                    bs = False
                    cho3 = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            cho5 = False
            bs = True
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'cd')
            if read is True:
                bs = False
                cho5 = True
            elif read is False:
                bs = False
            if 'ac' in ip:
                if ip['ac']:
                    bs = False
                    cho5 = True
                else:
                    bs = False
                    cho5 = False
            while bs:
                inp = input(f'{lan["INPUT2"]}(y/n)')
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho5 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}\ncho5 = {cho5}", currentframe(), "LIVE RECORD VIDEO PARA")
            read = videodownload.lrvideodownload(ri, section, cho3, cho5, se, ip)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE RECORD VIDEO RETURN")
            if read == -5:
                return -1
        return 0
    if chel:
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        r.headers.update({'referer': 'https://www.bilibili.com/v/cheese/mine/list'})
        chep = JSONParser2.getchel(r, logg)
        if log:
            logg.write(f"chep = {chep}", currentframe(), "PAID COURSES LIST")
        if chep == -1:
            return -1
        if ns:
            PrintInfo.printInfo10(chep)
        vn = len(chep)
        bs = True
        f = True
        while bs:
            if f and 'p' in ip:
                f = False
                inp = ip['p']
            elif ns:
                inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
            else:
                print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                return -1
            cho = []
            if inp[0] == 'a':
                if ns:
                    print(lan['OUTPUT5'])  # 您全选了所有视频
                for i in range(1, vn + 1):
                    cho.append(i)
                bs = False
            else:
                inp = inp.split(',')
                bb = True
                for i in inp:
                    if i.isnumeric() and int(i) > 0 and int(i) <= vn and (not (int(i) in cho)):
                        cho.append(int(i))
                    else:
                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                        if rrs is not None:
                            rrs = rrs.groups()
                            i1 = int(rrs[0])
                            i2 = int(rrs[1])
                            if i2 < i1:
                                tt = i1
                                i1 = i2
                                i2 = tt
                            for i in range(i1, i2 + 1):
                                if i > 0 and i <= vn and (not (i in cho)):
                                    cho.append(i)
                        else:
                            bb = False
                if bb:
                    bs = False
                    for i in cho:
                        if ns:
                            print(lan['OUTPUT6'] + str(i) + ',' + chep[i - 1]['title'])  # 您选中了视频：
        bs = True
        c1 = False
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'da')
        if read is not None:
            c1 = read
            bs = False
        if 'da' in ip:
            c1 = ip['da']
            bs = False
        while bs:
            inp = input(f"{lan['INPUT4']}(y/n)")  # 是否自动下载每一个视频的所有分P？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    c1 = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"c1 = {c1}", currentframe(), "PAID COURSES LIST PARA")
        for i in cho:
            ip2 = copyip(ip)
            ip2['i'] = f"https://www.bilibili.com/cheese/play/ss{chep[i-1]['id']}"
            ip2['uc'] = False
            if c1:
                ip2['p'] = 'a'
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "PAID COURSES LIST PARA 2")
            read = main(ip2)
            if log:
                logg.write(f"read = {read}", currentframe(), "PAID COURSES LIST RETURN")
            if read != 0 and read != NOT_FOUND:
                return read
        return 0
    if che:
        if ssid == -1:  # 输入为ep号时的处理
            uri = f"https://api.bilibili.com/pugv/view/web/season?ep_id={epid}"
        else:
            uri = f"https://api.bilibili.com/pugv/view/web/season?season_id={ssid}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "GET PAID COURSES INFO")
        re = section.get(uri)
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET PAID COURSES INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            if re['code'] == -404:
                return NOT_FOUND
            return -1
        vd = JSONParser.parseche(re)
        if log:
            logg.write(f"vd = {vd}", currentframe(), "PAID COURSES INFO")
    if live:
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        uri = f"https://live.bilibili.com/{roomid}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "GET LIVE ROOM WEBPAGE")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE ROOM WEBPAGE RESULT")
        r.headers.update({'referer': uri})
        rs = search(r'window\.__NEPTUNE_IS_MY_WAIFU__=({[^<]+})', re.text, I)
        if rs is not None:
            live_info = json.loads(rs.groups()[0])
        else:
            live_info = None
        uri = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={roomid}&from=room"
        if log:
            logg.write(f"GET {uri}", currentframe(), "GET LIVE ROOM INFO")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
            if re['code'] == 1:
                return NOT_FOUND
            return -1
        room_info = re['data']
        info = JSONParser2.getliveinfo1(room_info)
        if log:
            logg.write(f"live_info = {live_info}\nroom_info = {room_info}", currentframe(), "LIVE ROOM INFO")
        uri = f"https://api.bilibili.com/x/space/acc/info?mid={info['uid']}&jsonp=jsonp"
        if log:
            logg.write(f"GET {uri}", currentframe(), "GET LIVE UPLOADER INFO")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET LIVE UPLOADER INFO RESULT")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['message']}")
        uploader_info = re['data']
        JSONParser2.getliveinfo2(uploader_info, info)
        if ns:
            PrintInfo.printliveInfo(info)
        roomInitRes = None
        if live_info is not None:
            roomInitRes = live_info['roomInitRes']['data']
        if log:
            logg.write(f"uploader_info = {uploader_info}\ninfo = {info}\nroomInitRes = {roomInitRes}", currentframe(), "LIVE INFO")
        bs = True
        cho = False
        if not ns:
            bs = False
        read = JSONParser.getset(se, 'mp')
        if read is True:
            bs = False
            cho = True
        elif read is False:
            bs = False
        if 'm' in ip:
            bs = False
            cho = ip['m']
        while bs:
            inp = input(f"{lan['INPUT8']}(y/n)")  # 是否要默认下载最高画质（这样将不会询问具体画质）？
            if len(inp) > 0:
                if inp[0].lower() == 'y':
                    cho = True
                    bs = False
                elif inp[0].lower() == 'n':
                    bs = False
        if log:
            logg.write(f"cho = {cho}", currentframe(), "LIVE PARA")
        if info['livestatus'] > 0:
            read = videodownload.livevideodownload(info, roomInitRes, r, cho, se, ip)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE VIDEO RETURN")
            if read != 0:
                return -1
        else:
            print(lan['LIVE_NOT_START'])
            bs = True
            while bs:
                sleep(30)  # 30秒后继续检测
                uri = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={roomid}&from=room"
                if log:
                    logg.write(f"GET {uri}", currentframe(), "GET ROOM INFO 2")
                re = r.get(uri)
                re.encoding = 'utf8'
                if log:
                    logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET ROOM INFO 2 RESULT")
                re = re.json()
                if re['code'] != 0:
                    print(f"{re['code']} {re['message']}")
                    return -1
                room_info = re['data']
                if room_info['live_status'] > 0:
                    info['livestatus'] = room_info['live_status']
                    bs = False
                elif ns:
                    print(lan['LIVE_NOT_START'])
            read = videodownload.livevideodownload(info, roomInitRes, r, cho, se, ip)
            if log:
                logg.write(f"read = {read}", currentframe(), "LIVE VIDEO RETURN 2")
            if read != 0:
                return -1
        return 0
    if au:
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if log:
            logg.write(f"read = {read}", currentframe(), "Audio Load Cookies Failed")
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.headers.update({'referer': f'https://www.bilibili.com/audio/au{auid}'})
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        uri = f"https://www.bilibili.com/audio/music-service-c/web/song/info?sid={auid}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Audio Get Info")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Get Info Result")
        re = re.json()
        wapir = False  # 网页端API结果
        mapir = False  # APP API结果
        uri = f"https://api.bilibili.com/audio/music-service-c/songs/playing?song_id={auid}"  # build=6140500
        if log:
            logg.write(f"GET {uri}", currentframe(), "Audio Get Info (APPAPI)")
        re2 = r.get(uri)
        re2.encoding = 'utf8'
        if log:
            logg.write(f"status = {re2.status_code}\n{re2.text}", currentframe(), "Audio Get Info Result (APPAPI)")
        re2 = re2.json()
        if re['code'] != 0 and re['code'] != 72010027:
            print(f"{re['code']} {re['msg']}")
            if re['code'] == 7201006:
                return NOT_FOUND
        elif re['code'] == 0:
            wapir = True
        if re2['code'] != 0:
            print(f"{re2['code']} {re2['msg']}")
            if re['code'] == 7201006:
                return NOT_FOUND
        else:
            mapir = True
        if not wapir and not mapir:
            if re['code'] == 72010027:
                print(lan['AUAPPERR'])  # 该音频只能在APP上播放。（该程序目前不支持。）
            return 0
        sd = {}
        if wapir:
            sd = re['data']
        if mapir:
            sd = JSONParser2.dealwithauapi(sd, re2['data'])
        uri = f"https://www.bilibili.com/audio/music-service-c/web/tag/song?sid={auid}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Audio Get Tags Info")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Get Tags Info Result")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['msg']}")
            return 0
        sd['tags'] = []
        for i in re['data']:
            sd['tags'].append(i['info'])
        if 'pgc_info' in sd and sd['pgc_info'] is not None and type(sd['pgc_info']) == dict:
            pgc_info = sd['pgc_info']
            if 'pgc_menu' in pgc_info and pgc_info['pgc_menu'] is not None and type(pgc_info['pgc_menu']) == dict:
                pgc_menu = pgc_info['pgc_menu']
                if 'menuId' in pgc_menu and pgc_menu['menuId'] is not None and pgc_menu['menuId'] != 0:
                    uri = f"https://api.bilibili.com/audio/music-service-c/menus/{pgc_menu['menuId']}"
                    if log:
                        logg.write(f"GET {uri}", currentframe(), "Audio Get Album List (APP API)")
                    re = r.get(uri)
                    re.encoding = 'utf8'
                    if log:
                        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Get Album List Result (APP API)")
                    re = re.json()
                    if re['code'] != 0:
                        print(f"{re['code']} {re['msg']}")
                    else:
                        re = re['data']
                        pgc_info['menusRespones'] = re['menusRespones']
                        pgc_info['songsList'] = re['songsList']
                        if menuInfo is not None:
                            pgc_info['menusRespones2'] = menuInfo['menusRespones']
                            pgc_info['songsList2'] = menuInfo['songsList']
        elif menuInfo is not None:
            pgc_info = {}
            sd['pgc_info'] = pgc_info
            pgc_info['menusRespones2'] = menuInfo['menusRespones']
            pgc_info['songsList2'] = menuInfo['songsList']
        if log:
            logg.write(f"sd = {sd}", currentframe(), 'Audio Info')
        if ns:
            PrintInfo.printAuInfo(sd)
        cho = 1
        bs = True
        if 'd' in ip:
            bs = False
            cho = ip['d']
            if cho < 1 or cho > 3:
                cho = 1
                bs = True
        while bs:
            if not ns:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            inp = input(lan['AUINPUT'])
            if inp[0].isnumeric() and int(inp[0]) > 0 and int(inp[0]) < 4:
                cho = int(inp[0])
                bs = False
        if cho == 1:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                if ip['m']:
                    bs = False
                    cho3 = True
                else:
                    bs = False
                    cho3 = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            cho5 = False
            bs = True
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'cd')
            if read is True:
                bs = False
                cho5 = True
            elif read is False:
                bs = False
            if 'ac' in ip:
                if ip['ac']:
                    bs = False
                    cho5 = True
                else:
                    bs = False
                    cho5 = False
            while bs:
                inp = input(f'{lan["INPUT2"]}(y/n)')
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho5 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}\ncho5 = {cho5}", currentframe(), "Normal Video Download Video/Audio Para")
            read = videodownload.audownload(sd, r, se, ip, cho3, cho5, ud)
            if log:
                logg.write(f"read = {read}", currentframe(), "Audio Download Audio Return")
        elif cho == 2:
            read = videodownload.aulrcdownload(sd, r, se, ip)
            if log:
                logg.write(f"read = {read}", currentframe(), "Audio Download Lyrics Retrun")
            if read == -1 or read == -4:
                return -1
        elif cho == 3:
            read = videodownload.aupicdownload(sd, r, se, ip)
            if log:
                logg.write(f"read = {read}", currentframe(), "Audio Download Cover Image Retrun")
            if read == -1:
                return -1
        return 0
    if ac:
        r = requests.Session()
        r.headers = copydict(section.headers)
        r.proxies = section.proxies
        if nte:
            r.trust_env = False
        read = JSONParser.loadcookie(r, logg)
        if log:
            logg.write(f"read = {read}", currentframe(), "Audio Album Load Cookies Failed")
        if read != 0:
            print(lan['ERROR10'])  # 读取cookies.json出现错误
            return -1
        r.headers.update({'referer': f'https://www.bilibili.com/audio/au{auid}'})
        r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
        r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
        r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
        r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
        if menuid == -1:
            uri = f"https://www.bilibili.com/audio/music-service-c/web/collections/info?sid={collid}"
            if log:
                logg.write(f"GET {uri}", currentframe(), "Audio Coll Get Info")
            re = r.get(uri)
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Coll Get Info Result")
            re = re.json()
            if re['code'] != 0:
                print(f"{re['code']} {re['msg']}")
                return -1
            if re['data'] is None:
                return NOT_FOUND
            menuid = re['data']['menuId']
        uri = f"https://api.bilibili.com/audio/music-service-c/menus/{menuid}"
        if log:
            logg.write(f"GET {uri}", currentframe(), "Audio Album Get Info (APP API)")
        re = r.get(uri)
        re.encoding = 'utf8'
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Audio Album Get Info Result")
        re = re.json()
        if re['code'] != 0:
            print(f"{re['code']} {re['msg']}")
            if re['code'] == 7201009:
                return NOT_FOUND
            return -1
        re = re['data']
        songsList = re['songsList']
        an = len(songsList)
        if ns:
            PrintInfo.printAmInfo(re)
        bs = True
        f = True
        while bs:
            if f and 'p' in ip:
                f = False
                inp = ip['p']
            elif ns:
                inp = input(lan['OUTPUT14'])  # 请输入你想下载的音频编号（每两个编号间用,隔开，全部下载可输入a）：
            else:
                print(lan['ERROR13'])  # 请使用-p <number>选择音频编号
                return -1
            cho = []
            if inp[0] == 'a':
                if ns:
                    print(lan['OUTPUT15'])  # 您全选了所有音频
                for i in range(1, an + 1):
                    cho.append(i)
                bs = False
            else:
                inp = inp.split(',')
                bb = True
                for i in inp:
                    if i.isnumeric() and int(i) > 0 and int(i) <= an and (not (int(i) in cho)):
                        cho.append(int(i))
                    else:
                        rrs = search(r"([0-9]+)-([0-9]+)", i)
                        if rrs is not None:
                            rrs = rrs.groups()
                            i1 = int(rrs[0])
                            i2 = int(rrs[1])
                            if i2 < i1:
                                tt = i1
                                i1 = i2
                                i2 = tt
                            for i in range(i1, i2 + 1):
                                if i > 0 and i <= an and (not (i in cho)):
                                    cho.append(i)
                        else:
                            bb = False
                if bb:
                    bs = False
                    for i in cho:
                        if ns:
                            print(f"{lan['OUTPUT16']}{i},{songsList[i-1]['title']}")
        for i in cho:
            ip2 = copyip(ip)
            ip2['i'] = f"au{songsList[i-1]['song_id']}"
            ip2['uc'] = False
            if log:
                logg.write(f"ip2 = {ip2}", currentframe(), "Audio Album Audio Para")
            read = main(ip2, menuInfo=re)
            if log:
                logg.write(f"read = {read}", currentframe(), "Audio Album Audio Return")
            if read != 0 and read != NOT_FOUND:
                return read
        return 0
    if acvideo:
        url = f"https://www.acfun.cn/v/ac{acvideoid}"
        if log:
            logg.write(f"GET {url}", currentframe(), "Get Acfun Video Webpage")
        re = section.get(url)
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Acfun Video Webpage Result")
        if re.status_code == 404 or re.url != url:
            print("404")
            return NOT_FOUND
        elif re.status_code >= 400:
            return -1
        parser = HTMLParser.AcfunParser()
        parser.feed(re.text)
        if log:
            logg.write(f"parser.videoInfo = {parser.videoInfo}", currentframe(), "Acfun Video Webpage Parser Result")
        videoInfo = json.loads(parser.videoInfo, strict=False)
        if 'tagList' not in videoInfo:
            videoInfo['tagList'] = []
        if ns:
            PrintInfo.printAcInfo(videoInfo)
        cho = []
        videoCount = len(videoInfo['videoList'])
        if videoCount == 1:
            cho.append(1)
        else:
            bs = True
            f = True
            while bs:
                if f and 'p' in ip:
                    f = False
                    inp = ip['p']
                elif ns:
                    inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
                else:
                    print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                    return -1
                cho = []
                if inp[0] == 'a':
                    if ns:
                        print(lan['OUTPUT5'])  # 您全选了所有视频
                    for i in range(1, videoCount + 1):
                        cho.append(i)
                    bs = False
                else:
                    inp = inp.split(',')
                    bb = True
                    for i in inp:
                        if i.isnumeric() and int(i) > 0 and int(i) <= videoCount and (not (int(i) in cho)):
                            cho.append(int(i))
                        else:
                            rrs = search(r"([0-9]+)-([0-9]+)", i)
                            if rrs is not None:
                                rrs = rrs.groups()
                                i1 = int(rrs[0])
                                i2 = int(rrs[1])
                                if i2 < i1:
                                    tt = i1
                                    i1 = i2
                                    i2 = tt
                                for i in range(i1, i2 + 1):
                                    if i > 0 and i <= videoCount and (not (i in cho)):
                                        cho.append(i)
                            else:
                                bb = False
                    if bb:
                        bs = False
                        for i in cho:
                            if ns:
                                print(f"{lan['OUTPUT6']}{i},{videoInfo['videoList'][i-1]['title']}")  # 您选中了视频：
        cho2 = 0
        bs = True
        if 'd' in ip and ip['d'] > 0 and ip['d'] < 5:
            bs = False
            cho2 = ip['d']
        while bs:
            if not ns:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            inp = input(lan['INPUT13'])  # 选择下载方式
            if inp[0].isnumeric() and int(inp[0]) > 0 and int(inp[0]) < 5:
                cho2 = int(inp[0])
                bs = False
        if cho2 == 1 or cho2 == 4:
            for i in cho:
                read = biliDanmu.acDownloadDanmu(section, i - 1, videoInfo, se, ip, xml, xmlc)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Normal Video Download Barrage Return")
                if read == 0:
                    print(lan['OUTPUT9'].replace('<number>', str(i)))  # <number>P下载完成
        if cho2 == 2 or cho2 == 4:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                cho3 = ip['m']
                bs = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}", currentframe(), "Acfun Normal Video Download Video Para")
            for i in cho:
                read = videodownload.acVideoDownload(section, i - 1, videoInfo, cho3, se, ip)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Normal Video Download Video Return")
                if read == -4:
                    return -1
        if cho2 == 3:
            for i in cho:
                read = videodownload.acCoverImgDownload(section, videoInfo, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Normal Video Download Pic Return")
        return 0
    if acbangumi:
        url = f"https://www.acfun.cn/bangumi/aa{acbangumiid}"
        if log:
            logg.write(f"GET {url}", currentframe(), "Get Acfun Bangumi Webpage")
        re = section.get(url)
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Acfun Bangumi Webpage Result")
        if re.status_code == 404:
            print("404")
            return NOT_FOUND
        elif re.status_code >= 400:
            return -1
        parser = HTMLParser.AcfunBangumiParser()
        parser.feed(re.text)
        if log:
            logg.write(f"parser.bangumiData = {parser.bangumiData}\nparser.bangumiList = {parser.bangumiList}", currentframe(), "Acfun Bangumi Webpage Parser Result")
        bangumiData = json.loads(parser.bangumiData, strict=False)
        bangumiList = json.loads(parser.bangumiList, strict=False)
        if ns:
            PrintInfo.printAcBangumiInfo(bangumiData, bangumiList)
        cho = []
        videoCount = len(bangumiList['items'])
        if videoCount == 1:
            cho.append(1)
        else:
            epl = lan['INPUT10'] if acepisodeid != -1 else ''  # ，仅下载输入的ep号可输入b
            bs = True
            f = True
            while bs:
                if f and 'p' in ip:
                    f = False
                    inp = ip['p']
                elif ns:
                    inp = input(f"{lan['OUTPUT4']}{epl}")  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
                else:
                    print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                    return -1
                cho = []
                if inp[0] == 'a':
                    if ns:
                        print(lan['OUTPUT5'])  # 您全选了所有视频
                    for i in range(1, videoCount + 1):
                        cho.append(i)
                    bs = False
                elif acepisodeid != -1 and inp[0] == 'b':
                    i = 0
                    found = False
                    for k in bangumiList['items']:
                        i += 1
                        if k['itemId'] == acepisodeid:
                            cho.append(i)
                            found = True
                            break
                    if found:
                        bs = False
                else:
                    inp = inp.split(',')
                    bb = True
                    for i in inp:
                        if i.isnumeric() and int(i) > 0 and int(i) <= videoCount and (not (int(i) in cho)):
                            cho.append(int(i))
                        else:
                            rrs = search(r"([0-9]+)-([0-9]+)", i)
                            if rrs is not None:
                                rrs = rrs.groups()
                                i1 = int(rrs[0])
                                i2 = int(rrs[1])
                                if i2 < i1:
                                    tt = i1
                                    i1 = i2
                                    i2 = tt
                                for i in range(i1, i2 + 1):
                                    if i > 0 and i <= videoCount and (not (i in cho)):
                                        cho.append(i)
                            else:
                                bb = False
                    if bb:
                        bs = False
            for i in cho:
                if ns:
                    print(f"{lan['OUTPUT6']}{i},{bangumiList['items'][i-1]['title']}")  # 您选中了视频：
        cho2 = 0
        bs = True
        if 'd' in ip and ip['d'] > 0 and ip['d'] < 5:
            bs = False
            cho2 = ip['d']
        while bs:
            if not ns:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            inp = input(lan['INPUT13'])  # 选择下载方式
            if inp[0].isnumeric() and int(inp[0]) > 0 and int(inp[0]) < 5:
                cho2 = int(inp[0])
                bs = False
        if cho2 == 1 or cho2 == 4:
            for i in cho:
                biliDanmu.acBangumiDownloadDanmu(section, bangumiData, bangumiList, i - 1, se, ip, xml, xmlc)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Bangumi Video Download Barrage Return")
                if read == 0:
                    print(lan['OUTPUT9'].replace('<number>', str(i)))  # <number>P下载完成
        if cho2 == 2 or cho2 == 4:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                cho3 = ip['m']
                bs = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}", currentframe(), "Acfun Bangumi Video Download Video Para")
            for i in cho:
                read = videodownload.acBangumiVideoDownload(section, i - 1, bangumiData, bangumiList, cho3, se, ip)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Bangumi Video Download Video Return")
                if read == -4:
                    return -1
        if cho2 == 3:
            for i in cho:
                read = videodownload.acfunBangumiCoverImgDownload(section, i - 1, bangumiData, bangumiList, se, ip)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Acfun Bangumi Video Download Pic Return")
        return 0
    if not che:
        if log:
            logg.write(f"GET {s}", currentframe(), "GET NORMAL/BANGUMI VIDEO WEBPAGE")
        re = section.get(s)
        if log:
            logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET NORMAL/BANGUMI VIDEO WEBPAGE RESULT")
        rtry = 0
        while re.status_code == 412 and rtry < 3:
            biliLogin.dealwithcap(section, s, logg)
            if log:
                logg.write(f"GET {s}", currentframe(), "GET NORMAL/BANGUMI VIDEO WEBPAGE2")
            re = section.get(s)
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET NORMAL/BANGUMI VIDEO WEBPAGE2 RESULT")
            rtry = rtry + 1
        if re.status_code == 412:
            print(lan['SPERROR'].replace('<url>', s))
            return -1
        parser = HTMLParser.Myparser()
        parser.feed(re.text)
        if log:
            logg.write(f"parser.videodata = {parser.videodata}", currentframe(), "NORMAL/BANGUMI VIDEO DATA")
        try:
            vd = json.loads(parser.videodata, strict=False)
        except Exception:
            if log:
                logg.write(traceback.format_exc(), currentframe(), "NORMAL/BANGUMI VIDEO DATA INVALID")
            if av:
                re = search(r"av([0-9]+)", s, I).groups()[0]
                if log:
                    logg.write(f"GET https://api.bilibili.com/x/web-interface/view/detail?bvid=&aid={re}&jsonp=jsonp", currentframe(), "GET NORMAL VIDEO INFO")
                re = section.get("https://api.bilibili.com/x/web-interface/view/detail?bvid=&aid=%s&jsonp=jsonp" % (re))
                re.encoding = 'utf8'
                if log:
                    logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET NORMAL VIDEO INFO RESULT")
                re = re.json()
                if re['code'] != 0:
                    print('%s %s' % (re['code'], re['message']))
                    return -1
                if 'data' in re and 'View' in re['data'] and 'redirect_url' in re['data']['View']:
                    ip2 = copyip(ip)
                    ip2['i'] = re['data']['View']['redirect_url']
                    ip2['uc'] = False
                    if 'p' in ip:
                        ip2['p'] = ip['p']
                    if log:
                        logg.write(f"ip2 = {ip2}", currentframe(), "NORMAL VIDEO DIRECT PARA")
                    read = main(ip2)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "NORMAL VIDEO DIRECT RETURN")
                    return read
                print(traceback.format_exc())
                return -1
            elif ss or ep:
                if re.status_code == 404:
                    print('404 Not Found')
                    s = s.replace('bangumi', 'cheese')
                    print(lan['OUTPUT12'].replace('<link>', s))  # 尝试重定向至"<link>"。
                    ip['i'] = s
                    ip['uc'] = False
                    if log:
                        logg.write(f"ip = {ip}", currentframe(), "BANGUMI VIDEO DIRECT PARA")
                    read = main(ip)
                    if log:
                        logg.write(f"read = {read}", currentframe(), "BANGUMI VIDEO DIRECT RETURN")
                    return read
                print(traceback.format_exc())
                return -1
            else:
                print(traceback.format_exc())
                return -1
        if 'error' in vd and 'code' in vd['error'] and vd['error']['code'] != 0:
            if 'message' in vd['error'] and vd['error']['message'] is not None:
                print('%s %s' % (vd['error']['code'], vd['error']['message']))
            if(vd['error']['trueCode'] == 62002 or vd['error']['trueCode'] == -404):
                return NOT_FOUND
            if vd['error']['trueCode'] == -200:
                ip2 = copyip(ip)
                if 'p' in ip:
                    ip2['p'] = ip['p']
                ip2['i'] = urljoin('https://www.bilibili.com', vd['error']['forward'])
                ip2['uc'] = False
                if log:
                    logg.write(f"ip2 = {ip2}", currentframe(), "VIDEO CONFLICT REDIRECT PARAMETERS")
                read = main(ip2)
                if log:
                    logg.write(f"read = {read}", currentframe(), "VIDEO CONFLICT REDIRECT RETURN")
                return read
            return -1
    if av:
        data = JSONParser.Myparser(parser.videodata)
        if log:
            logg.write(f"data = {data}", currentframe(), "NORMAL VIDEO FILTERED DATA")
        if data == -1:
            re = search(r"av([0-9]+)", s, I).groups()[0]
            if log:
                logg.write(f"GET https://api.bilibili.com/x/web-interface/view/detail?bvid=&aid={re}&jsonp=jsonp", currentframe(), "GET NORMAL VIDEO INFO2")
            re = section.get(f"https://api.bilibili.com/x/web-interface/view/detail?bvid=&aid={re}&jsonp=jsonp")
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET NORMAL VIDEO INFO2 RESULT")
            re = re.json()
            if re['code'] != 0:
                print(f"{re['code']} {re['message']}")
                if re['code'] == -404:
                    return NOT_FOUND
                return -1
            if 'data' in re and 'View' in re['data'] and 'redirect_url' in re['data']['View']:
                ip2 = copyip(ip)
                ip2['i'] = re['data']['View']['redirect_url']
                ip2['uc'] = False
                if 'p' in ip:
                    ip2['p'] = ip['p']
                if log:
                    logg.write(f"ip2 = {ip2}", currentframe(), "NORMAL VIDEO DIRECT2 PARA")
                read = main(ip2)
                if log:
                    logg.write(f"read = {read}", currentframe(), "NORMAL VIDEO DIRECT2 RETURN")
                return read
        if data['videos'] != len(data['page']):
            r = requests.Session()
            r.headers = copydict(section.headers)
            r.proxies = section.proxies
            if nte:
                r.trust_env = False
            read = JSONParser.loadcookie(r, logg)
            if read != 0:
                print(lan['ERROR10'])  # 读取cookies.json出现错误
                return -1
            r.headers.update({'referer': "https://www.bilibili.com/video/%s" % (data['bvid'])})
            r.cookies.set('CURRENT_QUALITY', '125', domain='.bilibili.com', path='/')
            r.cookies.set('CURRENT_FNVAL', '80', domain='.bilibili.com', path='/')
            r.cookies.set('laboratory', '1-1', domain='.bilibili.com', path='/')
            r.cookies.set('stardustvideo', '1', domain='.bilibili.com', path='/')
            uri = f"https://api.bilibili.com/x/player.so?id=cid:{data['page'][0]['cid']}&aid={data['aid']}&bvid={data['bvid']}&buvid={r.cookies.get('buvid3')}"
            if log:
                logg.write(f"GET {uri}", currentframe(), "GET PLAYER.SO")
            re = r.get(uri)
            re.encoding = 'utf8'
            if log:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET PLAYER.SO RESULT")
            rs = search(r"<interaction>(.+)</interaction>", re.text, I)
            if rs is not None:
                rs = rs.groups()[0]
                if log:
                    logg.write(f"rs = {rs}", currentframe(), "PLAYER.SO REGEX")
                if rs != "":
                    rs = json.loads(rs)
                    data['gv'] = rs['graph_version']
                    hd = True
        if hd:
            p = HDVideoParser(r, data, logg)
            read = p.parser()
            if log:
                logg.write(f"read = {read}", currentframe(), "Parse HD Video Return")
            if read == -1:
                return -1
        if ns:
            PrintInfo.printInfo(data)
        cho = []
        if data['videos'] == 1:
            cho.append(1)
        else:
            bs = True
            f = True
            while bs:
                if f and 'p' in ip:
                    f = False
                    inp = ip['p']
                elif ns:
                    inp = input(lan['OUTPUT4'])  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
                else:
                    print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                    return -1
                cho = []
                if inp[0] == 'a':
                    if ns:
                        print(lan['OUTPUT5'])  # 您全选了所有视频
                    for i in range(1, data['videos'] + 1):
                        cho.append(i)
                    bs = False
                else:
                    inp = inp.split(',')
                    bb = True
                    for i in inp:
                        if i.isnumeric() and int(i) > 0 and int(i) <= data['videos'] and (not (int(i) in cho)):
                            cho.append(int(i))
                        else:
                            rrs = search(r"([0-9]+)-([0-9]+)", i)
                            if rrs is not None:
                                rrs = rrs.groups()
                                i1 = int(rrs[0])
                                i2 = int(rrs[1])
                                if i2 < i1:
                                    tt = i1
                                    i1 = i2
                                    i2 = tt
                                for i in range(i1, i2 + 1):
                                    if i > 0 and i <= data['videos'] and (not (i in cho)):
                                        cho.append(i)
                            else:
                                bb = False
                    if bb:
                        bs = False
                        for i in cho:
                            if ns:
                                print(lan['OUTPUT6'] + str(i) + ',' + data['page'][i - 1]['part'])  # 您选中了视频：
        cho2 = 0
        bs = True
        if 'd' in ip:
            bs = False
            cho2 = ip['d']
        while bs:
            if not ns:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            inp = input(lan['INPUT9'])  # 请输入你要下载的方式：\n1.当前弹幕下载\n2.全弹幕下载（可能需要大量时间）\n3.视频下载\n4.当前弹幕+视频下载\n5.全弹幕+视频下载\n6.仅字幕下载\n7.仅封面图片下载
            if inp[0].isnumeric() and int(inp[0]) > 0 and int(inp[0]) < 9:
                cho2 = int(inp[0])
                bs = False
        if cho2 == 1 or cho2 == 4:
            for i in cho:
                read = biliDanmu.DanmuGetn(i, data, section, 'av', xml, xmlc, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Normal Video Download Barrage Return")
                if read == -1 or read == -4 or read == -2:
                    pass
                elif read == 0:
                    print(lan['OUTPUT9'].replace('<number>', str(i)))  # <number>P下载完成
                else:
                    return -1
        if cho2 == 2 or cho2 == 5:
            read = biliTime.equal(biliTime.getDate(data['pubdate']), biliTime.getNowDate())
            if read == 0 or read == 1:
                print(lan['ERROR12'])  # 该视频不支持全弹幕！
                pass
            for i in cho:
                read = biliDanmu.DanmuGeta(i, data, section, 'av', xml, xmlc, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Normal Video Download All Barrage Return")
                if read == -2 or read == -1 or read == -3:
                    pass
                elif read == 0:
                    print(lan['OUTPUT9'].replace('<number>', str(i)))  # <number>P下载完成
                else:
                    return -1
        if (cho2 > 2 and cho2 < 6) or cho2 == 8:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                if ip['m']:
                    bs = False
                    cho3 = True
                else:
                    bs = False
                    cho3 = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            cho5 = False
            bs = True
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'cd')
            if read is True:
                bs = False
                cho5 = True
            elif read is False:
                bs = False
            if 'ac' in ip:
                if ip['ac']:
                    bs = False
                    cho5 = True
                else:
                    bs = False
                    cho5 = False
            while bs:
                inp = input(f'{lan["INPUT2"]}(y/n)')
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho5 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}\ncho5 = {cho5}", currentframe(), "Normal Video Download Video/Audio Para")
            if cho2 == 8:
                for i in cho:
                    read = videodownload.avaudiodownload(data, section, i, ip, se, s, cho3, cho5, ud)
            else:
                for i in cho:
                    read = videodownload.avvideodownload(i, s, data, section, cho3, cho5, se, ip, ud)
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Video Download Video/Audio Return")
            if read == -5 or read == -6:
                return -1
        if cho2 == 6:
            for i in cho:
                read = videodownload.avsubdownload(i, s, data, section, se, ip, ud)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Normal Video Download Subtitles Only Return")
        if cho2 == 7:
            read = videodownload.avpicdownload(data, section, ip, se)
            if log:
                logg.write(f"read = {read}", currentframe(), "Normal Video Download Cover Only Return")
    if ss or ep:
        if ep:
            epl = lan['INPUT10']  # ，仅下载输入的ep号可输入b
        else:
            epl = ''
        led = -1  # 上一次播放epid
        if che:
            le = PrintInfo.printInfo2(vd, ns)
            if 'led' in vd:
                led = vd['led']
            data = vd
        else:
            data = JSONParser.Myparser2(parser.videodata)
            le = PrintInfo.printInfo2(data, ns)
            rs = search(r'__PGC_USERSTATE__=([^<]+)', re.text)
            if rs is not None:
                rs = rs.groups()[0]
                if log:
                    logg.write(f"rs = {rs}", currentframe(), "Normal Bangumi Data Regex")
                pgc = json.loads(rs)
                if 'progress' in pgc and pgc['progress'] is not None:
                    if 'last_ep_id' in pgc['progress'] and pgc['progress']['last_ep_id'] > -1:
                        led = pgc['progress']['last_ep_id']
        epr = ""
        if led > -1:
            epr = lan['INPUT11'].replace('<number>', str(led))  # ，下载上次观看的EP<number>可输入l
        cho = []
        if le == 1:
            cho.append(1)
            cho = chon.getcho(cho, data)
        else:
            bs = True
            f = True
            while bs:
                if f and 'p' in ip:
                    inp = ip['p']
                    f = False
                elif ns:
                    tee = ""
                    if epl != "" or epr != "":
                        tee = f"({epl}{epr})"
                    inp = input(lan['OUTPUT4'] + tee)  # 请输入你想下载的视频编号（每两个编号间用,隔开，全部下载可输入a）：
                else:
                    print(lan['ERROR9'])  # 请使用-p <number>选择视频编号
                    return -1
                cho = []
                if len(inp) > 0:
                    if inp[0] == 'a':
                        if ns:
                            print(lan['OUTPUT5'])  # 您全选了所有视频
                        for j in range(1, le + 1):
                            cho.append(j)
                        bs = False
                    elif ep and inp[0] == 'b':
                        if che:
                            iii = 1
                            co = True
                            for i in data['epList']:
                                if epid == i['id']:
                                    co = False
                                    break
                                iii = iii + 1
                            if not co:
                                cho.append(iii)
                                bs = False
                        else:
                            iii = 1
                            co = True
                            if 'epList' in data:
                                for i in data['epList']:
                                    if i['loaded']:
                                        co = False
                                        break
                                    iii = iii + 1
                            if co and 'sections' in data:
                                for i in data['sections']:
                                    for j in i['epList']:
                                        if j['loaded']:
                                            co = False
                                            break
                                        iii = iii + 1
                            if not co:
                                cho.append(iii)
                                bs = False
                    elif led > -1 and inp[0] == 'l':
                        iii = 1
                        co = True
                        if 'epList' in data:
                            for i in data['epList']:
                                if i['id'] == led:
                                    co = False
                                    break
                                iii = iii + 1
                        if co and 'sections' in data:
                            for i in data['sections']:
                                for j in i['epList']:
                                    if j['id'] == led:
                                        co = False
                                        break
                                    iii = iii + 1
                        if not co:
                            cho.append(iii)
                            bs = False
                    else:
                        inp = inp.split(',')
                        bb = True
                        for i in inp:
                            if i.isnumeric() and int(i) <= le and int(i) > 0 and (not (int(i) in cho)):
                                cho.append(int(i))
                            else:
                                rrs = search(r"([0-9]+)-([0-9]+)", i)
                                if rrs is not None:
                                    rrs = rrs.groups()
                                    i1 = int(rrs[0])
                                    i2 = int(rrs[1])
                                    if i2 < i1:
                                        tt = i1
                                        i1 = i2
                                        i2 = tt
                                    for i in range(i1, i2 + 1):
                                        if i > 0 and i <= le and (not (i in cho)):
                                            cho.append(i)
                                else:
                                    bb = False
                        if bb:
                            bs = False
                cho = chon.getcho(cho, data)
                if ns:
                    PrintInfo.printcho(cho)
        cho2 = 0
        bs = True
        if 'd' in ip:
            bs = False
            cho2 = ip['d']
        while bs:
            if not ns:
                print(lan['ERROR11'])  # 请使用-d <method>选择下载方式
                return -1
            inp = input(lan['INPUT12'])  # 请输入你要下载的方式：\n1.当前弹幕下载\n2.全弹幕下载（可能需要大量时间）\n3.视频下载\n4.当前弹幕+视频下载\n5.全弹幕+视频下载\n7.仅封面图片下载
            if inp[0].isnumeric() and ((int(inp[0]) > 0 and int(inp[0]) < 6) or int(inp[0]) == 7 or int(inp[0]) == 8):
                cho2 = int(inp[0])
                bs = False
        if cho2 == 1 or cho2 == 4:
            for i in cho:
                read = biliDanmu.DanmuGetn(i, data, section, 'ss', xml, xmlc, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bagumi Download Barrige Retrun")
                if read == -1 or read == -4 or read == -2:
                    pass
                elif read == 0:
                    print(lan['OUTPUT10'].replace('<title>', i['titleFormat']))  # <title>下载完成
                else:
                    return -1
        if cho2 == 2 or cho2 == 5:
            for i in cho:
                read = biliDanmu.DanmuGeta(i, data, section, 'ss', xml, xmlc, ip, se, che)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Download All Barrage Return")
                if read == 0:
                    print(lan['OUTPUT10'].replace('<title>', i['titleFormat']))  # <title>下载完成
                elif read >= -3:
                    pass
                else:
                    return -1
        if (cho2 > 2 and cho2 < 6) or cho2 == 8:
            bs = True
            cho3 = False
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'mp')
            if read is True:
                bs = False
                cho3 = True
            elif read is False:
                bs = False
            if 'm' in ip:
                if ip['m']:
                    bs = False
                    cho3 = True
                else:
                    bs = False
                    cho3 = False
            while bs:
                inp = input(f'{lan["INPUT8"]}(y/n)')  # 是否要默认下载最高画质（这样将不会询问具体画质）？
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho3 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            cho5 = False
            bs = True
            if not ns:
                bs = False
            read = JSONParser.getset(se, 'cd')
            if read is True:
                bs = False
                cho5 = True
            elif read is False:
                bs = False
            if 'ac' in ip:
                if ip['ac']:
                    bs = False
                    cho5 = True
                else:
                    bs = False
                    cho5 = False
            while bs:
                inp = input(f'{lan["INPUT2"]}(y/n)')
                if len(inp) > 0:
                    if inp[0].lower() == 'y':
                        cho5 = True
                        bs = False
                    elif inp[0].lower() == 'n':
                        bs = False
            if log:
                logg.write(f"cho3 = {cho3}\ncho5 = {cho5}", currentframe(), "Bangumi Video Download Para")
            if cho2 == 8:
                for i in cho:
                    read = videodownload.epaudiodownload(i, f"https://www.bilibili.com/bangumi/play/ss{data['mediaInfo']['ssId']}", data, section, cho3, cho5, se, ip, ud)
            else:
                for i in cho:
                    read = videodownload.epvideodownload(i, f"https://www.bilibili.com/bangumi/play/ss{data['mediaInfo']['ssId']}", data, section, cho3, cho5, se, ip, ud)
            if log:
                logg.write(f"read = {read}", currentframe(), "Bangumi Video Download Return")
            if read == -5 or read == -6:
                return -1
        if cho2 == 7:
            for i in cho:
                read = videodownload.eppicdownload(i, data, section, ip, se)
                if log:
                    logg.write(f"read = {read}", currentframe(), "Bangumi Video Cover Download Return")
    return 0


if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
    if 'SHOW' in ip:
        PrintInfo.prc()
        sys.exit(0)
log = True
logg = None
if 'log' in se:
    log = se['log']
if 'log' in ip:
    log = ip['log']
if log:
    seipt = f"Settings: {se}\nCommand Line parameters: {ip}"
    logg = Logger()
    ip['logg'] = logg
    logg.write(seipt)
ol = True
if 'ol' in se:
    ol = se['ol']
if 'ol' in ip:
    ol = ip['ol']
if ol:
    ip['oll'] = autoopenfilelist(logg)
lan = getdict('start', getlan(se, ip))


class mains(Thread):
    def __init__(self, ip: dict):
        Thread.__init__(self)
        self.ip = ip

    def run(self):
        main(self.ip)


if __name__ == "__main__":
    PrintInfo.pr()
    res = -1
    if not log or __debug__:
        res = main(ip)
    else:
        try:
            res = main(ip)
        except:
            te = traceback.format_exc()
            print(te)
            logg.write(te, currentframe(), "Main Function Except")
            if not logg.hasf():
                logg.openf(f'log/{round(time())}.log')
            logg.flush()
            logg.closef()
    if 'oll' in ip:
        ip['oll'].open()
    sys.exit(res)
else:
    print(lan['OUTPUT11'])  # 请运行start.py
