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
from requests.structures import CaseInsensitiveDict
def copydict(x) :
    if isinstance(x,dict):
        r={}
    elif isinstance(x,CaseInsensitiveDict) :
        r=CaseInsensitiveDict()
    else :
        return {}
    for i in x.keys() :
        t=x[i]
        if isinstance(t,(dict,CaseInsensitiveDict)) :
            r[i]=copydict(t)
        elif isinstance(t,list) :
            r[i]=copylist(t)
        else :
            r[i]=t
    return r
def copylist(x) :
    r=[]
    for i in x :
        if isinstance(i,(dict,CaseInsensitiveDict)) :
            r.append(copydict(i))
        elif isinstance(i,list) :
            r.append(copylist(i))
        else :
            r.append(i)
    return r
def copyip(x:dict):
    "复制时不保留i,p"
    r={}
    for i in x.keys() :
        if i!='i' and i!='p' :
            t=x[i]
            if isinstance(t,(dict,CaseInsensitiveDict)) :
                r[i]=copydict(t)
            elif isinstance(t,list) :
                r[i]=copylist(t)
            else :
                r[i]=t
    return r
