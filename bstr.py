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
from re import search,I
from html.parser import HTMLParser
from regex import search as rsearch
def f(i:str):
    s=i.replace('\r','\\r')
    s=s.replace('\n','\\n')
    s=s.replace('"',"'")
    return s


def g(i: str):
    s = str(i)
    re = rsearch(r'[^[:print:]\r\n]', s)
    while re is not None:
        s = s.replace(re.group(), '_')
        re = rsearch(r'[^[:print:]\r\n]', s)
    s = s.replace('#', '\\#')
    s = s.replace('\\', '\\\\')
    s = s.replace('=', '\\=')
    s = s.replace(';', '\\;')
    s = s.replace('\r', '')
    s = s.replace('\n', '\\\n')
    return s


def gettags(t:list) -> str:
    "将tag列表转换为文字"
    f=True
    s=""
    for i in t :
        if f:
            f=False
            s=i
        else :
            s=s+","+i
    return s
def rhtml(s:str)-> str:
    "去HTML化"
    r=s.replace('\n','')
    r=r.replace('<br>','\n')
    r=r.replace('<br/>','\n')
    r=r.replace('</p>','\n')
    t=search(r'<[^>]+>',r,I)
    while t!=None:
        t=t.span()
        if t[0]==0 :
            r=r[t[1]:]
        elif t[1]==len(s) :
            r=r[:t[0]]
        else :
            r=r[:t[0]]+r[t[1]:]
        t=search(r'<[^>]+>',r,I)
    r=HTMLParser().unescape(r)
    return r
def getv(l:list) -> (list,list) :
    """将合并在一起的画质id和画质描述分开
    返回值为id,画质描述"""
    q=[]
    d=[]
    for i in l:
        q.append(i['qn'])
        d.append(i['desc'])
    return q,d
