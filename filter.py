# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import file
import biliPlayerXmlParser
from os.path import exists
import biliDanmuXmlParser
from os import remove
import biliDanmuXmlFilter
import biliDanmuCreate
if __name__!="__main__" :
    print('请直接运行filter.py')
else :
    read=biliPlayerXmlParser.loadXML()
    xml=read#弹幕过滤列表
    if read==-1 :
        print('没有tv.bilibili.plater.xml文件')
        exit(-1)
    bs=True
    while bs :
        inp=input('请输入要过滤的文件数量：')
        if len(inp)>0 :
            if inp.isnumeric() :
                g=int(inp)
                bs=False
    fl=file.getfilen(g=g)
    for i in fl :
        if exists(i['a']) :
            try :
                read=biliDanmuXmlParser.loadXML(i['a'])
            except :
                print('此文件不是弹幕文件。')
                continue
            r=read
            input('按Enter开始选择保存文件名')
            read=file.getfilen(save=True)
            if read==-1 :
                read=file.getfilen('.',save=True)
            fn=read[0]
            if exists(fn['a']) :
                remove(fn['a'])
            try :
                f=open(fn['a'],mode='w',encoding='utf8')
                f.write('<?xml version="1.0" encoding="UTF-8"?>')
                f.write('<i><chatserver>%s</chatserver><chatid>%s</chatid><mission>%s</mission><maxlimit>%s</maxlimit><state>%s</state><real_name>%s</real_name><source>%s</source>' % (r['chatserver'],r['chatid'],r['mission'],r['maxlimit'],r['state'],r['real_name'],r['source']))
                z=len(r['list'])
                g=0
                for j in r['list'] :
                    if biliDanmuXmlFilter.Filter(j,xml) :
                        g=g+1
                    else :
                        try :
                            f.write(biliDanmuCreate.objtoxml(j))
                        except :
                            print('保存到文件失败：'+fn['f'])
                            continue
                m=z-g
                print('该文件中共有%s条弹幕，过滤了%s条，剩余%s条' %(z,g,m))
            except :
                print('保存到文件失败：'+fn['f'])
                continue
        else :
            print('\"%s\"文件不存在' %(i['f']))