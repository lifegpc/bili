# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from json import loads,dumps
from os.path import exists
from os import remove
from requests import Session
def Myparser(s) :
    "解析普通AV视频信息"
    obj=loads(s)
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
    page=[]
    for i in obj['videoData']['pages'] :
    	t={}
    	t['cid']=i['cid']
    	t['page']=i['page']
    	t['part']=i['part']
    	page.append(t)
    data['page']=page
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
            epList.append(t)
        data['epList']=epList
    if 'sections' in obj :
        sections=[]
        for i in obj['sections'] :
            t={}
            t['id']=i['id']
            t['title']=i['title']
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
def loadcookie(r) :
    '读取cookie信息'
    try :
        obj=open('cookies.json',mode='r')
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
def getpli(r,f,i):
    uri='https://api.bilibili.com/x/v3/fav/resource/list?media_id=%s&pn=%s&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'%(f,i)
    bs=True
    while bs :
        try :
            re=r.get(uri)
            bs=False
        except :
            print('获取收藏夹第%s页失败，正在重试……'%(i))
    re.encoding='utf8'
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
def getchi(r:Session,u:int,c:int,n:int):
    uri="https://api.bilibili.com/x/space/channel/video?mid=%s&cid=%s&pn=%s&ps=30&order=0&jsonp=jsonp"%(u,c,n)
    bs=True
    while bs :
        try :
            re=r.get(uri)
            bs=False
        except :
            print('获取频道第%s页失败，正在重试……'%(n))
    re.encoding='utf8'
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
            print('获取第%s页失败，正在重试……'%(n))
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
            print('获取uid为%s的UP主信息失败，正在重试……'%(u))
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
