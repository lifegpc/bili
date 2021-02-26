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
from JSONParser import loadset, saveset, getset
from re import search
from PrintInfo import pr
from file import filterd
from lang import lan, getlan, getdict
import sys
from command import gopt
la = None
se = loadset()
if se == -1 or se == -2:
    se = {}
ip = {}
if len(sys.argv) > 1:
    ip = gopt(sys.argv[1:])
la = getdict('setsettings', getlan(se, ip))
l1 = ['x', '', '']
l2 = ['', 'x', '']
l3 = ['', '', 'x']


def print2(s: str, l: list):  # noqa: E741
    t = search('%s', s)
    u = len(l)
    i = 0
    while t:
        s = s.replace('%s', str(l[i]), 1)
        t = search('%s', s)
        i = i + 1
        if i == u:
            i = 0
    print(s)


def gk(se: dict, key: str):
    if not se:
        return l3
    else:
        no = getset(se, key)
        if no is None:
            return l3
        elif no:
            return l1
        else:
            return l2


def sk(se: dict, key: str, re: dict):
    b = True
    while b:
        i = input(la['INPUT1'])  # 请输入选项中的数字以选择
        if len(i) > 0 and i.isnumeric():
            i = int(i)
            if i == 1:
                b = False
                se[key] = True
            elif i == 2:
                b = False
                se[key] = False
            elif i == 3:
                b = False
        else:
            b = False
            if re and key in re:
                se[key] = re[key]


if __name__ == '__main__':
    pr()
    ne = {}
    se = loadset()
    if not isinstance(se, dict):
        se = {}
    r = []
    print(la['OUTPUT1'])  # 选项前的x指明了当前选中的设置，直接回车会保持当前设置
    if se:
        print(la['OUTPUT2'])  # 删除当前文件夹下的setting.json可以重置设置
    n = la['NOTSET']  # 不设置
    p = ""
    if se and 'lan' in se:
        p = se['lan']
        n = lan[p]
    print(la['OUTPUT3'].replace('<languagename>', n))  # 请选择程序语言（目前为<languagename>）：
    print(f'null : {la["NOTSET"]}')
    for i in lan.keys():
        print(f'{i} : {lan[i]}')
    r = input(la['INPUT2'])  # 请输入:之前的语言代码：
    if len(r) > 0 and (r in lan or r == "null"):
        p = r
        if p != "null":
            ne['lan'] = p
            la = getdict('setsettings', p)
        else:
            la = getdict('setsettings', getlan({}, {}))
    print(la['INPUT3'])  # 是否默认启用弹幕过滤？
    r = gk(se, 'dmgl')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'dmgl', se)
    print(la['INPUT4'])  # 是否要默认下载最高画质（这样将不会询问具体画质）？
    r = gk(se, 'mp')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'mp', se)
    print(la['INPUT5'])  # 在合并完成后是否删除无用文件？
    r = gk(se, 'ad')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'ad', se)
    print(la['INPUT6'])  # 是否开启继续下载功能？
    r = gk(se, 'cd')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'cd', se)
    print(la['INPUT7'])  # 是否开启下载失败后自动重新下载？
    r = gk(se, 'rd')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'rd', se)
    print(f"{la['INPUT8']}{la['NTN']}")  # 是否不使用ffmpeg合并？ （不设置相当于否）
    r = gk(se, 'nf')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'nf', se)
    print(la['INPUT9'])  # 默认下载最高画质时偏好的视频编码：
    r = gk(se, 'mpc')
    print2(f'%s1.avc(h.264)\t%s2.hevc(h.265)\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'mpc', se)
    print(f"{la['INPUT10']}{la['NTY']}")  # 是否使用aria2c下载？（不设置相当于是）
    r = gk(se, 'a')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'a', se)
    n = 3
    if se and 'ax' in se:
        n = se['ax']
    print(la['INPUT11'].replace('<value3>', str(n)).replace('<value1>', '1-16').replace('<value2>', '3'))  # 使用aria2c时单个服务器最大连接数(有效值：<value1>，默认：<value2>，目前：<value3>)： 1-16 3
    inp = input(la['INPUT12'].replace('<min>', '1').replace('<max>', '16'))  # 请输入<min>-<max>中的数字： 1 16
    if len(inp) > 0:
        if inp.isnumeric():
            i = int(inp)
            if i >= 1 and i <= 16 and i != 3:
                ne['ax'] = i
    elif n != 3:
        ne['ax'] = n
    n = 5
    if se and 'as' in se:
        n = se['as']
    print(la['INPUT13'].replace('<value3>', str(n)).replace('<value1>', '1-*').replace('<value2>', '5'))  # 使用aria2c时单个文件最大连接数(1-*，默认5，目前为%s)：
    inp = input(la['INPUT14'].replace('<min>', '1'))  # 请输入大于等于<min>的数字： 1
    if len(inp) > 0:
        if inp.isnumeric():
            i = int(inp)
            if i >= 1 and i != 5:
                ne['as'] = i
    elif n != 5:
        ne['as'] = n
    n = 5
    if se and 'ak' in se:
        n = se['ak']
    print(la['INPUT15'].replace('<value4>', str(n)).replace('<value1>', 'M').replace('<value2>', '1-1024').replace('<value3>', '5'))  # aria2c文件分片大小(单位M，1-1024，默认5，目前为%s)：
    inp = input(la['INPUT12'].replace('<min>', '1').replace('<max>', '1024'))  # 请输入1-1024的数字：
    if len(inp) > 0:
        if inp.isnumeric():
            i = int(inp)
            if i >= 1 and i <= 1024 and i != 5:
                ne['ak'] = i
    elif n != 5:
        ne['ak'] = n
    print(f"{la['INPUT16']}{la['NTY']}")  # 在使用aria2c下载时是否使用备用网址？（不设置情况下为是）
    r = gk(se, 'ab')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'ab', se)
    n = 'prealloc'
    if se and 'fa' in se:
        n = se['fa']
    print(la['INPUT17'].replace('<value2>', n).replace('<value1>', 'prealloc'))  # 在使用arai2c下载时预分配方式即--file-allocation的参数(默认为prealloc，目前为%s)
    print('1.none\t2.prealloc\t3.trunc\t4.falloc')
    inp = input(la['INPUT1'])  # 请输入选项中的数字以选择
    if len(inp) > 0 and inp.isnumeric():
        i = int(inp)
        x = ['none', 'prealloc', 'trunc', 'falloc']
        if i > 0 and i < 5 and i != 2:
            ne['fa'] = x[i - 1]
    elif n != "prealloc":
        ne['fa'] = n
    print(f"{la['INPUT18']}{la['NTY']}")  # 文件名中是否输出视频画质信息？（不设置情况下为是）
    r = gk(se, 'sv')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'sv', se)
    print(f"{la['INPUT19']}{la['NTY']}")  # 是否强制增加视频元数据（这会导致原本不需要转码的视频被转码，转码不会影响画质）？（不设置情况下为是）
    r = gk(se, 'ma')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'ma', se)
    n = "0"
    if se and 'ms' in se:
        n = se['ms']
    inp = input(la['INPUT20'].replace('<value2>', n).replace('<value1>', '0'))  # 在使用aria2c时最大总体速度(B/s)（0代表无限制，可以使用K和M为单位（1K=1024，1M=1024K），默认：，目前为%s）：
    if len(inp) > 0:
        t = search("^[0-9]+[MK]?$", inp)
        if t is not None:
            if inp != "0":
                ne['ms'] = inp
    elif n != "0":
        ne['ms'] = n
    print(la['INPUT21'])  # 收藏夹/频道/投稿是否自动下载每一个视频的所有分P？
    r = gk(se, 'da')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'da', se)
    print(f"{la['INPUT22']}{la['NTN']}")  # 下载全弹幕时两次抓取之间的天数默认设置为自动？（不设置情况下为否）
    r = gk(se, 'jt')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'jt', se)
    o = "Download/"
    if se and 'o' in se:
        o = se['o']
    inp = input(la['INPUT23'].replace('<value2>', o).replace('<value1>', 'Download/'))  # 下载文件夹位置（默认为Download/，当前为%s）：
    if len(inp) > 0:
        if inp != 'Download/':
            ne['o'] = filterd(inp)
    elif o != 'Download/':
        ne['o'] = o
    print(f"{la['INPUT24']}{la['NTN']}")  # 解析收藏夹时若未指定收藏夹，是否不自动解析为默认收藏夹而是返回列表以选择？（不设置情况下为否）
    r = gk(se, 'af')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'af', se)
    print(f"{la['INPUT25']}{la['NTN']}")  # 下载小视频时，放入文件名中的描述长度是否可以超过20字？（不设置情况下为否）
    r = gk(se, 'slt')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'slt', se)
    print(f"{la['INPUT26']}{la['NTY']}")  # requests是否使用环境变量中的代理设置？（不设置情况下为是）
    r = gk(se, 'te')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'te', se)
    print(f"{la['INPUT27']}{la['NTN']}")  # 合并完成后删除文件时是否保留字幕文件？（不设置情况下为否）
    r = gk(se, 'bd')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'bd', se)
    print(f"{la['INPUT28']}{la['NTN']}")  # 使用aria2c时是否关闭异步DNS（关闭后在Windows系统下可以解决Timeout while contacting DNS servers问题）？（不设置情况下为否）
    r = gk(se, 'cad')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'cad', se)
    print(f"{la['INPUT29']}{la['NTY']}")  # 直播回放简介写入元数据时是否进行去HTML化？（不设置情况下为是）
    r = gk(se, 'lrh')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'lrh', se)
    print(f"{la['INPUT30']}{la['NTN']}")  # 合并完成后删除无用文件时是否保留封面图片？（不设置情况下为否）
    r = gk(se, 'bp')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'bp', se)
    print(f"{la['INPUT31']}{la['NTY']}")  # 是否将AV/BV号等放入文件名？（不设置情况下为是）
    r = gk(se, 'in')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'in', se)
    print(f"{la['INPUT32']}{la['NTN']}")  # 是否在有多个输入的时候启用多线程（这会是输出变得一团糟）？（不设置情况下为否）
    r = gk(se, 'mt')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'mt', se)
    print(f"{la['INPUT33']}{la['NTN']}")  # 是否要禁用检查新版本？（不设置情况下为否）
    r = gk(se, 'uc')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'uc', se)
    print(f"{la['INPUT34']}{la['NTN']}")  # 是否要将字幕文件保存为ASS(Advanced SubStation Alpha)文件？（不设置情况下为否）
    r = gk(se, 'ass')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'ass', se)
    print(f"{la['INPUT35']}{la['NTN']}")  # 是否要为多P视频创建单独的文件夹？（不设置情况下为否）
    r = gk(se, 'dmp')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'dmp', se)
    print(f"{la['INPUT36']}")
    r = gk(se, 'y')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'y', se)
    vf = 'mkv'
    if 'vf' in se:
        vf = se['vf']
    print(la['INPUT37'].replace('<value>', 'mkv').replace('<value2>', vf))
    print(f"1.{la['DE'][1:-1]}\t2.mkv\t3.mp4")
    b = True
    while b:
        inp = input(la['INPUT1'])
        if len(inp) > 0 and inp.isnumeric():
            i = int(inp)
            if i > 0 and i <= 3:
                b = False
                if i == 2:
                    ne['vf'] = 'mkv'
                elif i == 3:
                    ne['vf'] = 'mp4'
        else:
            b = False
            if 'vf' in se:
                ne['vf'] = se['vf']
    lmd = 10
    if 'lmd' in se:
        lmd = se['lmd']
    print(la['INPUT38'].replace('<value>', '10ms').replace('<value2>', f'{lmd}ms'))
    inp = input(la['INPUT14'].replace('<min>', '0'))
    bs = True
    while bs:
        if len(inp) == 0:
            bs = False
        elif inp.isnumeric():
            tem = int(inp)
            if tem >= 0:
                lmd = tem
                bs = False
        else:
            inp = input(la['INPUT14'].replace('<min>', '0'))
    if lmd != 10:
        ne['lmd'] = lmd
    print(f"{la['INPUT39']}{la['INPUT40']}{la['NTN']}")
    r = gk(se, 'nal')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'nal', se)
    print(f"{la['INPUT41']}{la['NTY']}")
    r = gk(se, 'log')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'log', se)
    print(f"{la['INPUT42']}{la['NTY']}")
    r = gk(se, 'auf')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'auf', se)
    print(f"{la['INPUT43']}{la['NTN']}")
    r = gk(se, 'dwa')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'dwa', se)
    print(f"{la['INPUT44']}{la['NTY']}")
    r = gk(se, 'ol')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'ol', se)
    print(f"{la['INPUT45']}{la['NTY']}")
    r = gk(se, 'cc')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'cc', se)
    print(f"{la['INPUT46']}{la['NTN']}")
    r = gk(se, 'nfo')
    print2(f'%s1.{la["YES"]}\t%s2.{la["NO"]}\t%s3.{la["NOTSET"]}{la["DE"]}', r)
    sk(ne, 'nfo', se)
    mxd = 40
    if 'mxd' in se:
        if se['mxd'] >= 0:
            mxd = se['mxd']
    print(la['INPUT47'].replace('<value>', '40').replace('<value2>', str(mxd)))
    inp = input(la['INPUT14'].replace('<min>', '0'))
    bs = True
    while bs:
        if len(inp) == 0:
            bs = False
        elif inp.isnumeric():
            tem = int(inp)
            if tem >= 0:
                mxd = tem
                bs = False
        else:
            inp = input(la['INPUT14'].replace('<min>', '0'))
    if mxd != 40:
        ne['mxd'] = mxd
    saveset(ne)
