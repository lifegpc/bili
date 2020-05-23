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
from requests import Session
def getninfo(r:Session,d:dict):
    re=r.get("https://api.bilibili.com/x/stein/edgeinfo_v2?bvid=%s&graph_version=%s&platform=pc&portal=0&screen=0&buvid=%s"%(d['bvid'],d['gv'],r.cookies.get('buvid3')))
    re.encoding='utf8'
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    q=[]
    if 'questions' in re['data']['edges']:
        q=re['data']['edges']['questions']
    e=[]
    addninfo(re,e)
    for a in q:
        for b in a['choices'] :
            read=getnch(r,b,d,e)
            if read==-1 :
                return -1
    d['page']=e
def getnch(r:Session,b:dict,d:dict,e:list) :
    re=r.get("https://api.bilibili.com/x/stein/edgeinfo_v2?bvid=%s&edge_id=%s&graph_version=%s&platform=pc&portal=0&screen=0&buvid=%s&choice=%s"%(d['bvid'],b['id'],d['gv'],r.cookies.get('buvid3'),b['native_action']))
    re.encoding='utf8'
    re=re.json()
    if re['code']!=0 :
        print('%s %s'%(re['code'],re['message']))
        return -1
    q=[]
    if 'questions' in re['data']['edges']:
        q=re['data']['edges']['questions']
    addninfo(re,e)
    for a in q:
        for b in a['choices'] :
            read=getnch(r,b,d,e)
            if read==-1 :
                return -1
def addninfo(d:dict,l:list):
    d=d['data']
    e={}
    e['page']=len(l)+1
    e['part']=d['title']
    i=d['edge_id']
    for k in d['story_list'] :
        if k['edge_id']==i :
            e['cid']=k['cid']
            if infoqc(e['cid'],l) : #发现重复，跳过
                return
            l.append(e)
            break
def infoqc(c:int,l:list):
    "对互动视频列表进行去重"
    for i in l:
        if i['cid']==c :
            return True
    return False
