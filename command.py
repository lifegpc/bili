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
from getopt import getopt
from re import search
from PrintInfo import pr,prc
from biliTime import checktime
def ph() :
    h='''命令行帮助：
    start.py -h/-?/--help   显示命令行帮助信息
    start.py [-i <输入>] [-d <下载方式>] [-p <p数>] [-m <boolean>] [--ac <boolean>] [--dm <boolean>] [--ad <boolean>] [-r <boolean>] [-y/-n] [--yf/--nf] [--mc avc/hev] [--ar/--nar] [--ax <number>] [--as <number>] [--ak <number>] [--ab/--nab] [--fa none/prealloc/trunc/falloc] [--sv <boolean>] [--ma <boolean>] [--ms <speed>] [--da <boolean>] [--httpproxy <URI>] [--httpsproxy <URI>] [--jt <number>|a|b] [--jts <date>] [-F] [-v <id>] [-a <id>]
    start.py show c/w   显示许可证
    -i <输入>   av/bv/ep/ss号或者视频链接
    -d <下载方式>   下载方式：1.当前弹幕2.全弹幕3.视频4.当前弹幕+视频5.全弹幕+视频
    -p <p数>    要下载的P数(两个p数可用,连接)，使用a全选，输入为ep号时可用b选择该ep号
    -m <boolean>    是否默认下载最高画质
    --ac <boolean>  是否开启继续下载功能
    --dm <boolean>  是否启用弹幕过滤
    --ad <boolean>  是否在合并完成后删除文件
    -r <boolean>    是否在下载失败后重新下载
    -y  覆盖所有重复文件
    -n  不覆盖重复文件
    --yf    使用ffmpeg
    --nf    不使用ffmpeg
    --mc avc/hev    默认下载最高画质偏好编码器
    --ar    使用aria2c下载
    --nar   不使用aria2c下载
    --ax <number>   aria2c单个服务器最大连接数即-x的参数，范围为1-16
    --as <number>   aria2c单个文件最大连接数即-s的参数，范围为1-*
    --ak <number>   aria2c文件分片大小即-k的参数，范围为1-1024，单位为M
    --ab    在使用aria2c下载时使用备用网址
    --nab   在使用aria2c下载时不使用备用网址
    --fa none/prealloc/trunc/falloc 在使用arai2c下载时预分配方式即--file-allocation的参数
    --sv <boolean>  文件名中是否输出视频画质信息
    --ma <boolean>  是否强制增加视频元数据（这会导致原本不需要转码的视频被转码，转码不会影响画质）
    --ms <speed>    在使用aria2c下载时最大总体速度，即--max-overall-download-limit的参数，默认单位为B，可以使用K和M为单位
    --da <boolean>  收藏夹是否自动下载每一个视频的所有分P
    --httpproxy <URI>   使用HTTP代理
    --httpsproxy <URI>  使用HTTPS代理 
    --jt <number>|a|b 下载全弹幕时两次抓取之间的天数，范围为1-365，a会启用自动模式（推荐自动模式），番剧模式下b修改抓取起始日期
    --jts <date>    下载全弹幕时且视频为番剧时抓取起始日期的默认值（原始值为番剧上传时间），格式例如1989-02-25，即年-月-日
    -F  视频下载时仅显示所有可选画质但不下载
    -v <id>     视频下载时选择相应的画质，id为画质前序号
    -a <id>     视频下载时选择相应的音质，id为音质前序号
    注1：如出现相同的选项，只有第一个会生效
    注2：命令行参数的优先级高于settings.json里的设置
    注3：ffmpeg和aria2c需要自行下载并确保放入当前文件夹或者放入环境变量PATH指定的目录中
    注4：当下载收藏夹/频道，除了-i和-p参数外，其他参数将被沿用至收藏夹/频道视频的下载设置，-i和-p参数只对收藏夹/频道起作用'''
    print(h)
def gopt(args) :
    re=getopt(args,'h?i:d:p:m:r:ynFv:a:',['help','ac=','dm=','ad=','yf','nf','mc=','ar','nar','ax=','as=','ak=','ab','nab','fa=','sv=','ma=','ms=','da=','httpproxy=','httpsproxy=','jt=','jts='])
    rr=re[0]
    r={}
    for i in rr:
        if i[0]=='-h' or i[0]=='-?' or i[0]=='--help':
            ph()
            exit()
        if i[0]=='-i' and not 'i' in r:
            r['i']=i[1]
        if i[0]=='-d' and not 'd' in r and i[1].isnumeric() and int(i[1])>0 and int(i[1])<6 :
            r['d']=int(i[1])
        if i[0]=='-p' and not 'p' in r :
            r['p']=i[1]
        if i[0]=='-m' and not 'm' in r :
            if i[1].lower()=='true' :
                r['m']=True
            elif i[1].lower()=='false' :
                r['m']=False
        if i[0]=='--ac' and not 'ac' in r:
            if i[1].lower()=='true' :
                r['ac']=True
            elif i[1].lower()=='false' :
                r['ac']=False
        if i[0]=='--dm' and not 'dm' in r:
            if i[1].lower()=='true' :
                r['dm']=True
            elif i[1].lower()=='false' :
                r['dm']=False
        if i[0]=='--ad' and not 'ad' in r:
            if i[1].lower()=='true' :
                r['ad']=True
            elif i[1].lower()=='false' :
                r['ad']=False
        if i[0]=='-r' and not 'r' in r:
            if i[1].lower()=='true' :
                r['r']=True
            elif i[1].lower()=='false' :
                r['r']=False
        if i[0]=='-y' and not 'y' in r:
            r['y']=True
        if i[0]=='-n' and not 'y' in r:
            r['y']=False
        if i[0]=='--yf' and not 'yf' in r:
            r['yf']=True
        if i[0]=='--nf' and not 'yf' in r:
            r['yf']=False
        if i[0]=='--mc' and not 'mc' in r:
            if i[1].lower()=='avc' :
                r['mc']=True
            elif i[1].lower()=='hev' :
                r['mc']=False
        if i[0]=='--ar' and not 'ar' in r:
            r['ar']=True
        if i[0]=='--nar' and not 'ar' in r:
            r['ar']=False
        if i[0]=='--ax' and not 'ax' in r:
            if i[1].isnumeric() :
                i2=int(i[1])
                if i2<17 and i2>0 :
                    r['ax']=i2
        if i[0]=='--as' and not 'as' in r:
            if i[1].isnumeric() :
                i2=int(i[1])
                if i2>0 :
                    r['as']=i2
        if i[0]=='--ak' and not 'ak' in r:
            if i[1].isnumeric() :
                i2=int(i[1])
                if i2>0 and i2<1025 :
                    r['ak']=i2
        if i[0]=='--ab' and not 'ab' in r:
            r['ab']=True
        if i[0]=='--nab' and not 'ab' in r:
            r['ab']=False
        if i[0]=='--fa' and not 'fa' in r:
            if i[1].lower()=='none' or i[1].lower()=='prealloc' or i[1].lower()=='trunc' or i[1].lower()=='falloc':
                r['fa']=i[1].lower()
        if i[0]=='--sv' and not 'sv' in r:
            if i[1].lower()=='true' :
                r['sv']=True
            elif i[1].lower()=='false' :
                r['sv']=False
        if i[0]=='--ma' and not 'ma' in r:
            if i[1].lower()=='true' :
                r['ma']=True
            elif i[1].lower()=='false' :
                r['ma']=False
        if i[0]=='--ms' and not 'ms' in r:
            t=search("^[0-9]+[MK]?$",i[1])
            if t!=None :
                r['ms']=i[1]
        if i[0]=='--da' and not 'da' in r:
            if i[1].lower()=='true' :
                r['da']=True
            elif i[1].lower()=='false' :
                r['da']=False
        if i[0]=='--httpproxy' and not 'httpproxy' in r:
            r['httpproxy']=i[1]
        if i[0]=='--httpsproxy' and not 'httpsproxy' in r:
            r['httpsproxy']=i[1]
        if i[0]=="--jt" and not 'jt' in r:
            if i[1].lower()=='a' or i[1].lower()=='b' or i[1].isnumeric():
                r['jt']=i[1].lower()
        if i[0]=='--jts' and not 'jts' in r:
            if checktime(i[1]) :
                r['jts']=i[1]
        if i[0]=='-F' and not 'F' in r:
            r['F']=True
        if i[0]=='-v' and not 'v' in r:
            if i[1].isnumeric() :
                if int(i[1])>0 :
                    r['v']=i[1]
        if i[0]=='-a' and not 'a' in r:
            if i[1].isnumeric():
                if int(i[1])>0:
                    r['a']=i[1]
    for i in re[1] :
        if i.lower()=="show":
            prc()
            exit()
    return r
if __name__ == "__main__":
    pr()
    import sys
    print(sys.argv)
    if len(sys.argv)==1 :
        print('该文件仅供测试命令行输入使用，请运行start.py')
    else :
        print(gopt(sys.argv[1:]))
