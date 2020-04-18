from getopt import getopt
def ph() :
    h='''命令行帮助：
    start.py -h/-?/--help   显示命令行帮助信息
    start.py [-i <输入>] [-d <下载方式>] [-p <p数>] [-m <boolean>] [--ac <boolean>] [--dm <boolean>] [--ad <boolean>] [-r <boolean>]
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
    注1：如出现相同的选项，只有第一个会生效
    注2：命令行参数的优先级高于settings.json里的设置'''
    print(h)
def gopt(args) :
    re=getopt(args,'h?i:d:p:m:r:yn',['help','ac=','dm=','ad='])
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
    return r
if __name__ == "__main__":
    import sys
    print(sys.argv)
    if len(sys.argv)==1 :
        print('该文件仅供测试命令行输入使用，请运行start.py')
    else :
        print(gopt(sys.argv[1:]))
