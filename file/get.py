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
from file.dir import listd, getinfod, printinfod, listc
from file.filter import listf
from os.path import abspath, exists, isdir, isfile
from file import lan


def getfilen(l='Download', lx=['xml'], yl=15, g=1, save=False):  # noqa: E741
    """获取需要的文件名
    l 初始目录 lx 过滤类型 yl 每页个数 g 获取文件的数量 save 是否为保存文件
    -1 文件夹不存在
    -2 参数错误"""
    nml = abspath(l)
    if not exists(nml):
        return -1
    if g < 1 or yl < 1:
        return -2
    nl = listd(nml)
    nlf = listf(nl, 2, lx)
    nlfi = getinfod(nlf)
    zys = int(len(nlf) / yl) + 1
    ys = 1
    gg = True
    gl = 2
    ci = 0
    c = []
    bs = True
    while bs:
        if zys == 1:
            printinfod(nlfi)
        elif ys == zys:
            printinfod(listc(nlfi, (ys - 1) * yl, len(nlf)))
        else:
            printinfod(listc(nlfi, (ys - 1) * yl, ys * yl))
        if ys == zys:
            sl = (len(nlf) - 1) % yl + 1
        else:
            sl = yl
        print(lan['OUTPUT3'].replace('<num>', str(ys)).replace('<count>', str(zys)))  # 第<num>页，共<count>页
        if ys != 1:
            print(f"a.{lan['O1']}\t", end='')  # 上一页
        if ys != zys:
            print(f"b.{lan['O2']}\t", end='')  # 下一页
        print(f"c.{lan['O3']}\t", end='')  # 上一文件夹
        if gg and gl == 2:
            print(f"d.{lan['O4']}\t", end='')  # 不显示无后缀名文件
        elif gg and gl == 0:
            print(f"d.{lan['O5']}\t", end='')  # 显示无后缀名文件
        if gg:
            print(f"e.{lan['O6']}\t", end='')  # 显示所有文件
        else:
            print(f"e.{lan['O7']}\t", end='')  # 显示过滤后文件
        if save:
            print(f"f.{lan['O8']}\tg.{lan['O9']}")  # 输入文件名
        else:
            print(f"f.{lan['O8']}")  # 输入文件夹名称
        bs2 = True
        while bs2:
            inp = input(lan['OUTPUT4'])  # 请输入文件名之前的序号选中文件，或输入文件夹名之前的序号进入文件夹，或输入操作之前的字母进行该操作
            if len(inp) > 0:
                if inp[0] == 'a' and ys != 1:
                    ys = ys - 1
                    bs2 = False
                elif inp[0] == 'b' and ys != zys:
                    ys = ys + 1
                    bs2 = False
                elif inp[0] == 'c':
                    tmp = abspath("%s/../" % (nml))
                    if exists(tmp):
                        nml = tmp
                        nl = listd(nml)
                        if gg:
                            nlf = listf(nl, gl, lx)
                        else:
                            nlf = nl
                        nlfi = getinfod(nlf)
                        zys = int(len(nlf) / yl) + 1
                        ys = 1
                        bs2 = False
                    else:
                        print(lan['ERROR1'])  # 上一层文件夹不存在。
                elif inp[0] == 'd' and gg:
                    if gl == 2:
                        gl = 0
                    elif gl == 0:
                        gl = 2
                    nlf = listf(nl, gl, lx)
                    nlfi = getinfod(nlf)
                    zys = int(len(nlf) / yl) + 1
                    ys = 1
                    bs2 = False
                elif inp[0] == 'e':
                    if gg:
                        gg = False
                    else:
                        gg = True
                    if gg:
                        nlf = listf(nl, gl, lx)
                    else:
                        nlf = nl
                    nlfi = getinfod(nlf)
                    zys = int(len(nlf) / yl) + 1
                    ys = 1
                    bs2 = False
                elif inp[0] == 'f':
                    inp2 = input(lan['INPUT1'])  # 请输入文件夹位置（支持绝对和相对位置）：
                    tmp = abspath(inp2)
                    if exists(tmp):
                        nml = tmp
                        nl = listd(nml)
                        if gg:
                            nlf = listf(nl, gl, lx)
                        else:
                            nlf = nl
                        nlfi = getinfod(nlf)
                        zys = int(len(nlf) / yl) + 1
                        ys = 1
                        bs2 = False
                    else:
                        print(lan['ERROR2'])  # 该文件夹不存在
                elif inp[0] == 'g' and save:
                    inp2 = input(lan['INPUT2'])  # 请输入文件名称：
                    tmp = {'a': abspath('%s/%s' % (nml, inp2)), 'f': inp2}
                    if ci > 0 and checkcf(c, tmp):
                        print(lan['ERROR3'])  # 之前已选择此文件。
                    else:
                        if exists(tmp['a']):
                            if isfile(tmp['a']):
                                bs3 = True
                                while bs3:
                                    inp3 = input(f"{lan['INPUT3']}(y/n)")  # 该文件已存在，是否覆盖？
                                    if len(inp3) > 0:
                                        if inp3[0].lower() == 'y':
                                            c.append(tmp)
                                            ci = ci + 1
                                            bs3 = False
                                            bs2 = False
                                        elif inp3[0].lower() == 'n':
                                            bs3 = False
                        else:
                            c.append(tmp)
                            ci = ci + 1
                            bs2 = False
                elif inp.isnumeric():
                    if int(inp) > 0 and int(inp) <= sl:
                        tmp = nlf[(ys - 1) * yl + int(inp) - 1]
                        if isfile(tmp['a']):
                            if ci > 0 and checkcf(c, tmp):
                                print(lan['ERROR3'])  # 之前已选择此文件。
                            else:
                                bs3 = True
                                while bs3:
                                    inp2 = input(f"{lan['INPUT4'].replace('<filename>',tmp['f'])}(y/n)")  # 是否选中文件"<filename>"？
                                    if len(inp2) > 0:
                                        if inp2[0].lower() == 'y':
                                            c.append(tmp)
                                            ci = ci + 1
                                            bs3 = False
                                            bs2 = False
                                        elif inp2[0].lower() == 'n':
                                            bs3 = False
                        elif isdir(tmp['a']):
                            nml = tmp['a']
                            nl = listd(nml)
                            if gg:
                                nlf = listf(nl, gl, lx)
                            else:
                                nlf = nl
                            nlfi = getinfod(nlf)
                            zys = int(len(nlf) / yl) + 1
                            ys = 1
                            bs2 = False
        if ci == g:
            bs = False
    return c


def checkcf(list, t):
    "检查新文件是否与列表内有重复"
    for i in list:
        if i['a'] == t['a']:
            return True
    return False
