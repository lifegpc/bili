# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from html.parser import HTMLParser
class Myparser(HTMLParser) :
    "解析B站HTML"
    script=0
    videodata=''
    def handle_starttag(self,tag,attrs) :
        if tag=='script' :
            self.script=1
        else :
            self.script=0
    def handle_data(self,data) :
        if self.script==1 and data[0:24]=="window.__INITIAL_STATE__":
            self.videodata=data[25:len(data)-122]
class Myparser2(HTMLParser) :
    "解析B站HTML"
    script=0
    videodata=''
    def handle_starttag(self,tag,attrs) :
        if tag=='script' :
            self.script=1
        else :
            self.script=0
    def handle_data(self,data) :
        if self.script==1 and data[0:19]=="window.__playinfo__":
            self.videodata=data[20:]
