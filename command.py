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
from file import filterd
from lang import lan
def ph() :
    h='''命令行帮助：
    start.py -h/-?/--help   显示命令行帮助信息
    start.py [-i <input>] [-d <下载方式>] [-p <p数>] [-m <boolean>/--ym/--nm] [--ac <boolean>/--yac/--nac] [--dm <boolean>/--ydm/--ndm] [--ad <boolean>/--yad/--nad] [-r <boolean>/--yr/--nr] [-y/-n] [--yf/--nf] [--mc avc/hev] [--ar/--nar] [--ax <number>] [--as <number>] [--ak <number>] [--ab/--nab] [--fa none/prealloc/trunc/falloc] [--sv <boolean>/--ysv/--nsv] [--ma <boolean>/--yma/--nma] [--ms <speed>] [--da <boolean>/--yda/--nda] [--httpproxy <URI>] [--httpsproxy <URI>] [--jt <number>|a|b] [--jts <date>] [-F] [-v <id>] [-a <id>] [-o <dir>] [--af/--naf] [--afp <序号>] [-s] [--slt/--nslt] [--te/--nte] [--bd/--nbd] [--cad/--ncad] [--lrh/--nlrh] [--ahttpproxy <PROXY>] [--ahttpsproxy <PROXY>] [--lan <LANGUAGECODE>]
    start.py show c/w   显示许可证
    -i <input>   av/bv/ep/ss号或者视频链接
    -d <下载方式>   下载方式：1.当前弹幕2.全弹幕3.视频4.当前弹幕+视频5.全弹幕+视频6.仅字幕下载（番剧除外）
    直播回放下载方式：1.视频2.弹幕3.视频+弹幕
    -p <p数>    要下载的P数(两个p数可用,连接)，使用a全选，输入为ep号时可用b选择该ep号，下载上次观看的视频可输入l（仅限番剧）
    -m <boolean>    是否默认下载最高画质
    --ym    相当于-m true
    --nm    相当于-m false
    --ac <boolean>  是否开启继续下载功能
    --yac   相当于--ac true
    --nac   相当于--ac false
    --dm <boolean>  是否启用弹幕过滤
    --ydm   相当于--dm true
    --ndm   相当于--dm false
    --ad <boolean>  是否在合并完成后删除文件
    --yad   相当于--ad true
    --nad   相当于--ad false
    -r <boolean>    是否在下载失败后重新下载
    --yr    相当于-r true
    --nr    相当于-r false
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
    --ysv   相当于--sv true
    --nsv   相当于--sv false
    --ma <boolean>  是否强制增加视频元数据（这会导致原本不需要转码的视频被转码，转码不会影响画质）
    --yma   相当于--ma true
    --nma   相当于--ma false
    --ms <speed>    在使用aria2c下载时最大总体速度，即--max-overall-download-limit的参数，默认单位为B，可以使用K和M为单位
    --da <boolean>  收藏夹是否自动下载每一个视频的所有分P
    --yda   相当于--da true
    --nda   相当于--da false
    --httpproxy <URI>   使用HTTP代理
    --httpsproxy <URI>  使用HTTPS代理 
    --jt <number>|a|b 下载全弹幕时两次抓取之间的天数，范围为1-365，a会启用自动模式（推荐自动模式），番剧模式下b修改抓取起始日期
    --jts <date>    下载全弹幕时且视频为番剧时抓取起始日期的默认值（原始值为番剧上传时间），格式例如1989-02-25，即年-月-日
    -F  视频下载时仅显示所有可选画质但不下载（使用该参数时，不受静默模式影响）
    -v <id>     视频下载时选择相应的画质，id为画质前序号
    -a <id>     视频下载时选择相应的音质，id为音质前序号
    -o <dir>    设置下载文件夹
    --af    解析收藏夹时若未指定收藏夹，自动解析为默认收藏夹
    --naf   解析收藏夹时若未指定收藏夹，不自动解析为默认收藏夹而是返回列表以选择
    --afp <序号>  解析收藏夹时若未指定收藏夹，解析列表中指定序号的收藏夹，支持多个序号（中间用,隔开），可使用a全选
    -s      启用静默模式，关闭除版权声明和错误信息和进度信息（即内置下载器和aria2输出的信息，以及下载完成的信息）外的所有输出（若有重复文件，在不手动设置的情况下默认为覆盖）
    --slt   下载小视频时，放入文件名中的描述长度可以超过20字
    --nslt  下载小视频时，放入文件名中的描述长度无法超过20字，超出部分将被舍弃
    --te    requests使用环境变量中的代理设置
    --nte   requests不使用环境变量中的代理设置
    --bd    合并完成后删除文件时保留字幕文件
    --nbd   合并完成后删除文件时删除字幕文件
    --cad   使用aria2c时关闭异步DNS（关闭后在Windows系统下可以解决Timeout while contacting DNS servers问题）
    --ncad  使用aria2c时启用异步DNS
    --lrh   直播回放简介写入元数据时进行去HTML化
    --nlrh  直播回放简介写入元数据时不进行去HTML化
    --ahttpproxy <PROXY>    指定aria2c使用的http代理，即aria2c的--http-proxy参数
    --ahttpsproxy <PROXY>   指定aria2c使用的https代理，即aria2c的--https-proxy参数
    --lan <LANGUAGECODE>    设置UI语言
    注1：如出现相同的选项，只有第一个会生效
    注2：命令行参数的优先级高于settings.json里的设置
    注3：ffmpeg和aria2c需要自行下载并确保放入当前文件夹或者放入环境变量PATH指定的目录中
    注4：当下载收藏夹/频道，除了-i和-p参数外，其他参数将被沿用至收藏夹/频道视频的下载设置，-i和-p参数只对收藏夹/频道起作用'''
    print(h)
def gopt(args,d:bool=False) :
    re=getopt(args,'h?i:d:p:m:r:ynFv:a:o:s',['help','ac=','dm=','ad=','yf','nf','mc=','ar','nar','ax=','as=','ak=','ab','nab','fa=','sv=','ma=','ms=','da=','httpproxy=','httpsproxy=','jt=','jts=','af','naf','afp=','slt','nslt','te','nte','bd','nbd','cad','ncad','lrh','nlrh','ym','nm','yac','nac','ydm','ndm','yad','nad','yr','nr','ysv','nsv','yma','nma','yda','nda','ahttpproxy=','ahttpsproxy=','lan='])
    if d:
        print(re)
    rr=re[0]
    r={}
    for i in rr:
        if i[0]=='-h' or i[0]=='-?' or i[0]=='--help':
            ph()
            exit()
        if i[0]=='-i' and not 'i' in r:
            r['i']=i[1]
        if i[0]=='-d' and not 'd' in r and i[1].isnumeric() and int(i[1])>0 and int(i[1])<7 :
            r['d']=int(i[1])
        if i[0]=='-p' and not 'p' in r :
            r['p']=i[1]
        if i[0]=='-m' and not 'm' in r :
            if i[1].lower()=='true' :
                r['m']=True
            elif i[1].lower()=='false' :
                r['m']=False
        if i[0]=='--ym' and not 'm' in r:
            r['m']=True
        if i[0]=='--nm' and not 'm' in r:
            r['m']=False
        if i[0]=='--ac' and not 'ac' in r:
            if i[1].lower()=='true' :
                r['ac']=True
            elif i[1].lower()=='false' :
                r['ac']=False
        if i[0]=='--yac' and not 'ac' in r:
            r['ac']=True
        if i[0]=='--nac' and not 'ac' in r:
            r['ac']=False
        if i[0]=='--dm' and not 'dm' in r:
            if i[1].lower()=='true' :
                r['dm']=True
            elif i[1].lower()=='false' :
                r['dm']=False
        if i[0]=='--ydm' and not 'dm' in r:
            r['dm']=True
        if i[0]=='--ndm' and not 'dm' in r:
            r['dm']=False
        if i[0]=='--ad' and not 'ad' in r:
            if i[1].lower()=='true' :
                r['ad']=True
            elif i[1].lower()=='false' :
                r['ad']=False
        if i[0]=='--yad' and not 'ad' in r:
            r['ad']=True
        if i[0]=='--nad' and not 'ad' in r:
            r['ad']=False
        if i[0]=='-r' and not 'r' in r:
            if i[1].lower()=='true' :
                r['r']=True
            elif i[1].lower()=='false' :
                r['r']=False
        if i[0]=='--yr' and not 'r' in r:
            r['r']=True
        if i[0]=='--nr' and not 'r' in r:
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
        if i[0]=='--ysv' and not 'sv' in r:
            r['sv']=True
        if i[0]=='--nsv' and not 'sv' in r:
            r['sv']=False
        if i[0]=='--ma' and not 'ma' in r:
            if i[1].lower()=='true' :
                r['ma']=True
            elif i[1].lower()=='false' :
                r['ma']=False
        if i[0]=='--yma' and not 'ma' in r:
            r['ma']=True
        if i[0]=='--nma' and not 'ma' in r:
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
        if i[0]=='--yda' and not 'da' in r:
            r['da']=True
        if i[0]=='--nda' and not 'da' in r:
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
        if i[0]=='-o' and not 'o' in r:
            r['o']=filterd(i[1])
        if i[0]=='--af' and not 'af' in r:
            r['af']=False
        if i[0]=='--naf' and not 'af' in r:
            r['af']=True
        if i[0]=='--afp' and not 'afp' in r:
            r['afp']=i[1]
        if i[0]=='-s' and not 's' in r:
            r['s']=True
        if i[0]=='--slt' and not 'slt' in r:
            r['slt']=True
        if i[0]=='--nslt' and not 'slt' in r:
            r['slt']=False
        if i[0]=='--te' and not 'te' in r:
            r['te']=True
        if i[0]=='--nte' and not 'te' in r:
            r['te']=False
        if i[0]=='--bd' and not 'bd' in r:
            r['bd']=True
        if i[0]=='--nbd' and not 'bd' in r:
            r['bd']=False
        if i[0]=='--cad' and not 'cad' in r:
            r['cad']=True
        if i[0]=='--ncad' and not 'cad' in r:
            r['cad']=False
        if i[0]=='--lrh' and not 'lrh' in r:
            r['lrh']=True
        if i[0]=='--nlrh' and not 'lrh' in r:
            r['lrh']=False
        if i[0]=='--ahttpproxy' and not 'ahttpproxy' in r:
            r['ahttpproxy']=i[1]
        if i[0]=='--ahttpsproxy' and not 'ahttpsproxy' in r:
            r['ahttpsproxy']=i[1]
        if i[0]=='--lan' and not 'lan' in r and (i[1]=='null' or i[1] in lan) :
            r['lan']=i[1]
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
        print(gopt(sys.argv[1:],True))
