# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import xml.sax
def loadXML(filen) :
    "加载弹幕"
    p=xml.sax.make_parser()
    p.setFeature(xml.sax.handler.feature_namespaces, 0)
    h=Hander()
    p.setContentHandler(h)
    p.parse(filen)
    return p.getContentHandler().sa
class Hander(xml.sax.ContentHandler) :
    istag=0
    sa={}
    sb=[]
    sc={}
    def startDocument(self) :
        self.sa={}
        self.istag=0
        self.sb=[]
        self.sc={}
    def startElement(self,tag,attributes) :
        if tag=='d' :
            self.istag=1
            at=attributes['p'].split(',')
            self.sc={'ti':at[0],'mod':at[1],'fs':at[2],'fc':at[3],'ut':at[4],'dp':at[5],'si':at[6],'ri':at[7]}
        elif tag=='chatserver' :
            self.istag=2
        elif tag=='chatid' :
            self.istag=3
        elif tag=='mission' :
            self.istag=4
        elif tag=='maxlimit' :
            self.istag=5
        elif tag=='state' :
            self.istag=6
        elif tag=='real_name' :
            self.istag=7
        elif tag=='source' :
            self.istag=8
        else :
            self.istag=0
    def endElement(self,tag) :
        if self.istag>0 :
            self.istag=0
            if tag=='d' :
                self.sb.append(self.sc)
    def characters(self,context) :
        if self.istag==1 :
            self.sc['t']=context
        elif self.istag==2 :
            self.sa['chatserver']=context
        elif self.istag==3 :
            self.sa['chatid']=context
        elif self.istag==4 :
            self.sa['mission']=context
        elif self.istag==5 :
            self.sa['maxlimit']=context
        elif self.istag==6 :
            self.sa['state']=context
        elif self.istag==7 :
            self.sa['real_name']=context
        elif self.istag==8 :
            self.sa['source']=context
    def endDocument(self) :
        self.sa['list']=self.sb