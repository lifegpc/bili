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
from biliTime import checktime
from file import filterd
from lang import lan,getlan,getdict
from JSONParser import loadset
import sys
def ph() :
    h=f'''{la['O1']}
    start.py -h/-?/--help   {la['O2']}
    start.py [-i <input>] [-d <method>] [-p <number>] [-m <boolean>/--ym/--nm] [--ac <boolean>/--yac/--nac] [--dm <boolean>/--ydm/--ndm] [--ad <boolean>/--yad/--nad] [-r <boolean>/--yr/--nr] [-y/-n] [--yf/--nf] [--mc avc/hev] [--ar/--nar] [--ax <number>] [--as <number>] [--ak <number>] [--ab/--nab] [--fa none/prealloc/trunc/falloc] [--sv <boolean>/--ysv/--nsv] [--ma <boolean>/--yma/--nma] [--ms <speed>] [--da <boolean>/--yda/--nda] [--httpproxy <URI>] [--httpsproxy <URI>] [--jt <number>|a|b] [--jts <date>] [-F] [-v <id>] [-a <id>] [-o <dir>] [--af/--naf] [--afp <number>] [-s] [--slt/--nslt] [--te/--nte] [--bd/--nbd] [--cad/--ncad] [--lrh/--nlrh] [--ahttpproxy <PROXY>] [--ahttpsproxy <PROXY>] [--lan <LANGUAGECODE>] [--bp/--nbp] [--in/--nin] [--mt/--nmt] [--vi <URL_index>]
    start.py show c/w   {la['O3']}
    -i <input>   {la['O4']}
    -d <method>   {la['O5']}
    {la['O6']}
    -p <number>    {la['O7']}
    -m <boolean>    {la['O8']}
    --ym    {la['AL'].replace('<value>','-m true')}
    --nm    {la['AL'].replace('<value>','-m false')}
    --ac <boolean>  {la['O9']}
    --yac   {la['AL'].replace('<value>','--ac true')}
    --nac   {la['AL'].replace('<value>','--ac false')}
    --dm <boolean>  {la['O10']}
    --ydm   {la['AL'].replace('<value>','--dm true')}
    --ndm   {la['AL'].replace('<value>','--dm false')}
    --ad <boolean>  {la['O11']}
    --yad   {la['AL'].replace('<value>','--ad true')}
    --nad   {la['AL'].replace('<value>','--ad false')}
    -r <boolean>    {la['O12']}
    --yr    {la['AL'].replace('<value>','-r true')}
    --nr    {la['AL'].replace('<value>','-r false')}
    -y  {la['O13']}
    -n  {la['O14']}
    --yf    {la['O15']}
    --nf    {la['O16']}
    --mc avc/hev    {la['O17']}
    --ar    {la['O18']}
    --nar   {la['O19']}
    --ax <number>   {la['O20'].replace('<value>','1-16')}
    --as <number>   {la['O21'].replace('<value>','1-*')}
    --ak <number>   {la['O22'].replace('<value1>','M').replace('<value2>','1-1024')}
    --ab    {la['O23']}
    --nab   {la['O24']}
    --fa none/prealloc/trunc/falloc {la['O25']}
    --sv <boolean>  {la['O26']}
    --ysv   {la['AL'].replace('<value>','--sv true')}
    --nsv   {la['AL'].replace('<value>','--sv false')}
    --ma <boolean>  {la['O27']}
    --yma   {la['AL'].replace('<value>','--ma true')}
    --nma   {la['AL'].replace('<value>','--ma false')}
    --ms <speed>    {la['O28']}
    --da <boolean>  {la['O29']}
    --yda   {la['AL'].replace('<value>','--da true')}
    --nda   {la['AL'].replace('<value>','--da false')}
    --httpproxy <URI>   {la['O30']}{la['O31']}
    --httpsproxy <URI>  {la['O32']}{la['O31']}
    --jt <number>|a|b   {la['O33'].replace('<value>','1-365')}
    --jts <date>    {la['O34']}
    -F      {la['O35']}
    -v <id>     {la['O36']}
    -a <id>     {la['O37']}
    -o <dir>    {la['O38']}
    --af    {la['O39']}
    --naf   {la['O40']}
    --afp <number>  {la['O41']}
    -s      {la['O42']}
    --slt   {la['O43']}
    --nslt  {la['O44']}
    --te    {la['O45']}
    --nte   {la['O46']}
    --bd    {la['O47']}
    --nbd   {la['O48']}
    --cad   {la['O49']}
    --ncad  {la['O50']}
    --lrh   {la['O51']}
    --nlrh  {la['O52']}
    --ahttpproxy <PROXY>    {la['O53']}
    --ahttpsproxy <PROXY>   {la['O54']}
    --lan <LANGUAGECODE>    {la['O55']}
    --bp    {la['O60']}
    --nbp   {la['O61']}
    --in    {la['O62']}
    --nin   {la['O63']}
    --mt    {la['O64']}
    --nmt   {la['O65']}
    --vi <URL_index>    {la['O66']}
    {la['O56']}
    {la['O57']}
    {la['O58']}
    {la['O59']}'''
    print(h)
def gopt(args,d:bool=False) :
    re = getopt(args, 'h?i:d:p:m:r:ynFv:a:o:s', ['help', 'ac=', 'dm=', 'ad=', 'yf', 'nf', 'mc=', 'ar', 'nar', 'ax=', 'as=', 'ak=', 'ab', 'nab', 'fa=', 'sv=', 'ma=', 'ms=', 'da=', 'httpproxy=', 'httpsproxy=', 'jt=', 'jts=', 'af', 'naf', 'afp=', 'slt', 'nslt', 'te', 'nte', 'bd', 'nbd', 'cad', 'ncad', 'lrh', 'nlrh', 'ym', 'nm', 'yac', 'nac', 'ydm', 'ndm', 'yad', 'nad', 'yr', 'nr', 'ysv', 'nsv', 'yma', 'nma', 'yda', 'nda', 'ahttpproxy=', 'ahttpsproxy=', 'lan=', 'bp', 'nbp', 'in', 'nin', 'mt', 'nmt', 'vi='])
    if d:
        print(re)
    rr=re[0]
    r={}
    h=False
    for i in rr:
        if i[0]=='-h' or i[0]=='-?' or i[0]=='--help':
            h=True
        if i[0]=='-i' and not 'i' in r:
            r['i']=i[1]
        if i[0]=='-d' and not 'd' in r and i[1].isnumeric() and int(i[1])>0 and int(i[1])<8 :
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
        if i[0]=='--bp' and not 'bp' in r:
            r['bp']=True
        if i[0]=='--nbp' and not 'bp' in r:
            r['bp']=False
        if i[0]=='--in' and not 'in' in r:
            r['in']=True
        if i[0]=='--nin' and not 'in' in r:
            r['in']=False
        if i[0]=='--mt' and not 'mt' in r:
            r['mt']=True
        if i[0]=='--nmt' and not 'mt' in r:
            r['mt']=False
        if i[0]=='--vi' and not 'vi' in r:
            if i[1].isnumeric():
                r['vi'] = int(i[1])
    if h:
        global la
        la=getdict('command',getlan(se,r))
        ph()
        exit()
    for i in re[1] :
        if i.lower()=="show":
            r['SHOW'] = True
    return r
la=None
se=loadset()
if se==-1 or se==-2 :
    se={}
la=getdict('command',getlan(se,{}))
if __name__ == "__main__":
    import sys
    print(sys.argv)
    if len(sys.argv)==1 :
        print('该文件仅供测试命令行输入使用，请运行start.py')
    else :
        print(gopt(sys.argv[1:],True))
