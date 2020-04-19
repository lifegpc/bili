from json import loads,dumps
from os.path import exists
from os import remove
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
def getcookie() :
    '读取cookies并获得cookies字符串'
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
    s='cookie: '
    k=0
    for i in o :
        if i['domain']=='.bilibili.com' :
            if k==0 :
                s=s+i['name']+'='+i['value']
            else :
                s=s+'; '+i['name']+'='+i['value']
            k=k+1
    return s
