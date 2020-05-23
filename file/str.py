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
from unicodedata import east_asian_width
def width(s) :
    '获取字符串宽度'
    t=0
    for i in s :
        if east_asian_width(i) in ('F','W','A') :
            t=t+2
        else :
            t=t+1
    return t
dw=['B','K','M','G','T','P','E','Z','Y']
def size(i) :
    '将字节数转为可读性较好的数'
    if i=='N/A' :
        return 'N/A'
    t=float(i)
    b=0
    while t > 10*2**10 and b<8 :
        b=b+1
        t=t/2**10
    global dw
    return "%.2f%s" %(t,dw[b])
def ftts(i) :
    '转换'
    if i=='d' :
        return '目录'
    elif i=='f' :
        return '文件'
def cml(s,t):
    '计算码率,s 大小B,t 时间ms'
    s=s*8/t
    return "%.2fkbps"%(s)
