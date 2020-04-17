from getopt import getopt
def ph() :
    h='''命令行帮助：
    start.py -h/-?/--help   显示命令行帮助信息
    start.py [-i <输入>] [-d <下载方式>] [-p <p数>]
    -i <输入>   av/bv/ep/ss号或者视频链接
    -d <下载方式>   下载方式：1.当前弹幕2.全弹幕3.视频4.当前弹幕+视频5.全弹幕+视频
    -p <p数>    要下载的P数(两个p数可用,连接)，使用a全选，输入为ep号时可用b选择该ep号'''
    print(h)
def gopt(args) :
    re=getopt(args,'h?i:d:p:',['help'])
    print(re)
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
    return r
if __name__ == "__main__":
    import sys
    if len(sys.argv)==1 :
        print('该文件仅供测试命令行输入使用，请运行start.py')
    else :
        print(gopt(sys.argv[1:]))
