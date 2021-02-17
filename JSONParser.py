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
from json import loads,dumps
from os.path import exists
from os import remove
from requests import Session
from biliBv import enbv
import sys
from biliTime import tostr2
from traceback import format_exc
from inspect import currentframe


def Myparser(s) :
    "解析普通AV视频信息"
    obj=loads(s)
    if 'ssList' in obj:
        return -1
    data={}
    data['aid']=obj['aid']
    data['bvid']=obj['videoData']['bvid']
    data['videos']=obj['videoData']['videos']
    data['title']=obj['videoData']['title']
    data['pubdate']=obj['videoData']['pubdate']
    data['ctime']=obj['videoData']['ctime']
    data['desc']=obj['videoData']['desc']
    data['uid']=obj['videoData']['owner']['mid']
    data['name']=obj['videoData']['owner']['name']
    data['pic']=obj['videoData']['pic']
    page=[]
    for i in obj['videoData']['pages'] :
        t={}
        t['cid']=i['cid']
        t['page']=i['page']
        t['part']=i['part']
        t['duration'] = i['duration']
        page.append(t)
    data['page']=page
    tags = []
    if 'tags' in obj and obj['tags'] is not None:
        for i in obj['tags']:
            tags.append(i['tag_name'])
    data['tags'] = tags
    return data
def Myparser2(s) :
    "解析SS视频信息"
    obj=loads(s)
    data={}
    if 'mediaInfo' in obj :
        mediaInfo={}
        mediaInfo['id']=obj['mediaInfo']['id']
        mediaInfo['ssId']=obj['mediaInfo']['ssId']
        mediaInfo['title']=obj['mediaInfo']['title']
        mediaInfo['jpTitle']=obj['mediaInfo']['jpTitle']
        mediaInfo['series']=obj['mediaInfo']['series']
        mediaInfo['alias']=obj['mediaInfo']['alias']
        mediaInfo['evaluate']=obj['mediaInfo']['evaluate']
        mediaInfo['type']=obj['mediaInfo']['ssTypeFormat']['name']
        mediaInfo['time']=obj['mediaInfo']['pub']['time']
        t=obj['mediaInfo']['cover']
        if t.startswith('//'):
            t="https:"+t
        mediaInfo['cover']=t
        data['mediaInfo']=mediaInfo
    if 'epList' in obj :
        epList=[]
        for i in obj['epList'] :
            t={}
            t['id']=i['id']
            t['aid']=i['aid']
            t['bvid']=i['bvid']
            t['cid']=i['cid']
            t['titleFormat']=i['titleFormat']
            t['longTitle']=i['longTitle']
            t['i']=i['i']
            t['loaded']=i['loaded']
            t['sectionType'] = i['sectionType']
            p=i['cover']
            if str(p).startswith('//'):
                p="https:"+p
            t['cover']=p
            epList.append(t)
        data['epList']=epList
    if 'sections' in obj :
        sections=[]
        for i in obj['sections'] :
            t={}
            t['id']=i['id']
            t['title']=i['title']
            t['type'] = i['type']
            if 'epList' in i :
                epList=[]
                for j in i['epList'] :
                    t2={}
                    t2['id']=j['id']
                    t2['aid']=j['aid']
                    t2['bvid']=j['bvid']
                    t2['cid']=j['cid']
                    t2['titleFormat']=j['titleFormat']
                    t2['longTitle']=j['longTitle']
                    t2['i']=j['i']
                    t2['loaded']=j['loaded']
                    t2['title']=i['title']
                    t2['sectionType'] = j['sectionType']
                    p=j['cover']
                    if str(p).startswith('//'):
                        p="https:"+p
                    t2['cover']=p
                    epList.append(t2)
                t['epList']=epList
            sections.append(t)
        data['sections']=sections
    return data
def savecookie(data) :
    '存储cookies信息'
    jsObj=dumps(data)
    obj=open('cookies.json',mode='w')
    obj.write(jsObj)
    obj.close()
def loadcookie(r, logg = None):
    '读取cookie信息'
    try :
        obj=open('cookies.json',mode='r')
    except :
        if logg is not None:
            logg.write(format_exc(), currentframe(), "READ cookies.json FAILED 1")
        return -1
    try :
        obj.seek(0,2)
        si=obj.tell()
        obj.seek(0,0)
        s=obj.read(si)
        o=loads(s)
    except :
        if logg is not None:
            logg.write(format_exc(), currentframe(), "READ cookies.json FAILED 2")
        return -2
    for i in o :
        r.cookies.set(i['name'],i['value'],domain=i['domain'],path=i['path'])
    return 0
def loadset():
    "加载settings.json设置"
    try :
        obj=open('settings.json',mode='r')
    except :
        return -1
    try :
        obj.seek(0,2)
        si=obj.tell()
        obj.seek(0,0)
        s=obj.read(si)
        o=loads(s)
    except :
        return -2
    return o


def getDefalutSettings():
    "获取默认设置"
    t = {}
    t['a'] = True
    t['ab'] = True
    t['sv'] = True
    t['te'] = True
    t['lrh'] = True
    t['in'] = True
    t['log'] = True
    t['ma'] = True
    t['auf'] = True
    t['ol'] = True
    t['cc'] = True
    return t


def saveset(d):
    "保存settings.json设置"
    try :
        if exists('settings.json') :
            remove('settings.json')
        obj=open('settings.json',mode='w')
    except :
        return -1
    try :
        obj.write(dumps(d))
        obj.close()
    except :
        return -2
    return 0
def getset(d:dict,key:str) :
    '获取当前key的设置，如不存在返回None'
    if d==None :
        return None
    if key in d :
        return d[key]
    else :
        return None
def parseche(d:dict) :
    "解析下载课程"
    r={}
    r['che']=True #标识为下载课程
    t=d['data']
    m={}
    m['id']=t['season_id']
    m['ssId']=t['season_id']
    m['title']=t['title']
    m['jpTitle']=''
    m['series']=t['title']
    m['alias']=''
    m['evaluate']=t['subtitle']
    m['type']=''
    m['cover']=t['cover']
    m['up_info'] = t['up_info']
    e=[]
    b=sys.maxsize #最早的时间
    for i in t['episodes'] :
        a={}
        a['id']=i['id']
        a['aid']=i['aid']
        a['bvid']=enbv(int(i['aid']))
        a['cid']=i['cid']
        a['titleFormat']=f"P{i['index']}"
        a['longTitle']=i['title']
        a['i']=i['index']-1
        a['time']=i['release_date']
        a['sectionType'] = 0
        if a['time']<b:
            b=a['time']
        e.append(a)
    m['time']=tostr2(b)
    r['mediaInfo']=m
    r['epList']=e
    if 'brief' in t:
        c=[]
        for i in t['brief']['img'] :
            c.append(i['url'])
        r['brief']=c
    if 'user_status' in t and 'progress' in t['user_status'] :
        r['led']=t['user_status']['progress']['last_ep_id']
    return r
