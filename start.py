import requests
import HTMLParser
import JSONParser
import PrintInfo
import biliLogin
import biliPlayerXmlParser
import biliDanmu
import biliTime
if __name__=='__main__':
    inp=input("请输入av号（暂不支持SS号）：")
    av=False
    ss=False
    if inp[0:2].lower()=='ss' and inp[2:].isnumeric() :
        s="https://www.bilibili.com/bangumi/play/ss"+inp[2:]
        ss=True
    elif inp[0:2].lower()=='av' and inp[2:].isnumeric() :
        s="https://www.bilibili.com/video/av"+inp[2:]
        av=True
    elif inp.isnumeric() :
        s="https://www.bilibili.com/video/av"+inp
        av=True
    else :
        print('输入有误')
        exit()
    section=requests.session()
    section.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36","Connection": "keep-alive","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Language": "zh-CN,zh;q=0.8"})
    read=JSONParser.loadcookie(section)
    login=0
    if read==0 :
        read=biliLogin.tryok(section)
        if read==True :
            print("登录校验成功！")
            login=1
        elif read==False :
            print('网络错误！校验失败！')
            exit()
        else :
            print("登录信息已过期！")
            login=2
    elif read==-1 :
        login=2
    else :
        print("文件读取错误！")
        login=2
    if login==2 :
        read=biliLogin.login(section)
        if read==0 :
            login=1
        elif read==1 :
            exit()
        else :
            exit()
    xml=0
    xmlc=[]
    read=biliPlayerXmlParser.loadXML()
    if read==-1 :
        xml=2
    else :
        xml=1
        xmlc=read
    if xml==1 :
        bs=True
        while bs:
            yn=input("是否启用弹幕过滤(y/n)？")
            if yn[0].lower() =='y' :
                bs=False
            if yn[0].lower() =='n' :
                bs=False
                xml=2
    re=section.get(s)
    parser=HTMLParser.Myparser()
    parser.feed(re.text)
    if av :
        data=JSONParser.Myparser(parser.videodata)
        PrintInfo.printInfo(data)
        cho=[]
        if data['videos']==1 :
            cho.append(1)
        else :
            bs=True
            while bs :
                inp=input('请输入你想下载弹幕的视频编号，每两个编号间用,隔开，全部下载可输入a')
                cho=[]
                if inp[0]=='a' :
                    print('您全选了所有视频')
                    for i in range(1,data['videos']+1) :
                        cho.append(i)
                    bs=False
                else :
                    inp=inp.split(',')
                    bb=True
                    for i in inp :
                        if i.isnumeric() and int(i)<=data['videos'] and (not (int(i) in cho)) :
                            cho.append(int(i))
                        else :
                            bb=False
                    if bb :
                        bs=False
                        for i in cho :
                            print("您选中了第"+str(i)+"P："+data['page'][i-1]['part'])
        cho2=0
        bs=True
        while bs :
            inp=input('请输入你要下载的方式：\n1.当前弹幕下载\n2.全弹幕下载')
            if inp[0] =='1' :
                cho2=1
                bs=False
            elif inp[0] =='2' :
                cho2=2
                bs=False
        if cho2==1 :
            for i in cho :
                read=biliDanmu.DanmuGetn(i,data,section,'av',xml,xmlc)
                if read==-1 or read==-4 :
                    pass
                elif read==0 :
                    print('第'+str(i)+"P下载完成")
                else :
                    exit()
        elif cho2==2 :
            read=biliTime.equal(biliTime.getDate(data['pubdate']),biliTime.getNowDate())
            if read==0 or read==1 :
                print('不能下载该视频全弹幕！')
                exit()
            for i in cho :
                read=biliDanmu.DanmuGeta(i,data,section,'av',xml,xmlc)
                if read==-2 :
                    pass
                elif read==0 :
                    print("第"+str(i)+"P下载完成")
                else :
                    exit()
    if ss :
        data=JSONParser.Myparser2(parser.videodata)
        print(data)
        len=PrintInfo.printInfo2(data)
        cho=[]
        if len==1:
            cho.append(1)
        else :
            bs=True
            while bs :
                inp=input('请输入你想下载弹幕的视频编号，每两个编号间用,隔开，全部下载可输入a')
                cho=[]
                if len(inp)>0:
                    if inp[0]=='a' :
                        print('你全选了所有视频')
                        for j in range(1,len+1) :
                            cho.append(j)
                        bs=False
else :
    print("请运行根目录下的start.py")