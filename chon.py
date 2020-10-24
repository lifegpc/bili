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
def getcho(cho,data) :
    "将选中的数字转为相应信息"
    m=0
    if 'epList' in data :
        m=len(data['epList'])
    n=[]
    if 'sections' in data :
        for j in data['sections'] :
            n.append(len(j['epList']))
    re=[]
    for i in cho :
        if i <= m :
            #data['epList'][i-1]['i']=i
            data['epList'][i-1]['s']='e'
            re.append(data['epList'][i-1])
            continue
        r=m
        q=m
        for j in range(0,len(n)) :
            r=r+n[j]
            if i<=r :
                #data['sections'][j]['epList'][i-q-1]['i']=i
                data['sections'][j]['epList'][i-q-1]['s']='s'
                re.append(data['sections'][j]['epList'][i-q-1])
                break
            q=q+n[j]
    return re