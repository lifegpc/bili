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
from requests import Session
from JSONParser import loadset
import sys
from lang import getdict,getlan
from command import gopt
from inspect import currentframe
from traceback import format_exc
from typing import Callable, List


StrList = List[str]
lan=None
se=loadset()
if se==-1 or se==-2 :
    se={}
ip={}
if len(sys.argv)>1 :
    ip=gopt(sys.argv[1:])
lan=getdict('JSONParser2',getlan(se,ip))
def getplinfo(d:dict) :
    t=d['data']['info']
    r={}
    r['id']=t['id']
    r['fid']=t['fid']
    r['uid']=t['mid']
    r['title']=t['title']
    r['author']=t['upper']['name']
    r['ctime']=t['ctime']
    r['mtime']=t['mtime']
    r['count']=t['media_count']
    return r
def getpli(r, f, i, d: dict, logg=None):
    uri = f"https://api.bilibili.com/x/v3/fav/resource/list?media_id={f}&pn={i}&ps=20&keyword={d['k']}&order={d['order']}&type={d['t']}&tid={d['tid']}&jsonp=jsonp"
    if logg is not None:
        logg.write(f"GET {uri}", currentframe(), "GET PLI INFO")
    bs=True
    while bs :
        try :
            re=r.get(uri)
            bs=False
        except :
            if logg is not None:
                logg.write(format_exc(), currentframe(), "GET PLI INFO ERROR")
            print(lan['OUTPUT1'].replace('<number>',str(i)))#获取收藏夹第%s页失败，正在重试……
    re.encoding='utf8'
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET PLI INFO RESULT")
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    return re
def getpliv(i:list,d:dict):
    for t in d['data']['medias']:
        r={}
        r['id']=t['id']
        r['title']=t['title']
        r['page']=t['page']
        r['duration']=t['duration']
        r['uid']=t['upper']['mid']
        r['author']=t['upper']['name']
        r['collect']=t['cnt_info']['collect']
        r['danmuku']=t['cnt_info']['danmaku']
        r['play']=t['cnt_info']['play']
        r['bvid']=t['bvid']
        r['ctime']=t['ctime']
        r['pubtime']=t['pubtime']
        r['ftime']=t['fav_time']
        i.append(r)


def getpltid(r: Session, fid: int, uid: int, logg=None):
    uri = f"https://api.bilibili.com/x/v3/fav/resource/partition?up_mid={uid}&media_id={fid}&jsonp=jsonp"
    if logg:
        logg.write(f"GET {uri}", currentframe(), "GET Pli Tid List")
    re = r.get(uri)
    re.encoding = 'utf8'
    if logg:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "Get Pli Tid List Result")
    re = re.json()
    if re['code'] != 0:
        print(f"{re['code']} {re['message']}")
        return -1
    return re['data']


def dealwithauapi(d: dict, d2: dict):
    "处理客户端API和网页端API的差异"
    def add(k: str, v=None, d: dict=d):
        "增加空值"
        if k not in d:
            d[k] = v
    def rep(k: str, nonev='', k2: str=None, nonev2=None, f: Callable=None, l: StrList=[], l2: StrList=[], strict: bool=False, d: dict=d, d2: dict=d2):
        "检查是否需要覆盖并覆盖"
        for s in l:
            if s not in d or d[s] is None or type(d[s]) != dict:
                if s not in d or d[s] is None:
                    d[s] = {}
                else:
                    return
            d = d[s]
        for s in l2:
            if s not in d2 or d2[s] is None or type(d2[s]) != dict:
                    return
            d2 = d2[s]
        if k2 is None or k2 == '':
            k2 = k
        if nonev2 is None:
            nonev2 = nonev
        if f is None:
            f = lambda s : s
        if k not in d or d[k] is None or d[k] == nonev:
            if k2 in d2 and d2[k2] is not None:
                if (k not in d or d[k] is None) and not strict:
                    d[k] = f(d2[k2])
                elif d2[k2] != nonev2:
                    d[k] = f(d2[k2])
    rep('activities', [])
    add('activityId', 0)
    rep('aid', 0, 'avid', '', lambda s : int(s[2:]) if s[2:] != "" else 0)
    rep('album_id')
    rep('attr', 0, 'songAttr')
    rep('author')
    rep('bvid')
    add('cid', 0)
    rep('coin_num', 0)
    rep('coinceiling', 0)
    add('collectIds', [])
    rep('cover', k2='cover_url')
    add('crtype', 0)
    rep('ctime', 0)
    rep('ctime_str')
    add('curtime', 0)
    rep('duration', 0)
    rep('fans', 0)
    rep('id', 0)
    rep('intro')
    rep('isFromVideo', 0)
    rep('is_cacheable', False)
    rep('is_collect', 0)
    rep('is_off', 0)
    rep('limit', 0)
    rep('limitdesc')
    rep('lyric', k2='lyric_url')
    rep('memberList', [])
    rep('menusRespones', [])
    add('msid', 0)
    add('passtime', 0)
    rep('pgc_info')
    rep('qualities', [])
    rep('region')
    rep('relationData')
    rep('collect', 0, 'collect_count', l=['statistic'])
    rep('comment', 0, 'reply_count', l=['statistic'])
    rep('play', 0, 'play_count', l=['statistic'])
    rep('share', 0, 'snum', l=['statistic'])
    rep('sid', 0, 'id', l=['statistic'])
    rep('title')
    rep('uid', 0, 'mid')
    rep('uname', k2='up_name')
    rep('up_cert_info')
    rep('up_cert_type')
    rep('up_hit_audios', [])
    rep('up_img')
    rep('up_is_follow', 0)
    rep('videos', [])
    return d


def getaualbuminfo(d: dict) -> (bool, dict):
    "读取AU号信息中的专辑信息"
    r = {}
    if 'pgc_info' not in d or d['pgc_info'] is None or type(d['pgc_info']) != dict:
        return False, r
    pgc_info = d['pgc_info']
    if 'pgc_menu' not in pgc_info or pgc_info['pgc_menu'] is None or type(pgc_info['pgc_menu']) != dict:
        return False, r
    pgc_menu = pgc_info['pgc_menu']
    r['menuId'] = pgc_menu['menuId']
    r['type'] = pgc_menu['type']
    r['coverUrl'] = pgc_menu['coverUrl']
    r['title'] = pgc_menu['title']
    r['mbnames'] = pgc_menu['mbnames']
    r['publisher'] = pgc_menu['publisher']
    r['pubTime'] = pgc_menu['pubTime']
    if 'tags' in pgc_menu and pgc_menu['tags'] is not None and type(pgc_menu['tags']) == list:
        r['tags'] = [i['itemVal'] for i in pgc_menu['tags']]
    else:
        r['tags'] = []
    r['passTime'] = pgc_menu['passTime']
    r['playNum'] = pgc_menu['playNum']
    r['tryNum'] = pgc_menu['tryNum']
    r['downloadNum'] = pgc_menu['downloadNum']
    r['collNum'] = pgc_menu['collNum']
    r['isOff'] = pgc_menu['isOff']
    r['uid'] = pgc_menu['uid']
    r['uname'] = pgc_menu['uname']
    r['collectionId'] = pgc_menu['collectionId']
    if 'menusRespones' in pgc_info:
        r['menusRespones'] = pgc_info['menusRespones']
    if 'songsList' in pgc_info:
        r['songsList'] = pgc_info['songsList']
    return True, r


def getindexfromsongs(l: list, id: int) -> int:
    k = 1
    for song in l:
        if song['id'] == id:
            return k
        k = k + 1
    return 0


def getchl(d:dict)->list:
    r=[]
    for i in d['data']['list'] :
        t={}
        t['cid']=i['cid']
        t['name']=i['name']
        t['intro']=i['intro']
        t['mtime']=i['mtime']
        t['count']=i['count']
        r.append(t)
    return r
def getchi(r:Session, u: int, c: int, n: int, logg=None):
    if logg is not None:
        logg.write(f"GET https://api.bilibili.com/x/space/channel/video?mid={u}&cid={c}&pn={n}&ps=30&order=0&jsonp=jsonp", currentframe(), "GET CHANNLE VIDEO LIST")
    uri="https://api.bilibili.com/x/space/channel/video?mid=%s&cid=%s&pn=%s&ps=30&order=0&jsonp=jsonp"%(u,c,n)
    bs=True
    while bs :
        try :
            re=r.get(uri)
            bs=False
        except :
            if logg is not None:
                logg.write(format_exc(), currentframe(), "GET CHANNLE VIDEO LIST ERROR")
            print(lan['OUTPUT2'].replace('<number>',str(n)))#获取频道第%s页失败，正在重试……
    re.encoding='utf8'
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET CHANNLE VIDEO LIST RESULT")
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    return re
def getchn(d:dict)->dict:
    i=d['data']['list']
    r={}
    r['cid']=i['cid']
    r['name']=i['name']
    r['intro']=i['intro']
    r['mtime']=i['mtime']
    r['count']=i['count']
    return r
def getchs(l:list,d:dict):
    for t in d['data']['list']['archives'] :
        r={}
        r['aid']=t['aid']
        r['videos']=t['videos']
        r['title']=t['title']
        r['pubdate']=t['pubdate']
        r['ctime']=t['ctime']
        r['desc']=t['desc']
        r['cid']=t['cid']
        r['bvid']=t['bvid']
        l.append(r)
def getsub(d:dict,z:dict):
    t=d['subtitles']
    if len(t)>0 :
        r=[]
        for i in t:
            e={}
            e['lan']=i['lan']
            e['land']=i['lan_doc']
            e['url']="https:%s"%(i['subtitle_url'])
            r.append(e)
        z['sub']=r
def getuvi(u: int, n: int, d: dict, r: Session, logg=None):
    if logg is not None:
        logg.write(f"GET https://api.bilibili.com/x/space/arc/search?mid={u}&ps=30&tid={d['t']}&pn={n}&keyword={d['k']}&order={d['o']}&jsonp=jsonp", currentframe(), "GET UPLOAD VIDEO LIST")
    uri="https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=%s&pn=%s&keyword=%s&order=%s&jsonp=jsonp"%(u,d['t'],n,d['k'],d['o'])
    bs=True
    while bs:
        try :
            re=r.get(uri)
            bs=False
        except :
            if logg is not None:
                logg.write(format_exc(), currentframe(), "GET UPLOAD VIDEO LIST FAILED")
            print(lan['OUTPUT3'].replace('<number>',str(n)))#获取第%s页失败，正在重试……
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET UPLOADER VIDEO LIST RESULT")
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    return re
def getuvl(d:dict,l:list):
    for t in d['data']['list']['vlist']:
        r={}
        r['aid']=t['aid']
        r['bvid']=t['bvid']
        r['title']=t['title']
        r['description']=t['description']
        r['ctime']=t['created']
        l.append(r)
def getup(u: int, r: Session, logg=None):
    if logg is not None:
        logg.write(f"GET https://api.bilibili.com/x/space/acc/info?mid={u}&jsonp=jsonp", currentframe(), "GET UPLOADER INFO")
    uri="https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp"%(u)
    bs=True
    while bs:
        try :
            re=r.get(uri)
            bs=False
        except :
            if logg is not None:
                logg.write(format_exc(), currentframe(), "GET UPLOADER INFO ERROR")
            print(lan['OUTPUT4'])#获取UP主信息失败，正在重试……
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET UPLOADER INFO RESULT")
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    return re
def getupi(d:dict)->dict :
    r={}
    q=d['data']
    r['n']=q['name']
    r['s']=q['sex']
    r['l']=q['level']
    r['sign']=q['sign']
    r['b']=q['birthday']
    return r
def getsmi(d:dict)->dict :
    "获取小视频信息"
    r={}
    if 'data' in d :
        if 'item' in d['data'] :
            x=d['data']['item']
            r['backup_playurl']=x['backup_playurl']
            r['description']=x['description']
            r['id']=x['id']
            r['height']=x['height']
            r['reply']=x['reply']
            r['tags']=x['tags']
            r['upload_time']=x['upload_time']
            r['video_playurl']=x['video_playurl']
            r['video_time']=x['video_time']
            r['width']=x['width']
        if 'user' in d['data'] :
            x=d['data']['user']
            r['name']=x['name']
            r['uid']=x['uid']
    return r
def getlr1(d:dict) -> dict :
    "获取直播回放信息"
    r={}
    t=d['data']
    r['dm']=t['dm_info']
    t=t['live_record_info']
    r['rid']=t['rid']
    r['roomid']=t['room_id']
    r['uid']=t['uid']
    r['title']=t['title']
    r['areaid']=t['area_id']
    r['pareaid']=t['parent_area_id']
    r['st']=t['start_timestamp']
    r['et']=t['end_timestamp']
    r['online']=t['online']
    r['danmunum']=t['danmu_num']
    return r
def getlr2(d:dict,r:dict) :
    "获得房间信息（可能与当前回放信息不同）"
    t=d['data']
    r['des']=t['description']
    r['arean']=t['area_name']
    r['parean']=t['parent_area_name']
    r['tags']=t['tags']
    r['hotwords']=t['hot_words']
def getlr3(d:dict,r:dict):
    "获得UP主信息"
    t=d['data']
    r['name']=t['name']
    r['sex']=t['sex']
    r['sign']=t['sign']
def getchel(r:Session, logg=None) -> list:
    """获得已购课程列表
    -1 获取出错"""
    if logg is not None:
        logg.write("GET https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn=1", currentframe(),"GET PAID COURSES LIST 1")
    re=r.get("https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn=1")
    re.encoding='utf8'
    if logg is not None:
        logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET PAID COURSES LIST 1 RESULT")
    re=re.json()
    if re['code']!=0:
        print(f"{re['code']} {re['message']}")
        return -1
    re=re['data']
    n=re['total']
    l:list=re['data']
    i=2
    while i<=n :
        bs=True
        while bs:
            try :
                if logg is not None:
                    logg.write(f"GET https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn={i}", currentframe(), "GET PAID COURSES LIST")
                re=r.get(f"https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn={i}")
                bs=False
            except :
                if logg is not None:
                    logg.write(format_exc(), currentframe(), "GET PAID COURSES LIST FAILED")
                print(lan['OUTPUT3'].replace('<number>',str(i)))#获取第%s页失败，正在重试……
            re.encoding='utf8'
            if logg is not None:
                logg.write(f"status = {re.status_code}\n{re.text}", currentframe(), "GET PAID COURSES LIST RESULT")
            re=re.json()
            if re['code']!=0:
                print(f"{re['code']} {re['message']}")
                return -1
            for j in re['data']['data'] :
                l.append(j)
        i=i+1
    return l
def getliveinfo1(d:dict) -> dict:
    r = {}
    r['roomid'] = d['room_id']
    r['uid'] = d['uid']
    r['online'] = d['online']
    r['des'] = d['description']
    r['title'] = d['title']
    r['areaid'] = d['area_id']
    r['areaname'] = d['area_name']
    r['pareaid'] = d['parent_area_id']
    r['pareaname'] = d['parent_area_name']
    r['livestatus'] = d['live_status']
    r['livetime'] = d['live_time']
    r['tags'] = d['tags']
    r['hotwords'] = d['hot_words']
    return r
def getliveinfo2(d: dict, r: dict):
    r['name'] = d['name']
    r['sex'] = d['sex']
    r['sign'] = d['sign']
