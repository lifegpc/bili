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
    if logg is not None:
        logg.write(f"GET https://api.bilibili.com/x/v3/fav/resource/list?media_id={f}&pn={i}&ps=20&keyword={d['k']}&order=mtime&type={d['t']}&tid=0&jsonp=jsonp", currentframe(), "GET PLI INFO")
    uri='https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=%s&ps=20&keyword=%s&order=mtime&type=%s&tid=0&jsonp=jsonp'%(f,i,d['k'],d['t'])
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
def getuvi(u:int,n:int,d:dict,r:Session):
    uri="https://api.bilibili.com/x/space/arc/search?mid=%s&ps=30&tid=%s&pn=%s&keyword=%s&order=%s&jsonp=jsonp"%(u,d['t'],n,d['k'],d['o'])
    bs=True
    while bs:
        try :
            re=r.get(uri)
            bs=False
        except :
            print(lan['OUTPUT3'].replace('<number>',str(n)))#获取第%s页失败，正在重试……
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
def getup(u:int,r:Session) :
    uri="https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp"%(u)
    bs=True
    while bs:
        try :
            re=r.get(uri)
            bs=False
        except :
            print(lan['OUTPUT4'])#获取UP主信息失败，正在重试……
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
def getchel(r:Session) -> list:
    """获得已购课程列表
    -1 获取出错"""
    re=r.get("https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn=1")
    re.encoding='utf8'
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
                re=r.get(f"https://api.bilibili.com/pugv/pay/web/my/paid?ps=10&pn={i}")
                bs=False
            except :
                print(lan['OUTPUT3'].replace('<number>',str(i)))#获取第%s页失败，正在重试……
            re.encoding='utf8'
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
