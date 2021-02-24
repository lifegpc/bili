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
from command import gopt
from time import localtime, strftime
from biliTime import tostr2, tostr6
from bstr import gettags, rhtml
from JSONParser import loadset
import sys
from lang import getdict, getlan


def printInfo(data):
    "输出普通AV号获取的信息"
    print(lan['O1'] + str(data['aid']))  # AV号：
    print(lan['O2'] + data['bvid'])  # BV号：
    print(lan['O3'] + str(data['videos']))  # 分P数：
    print(lan['O4'] + data['title'])  # 标题：
    print(lan['O5'] + strftime("%Y-%m-%d %H:%M:%S", localtime(data['pubdate'])))  # 发布时间：
    print(lan['O6'] + strftime("%Y-%m-%d %H:%M:%S", localtime(data['ctime'])))  # 上次修改时间：
    print(lan['O7'] + data['desc'])  # 描述：
    print(lan['O8'])  # UP主信息：
    print("UID：" + str(data['uid']))
    print(lan['O9'] + data['name'])  # 名字：
    print(lan['O10'])  # 分P信息：
    for i in data['page']:
        print(lan['O11'].replace('<number>', str(i['page'])))  # 第<number>P：
        print("CID：" + str(i['cid']))
        print(lan['O12'] + i['part'])  # 分P名：


def printInfo2(data, ns: bool):
    "未完成"
    if 'mediaInfo' in data and ns:
        t = data['mediaInfo']
        print("ID：" + str(t['id']))
        print("SSID：" + str(t['ssId']))
        print(lan['O4'] + t['title'])  # 标题：
        if t['jpTitle'] != '':
            print(lan['O13'] + t['jpTitle'])  # 日语名字：
        if t['series'] != '':
            print(lan['O14'] + t['series'])  # 系列名字：
        if t['alias'] != '':
            print(lan['O15'] + t['alias'])  # 别名：
        print(lan['O7'] + t['evaluate'])  # 简介：
        print(lan['O16'] + t['type'])  # 类型：
        print(lan['O5'] + t['time'])  # 发布时间：
    ii = 1
    if 'epList' in data:
        if ns:
            print(lan['O17'])  # 内容：
        for i in data['epList']:
            if not ns:
                ii = ii + 1
                continue
            print(str(ii) + "." + i['titleFormat'])
            ii = ii + 1
            print(lan['O4'] + i['longTitle'])  # 标题：
            print(lan['O1'] + str(i['aid']))  # AV号：
            print(lan['O2'] + str(i['bvid']))  # BV号：
            print('CID:' + str(i['cid']))
            print('ID:' + str(i['id']))
    if 'sections' in data:
        for i in data['sections']:
            if ns:
                print(i['title'] + ":")
            for j in i['epList']:
                if not ns:
                    ii = ii + 1
                    continue
                print(str(ii) + "." + j['titleFormat'])
                ii = ii + 1
                print(lan['O4'] + j['longTitle'])  # 标题：
                print(lan['O1'] + str(j['aid']))  # AV号：
                print(lan['O2'] + str(j['bvid']))  # BV号：
                print('CID:' + str(j['cid']))
                print('ID:' + str(j['id']))
    return ii - 1


def printInfo3(d: dict):
    print(f"{lan['O18']}{d['id']}")  # 收藏夹ID：
    print(f"{lan['O19']}{d['title']}")  # 收藏夹标题：
    print(f"{lan['O20']}{d['author']}")  # 创建者名字：
    print('UID：%s' % (d['uid']))
    print(f"{lan['O21']}{tostr2(d['ctime'])}")  # 创建时间：
    print(f"{lan['O6']}{tostr2(d['mtime'])}")  # 修改时间：
    print(f"{lan['O22']}{d['count']}")  # 视频数量：


def printInfo4(l: list):  # noqa: E741
    ii = 1
    for i in l:
        print(lan['O23'].replace('<number>', str(ii)))  # 视频<number>：
        print(f"{lan['O1']}{i['id']}")  # AV号：
        print(f"{lan['O2']}{i['bvid']}")  # BV号：
        print(f"{lan['O4']}{i['title']}")  # 标题：
        print(f"{lan['O24']}{i['author']}")  # UP主名称：
        print(f"{lan['O25']}{tostr2(i['ftime'])}")  # 收藏时间：
        ii = ii + 1


def printInfo5(l: list):  # noqa: E741
    e = 1
    for i in l:
        print(f"{e}.{lan['O26']}{i['cid']}")  # 频道ID：
        print(f"{lan['O9']}{i['name']}")  # 名字：
        print(f"{lan['O7']}{i['intro']}")  # 介绍：
        print(f"{lan['O6']}{tostr2(i['mtime'])}")  # 上次修改时间：
        print(f"{lan['O22']}{i['count']}")  # 视频数量：
        e = e + 1


def printInfo6(l: list, d: dict):  # noqa: E741
    print(f"{lan['O26']}{d['cid']}")  # 频道ID：
    print(f"{lan['O9']}{d['name']}")  # 名字：
    print(f"{lan['O7']}{d['intro']}")  # 介绍：
    print(f"{lan['O6']}{tostr2(d['mtime'])}")  # 上次修改时间：
    print(f"{lan['O22']}{d['count']}")  # 视频数量：
    e = 1
    for i in l:
        print(lan['O23'].replace('<number>', str(e)))  # 视频%s：
        print(f"{lan['O1']}{i['aid']}")  # AV号：
        print(f"{lan['O2']}{i['bvid']}")  # BV号：
        print(f"{lan['O4']}{i['title']}")  # 标题：
        e = e + 1


def printInfo7(u: dict, l: list):  # noqa: E741
    print(f"{lan['O24']}{u['n']}")  # UP主名字：
    print(f"{lan['O27']}{u['s']}")  # UP主性别：
    print(f"{lan['O28']}{u['l']}")  # UP主等级：
    print(f"{lan['O29']}{u['sign']}")  # 个性签名：
    print(f"{lan['O30']}{u['b']}")  # 生日：
    e = 1
    for i in l:
        print(lan['O23'].replace('<number>', str(e)))  # 视频%s：
        print(f"{lan['O1']}{i['aid']}")  # AV号：
        print(f"{lan['O2']}{i['bvid']}")  # BV号：
        print(f"{lan['O4']}{i['title']}")  # 标题：
        print(f"{lan['O7']}{i['description']}")  # 描述：
        print(f"{lan['O21']}{tostr2(i['ctime'])}")  # 创建时间：
        e = e + 1


def printInfo8(d: dict):
    k = 1
    for i in d['data']['list']:
        print(lan['O31'].replace('<number>', str(k)))  # 收藏夹%s：
        print(f"{lan['O18']}{i['id']}")  # 收藏夹ID：
        print(f"{lan['O19']}{i['title']}")  # 收藏夹名字：
        k = k + 1


def printInfo9(d: dict):
    print(f"{lan['O32']}{d['id']}")  # 小视频ID：
    print(f"{lan['O7']}{d['description']}")  # 描述：
    print(f"{lan['O33']}{gettags(d['tags'])}")  # 标签：
    print(f"{lan['O34']}{d['upload_time']}")  # 上传时间：
    print(f"{lan['O24']}{d['name']}")  # UP主名字：
    print('UID：%s' % (d['uid']))


def printInfo10(l: list):  # noqa: E741
    t = 1
    for i in l:
        print(f"{t}.{lan['O4']}{i['title']}")  # 标题：
        print(f"{lan['O7']}{i['sub_title']}")  # 描述：
        print(f"UID：{i['up_id']}")
        print(f"SSID：{i['id']}")
        t = t + 1


def printcho(cho):
    if len(cho) == 0:
        return
    print(lan['O35'], end='')  # 你选中了
    for i in cho:
        print('%s,' % (i['titleFormat']), end='')
    print()


def printlr(d: dict):
    print(f"{lan['O36']}{d['rid']}")  # 直播回放ID：
    print(f"{lan['O37']}{d['roomid']}")  # 房间ID：
    print(f"{lan['O24']}{d['name']}")  # UP主：
    print('UID：%s' % (d['uid']))
    print(f"{lan['O27']}{d['sex']}")  # UP主性别：
    print(f"{lan['O29']}{d['sign']}")  # UP主个性签名：
    print(f"{lan['O4']}{d['title']}")  # 直播名称：
    print(f"{lan['O38']}{tostr2(d['st'])}")  # 开始时间：
    print(f"{lan['O39']}{tostr2(d['et'])}")  # 结束时间：
    print(f"{lan['O7']}{rhtml(d['des'])}")  # 简介：
    print(f"{lan['O40']}{d['parean']}-{d['arean']}")  # 区域：
    print(f"{lan['O33']}{d['tags']}")  # 房间标签：
    print(f"{lan['O41']}{gettags(d['hotwords'])}")  # 房间热词：


def printliveInfo(d: dict):
    print(f"{lan['O37']}{d['roomid']}")  # 房间ID：
    print(f"{lan['O4']}{d['title']}")  # 标题：
    print(f"{lan['O24']}{d['name']}")  # UP主名称：
    print(f"UID：{d['uid']}")
    print(f"{lan['O27']}{d['sex']}")  # UP主性别：
    print(f"{lan['O29']}{d['sign']}")  # 个性签名：
    print(f"{lan['O38']}{d['livetime']}")  # 开始时间：
    print(f"{lan['O7']}{rhtml(d['des'])}")  # 简介：
    print(f"{lan['O40']}{d['pareaname']}-{d['areaname']}")  # 区域：
    print(f"{lan['O33']}{d['tags']}")  # 标签：
    print(f"{lan['O41']}{gettags(d['hotwords'])}")  # 房间热词


def printAuInfo(d: dict):
    print(f"{lan['O44']}{d['id']}")  # AU号
    if d['aid'] != 0:
        print(f"{lan['O1']}{d['aid']}")
        print(f"{lan['O2']}{d['bvid']}")
        if d['cid'] != 0:
            print(f"CID: {d['cid']}")
    print(f"{lan['O4']}{d['title']}")
    if 'passtime' in d and d['passtime'] is not None and d['passtime'] != 0:
        print(f"{lan['O5']}{tostr2(d['passtime'])}")
    if 'ctime' in d and d['ctime'] is not None and d['ctime'] != 0:
        print(f"{lan['O6']}{tostr2(d['ctime']/1000)}")
    if 'uid' in d and d['uid'] is not None and d['uid'] != 0:
        print(f"{lan['O7']}{d['intro']}")
    print(f"{lan['O45']}{tostr6(d['duration'])}")
    print(f"{lan['O33']}{gettags(d['tags'])}")
    print(f"{lan['O46']}{d['author']}")
    if 'uid' in d and d['uid'] is not None and d['uid'] != 0:
        print(lan['O8'])
        print(f"UID :{d['uid']}")
        print(f"{lan['O9']}{d['uname']}")
    if 'pgc_info' in d and d['pgc_info'] is not None and type(d['pgc_info']) == dict:
        pgc_info = d['pgc_info']
        if 'pgc_menu' in pgc_info and pgc_info['pgc_menu'] is not None and type(pgc_info['pgc_menu']) == dict:
            pgc_menu = pgc_info['pgc_menu']
            print(lan['O53'])
            print(f"{lan['O55']}{pgc_menu['title']}")
            print(f"{lan['O54']}{pgc_menu['mbnames']}")
            print(f"{lan['O56']}{pgc_menu['publisher']}")
            print(f"{lan['O57']}{tostr2(pgc_menu['pubTime'])}")
            if 'tags' in pgc_menu and pgc_menu['tags'] is not None and type(pgc_menu['tags']) == list:
                print(f"{lan['O58']}{gettags(pgc_menu['tags'], lambda d: d['itemVal'])}")
            print(f"{lan['O59']}{pgc_menu['playNum']}")
            print(f"{lan['O60']}{pgc_menu['collNum']}")
    print(lan['O47'])
    s = d['statistic']
    print(f"{lan['O48']}{s['play']}")
    print(f"{lan['O49']}{s['comment']}")
    print(f"{lan['O50']}{s['share']}")
    print(f"{lan['O51']}{s['collect']}")


def printAmInfo(d: dict):
    m = d['menusRespones']
    l = d['songsList']  # noqa: E741
    print(f"{lan['O61']}{m['menuId']}")  # AM号
    if m['collectionId'] > 0:
        print(f"{lan['O62']}{m['collectionId']}")  # 收藏夹ID
    print(f"{lan['O4']}{m['title']}")  # 标题
    if 'intro' in m and m['intro'] is not None and m['intro'] != '':
        print(f"{lan['O7']}{m['intro']}")  # 描述
    if 'mbnames' in m and m['mbnames'] is not None and m['mbnames'] != '':
        print(f"{lan['O54']}{m['mbnames']}")  # 专辑艺术家
    if m['pbtime'] > 0:
        print(f"{lan['O5']}{tostr2(m['pbtime']/1000)}")  # 发布时间
    elif m['patime'] > 0:
        print(f"{lan['O5']}{tostr2(m['patime']/1000)}")
    if m['ctime'] > 0:
        print(f"{lan['O6']}{tostr2(m['ctime']/1000)}")  # 创建时间
    if m['uid'] > 0:
        print(lan['O8'])  # 上传者信息
        print(f"UID: {m['uid']}")
        print(f"{lan['O9']}{m['uname']}")  # 名字
    print(lan['O47'])
    print(f"{lan['O51']}{m['collectNum']}")  # 收藏次数
    print(f"{lan['O49']}{m['commentNum']}")  # 评论数量
    print(f"{lan['O48']}{m['playNum']}")  # 播放次数
    print(f"{lan['O50']}{m['snum']}")  # 分享次数
    print(lan['O63'])
    k = 1
    for i in l:
        print(f"{k}. {lan['O44']}{i['song_id']}")  # AU号
        print(f"{lan['O4']}{i['title']}")  # 标题
        print(f"{lan['O46']}{i['author']}")  # 作者
        print(f"{lan['O45']}{tostr6(i['duration'])}")  # 时长
        k = k + 1


def printAcInfo(d: dict):
    print(f"{lan['O64']}{d['dougaId']}")  # CV号
    print(f"{lan['O3']}{len(d['videoList'])}")  # 分P数
    print(f"{lan['O4']}{d['title']}")  # 标题
    print(f"{lan['O5']}{tostr2(d['createTimeMillis']/1000)}")  # 发布时间
    print(f"{lan['O7']}{d['description']}")  # 描述
    print(lan['O8'])  # UP主信息：
    print(f"UID：{d['user']['id']}")
    print(f"{lan['O9']}{d['user']['name']}")  # 名字
    print(lan['O10'])  # 分P信息
    k = 0
    for i in d['videoList']:
        k += 1
        print(lan['O11'].replace('<number>', str(k)))  # 第<number>P
        print(f"ID：{i['id']}")
        print(f"{lan['O12']}{i['title']}")  # 分P名


def printplitid(d: list):
    for i in d:
        print(f"{lan['O52']}{i['tid']}")
        print(f"{lan['O16']}{i['name']}")
        print(f"{lan['O22']}{i['count']}")


def pr():
    print(f"""    bili  Copyright (C) 2019-2021  lifegpc
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    {lan['O42']}
""")


def prc():
    try:
        f = open("LICENSE", "r", encoding="utf8")
        t = f.readline()
        while t:
            print(t)
            t = f.readline()
        f.close()
    except:
        print(lan['O43'])  # 找不到GNU GPL3 LICENSE文件，请看<http://www.gnu.org/licenses/>。


lan = None
se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
lan = getdict('PrintInfo', getlan(se, ip))
