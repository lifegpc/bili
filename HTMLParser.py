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