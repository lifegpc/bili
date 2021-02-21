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
import xml.sax


def loadXML():
    "加载BiliBili弹幕过滤文件"
    try:
        fo = open('tv.bilibili.player.xml', mode='r')
    except:
        return -1
    fo.close()
    p = xml.sax.make_parser()
    p.setFeature(xml.sax.handler.feature_namespaces, 0)
    h = Hander()
    p.setContentHandler(h)
    p.parse('tv.bilibili.player.xml')
    return p.getContentHandler().sa


class Hander(xml.sax.ContentHandler):
    istag = False
    sa = []
    now = {}

    def startElement(self, tag, attributes):
        if tag == 'item':
            self.istag = True
            self.now = {'e': attributes['enabled']}
        else:
            self.istag = False

    def characters(self, context):
        if self.istag:
            if context[0] == 't':
                self.now['t'] = 't'
            elif context[0] == 'r':
                self.now['t'] = 'r'
            elif context[0] == 'u':
                self.now['t'] = 'u'
            else:
                self.now['t'] = ''
            self.now['w'] = context[2:len(context)]

    def endElement(self, tag):
        if tag == 'item' and self.istag:
            self.istag = False
            self.sa.append(self.now)


if __name__ == '__main__':
    re = loadXML()
    if re == -1:
        print('没有文件')
    else:
        print(re)
