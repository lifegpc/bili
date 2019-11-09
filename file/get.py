from file.dir import listd,getinfod,printinfod,listc
from file.filter import listf
from os.path import abspath,exists,isdir,isfile
def getfilen(l='Download',lx=['xml'],yl=15,g=1) :
    """获取需要的文件名
    -1 文件夹不存在
    -2 参数错误"""
    nml=abspath(l)
    if not exists(nml) :
        return -1
    if g<1 or yl<1 :
        return -2
    nl=listd(nml)
    nlf=listf(nl,2,lx)
    nlfi=getinfod(nlf)
    zys=int(len(nlf)/yl)+1
    ys=1
    gg=True
    gl=2
    ci=0
    c=[]
    bs=True
    while bs:
        if zys==1 :
            printinfod(nlfi)
        elif ys==zys :
            printinfod(listc(nlfi,(ys-1)*yl,len(nlf)))
        else :
            printinfod(listc(nlfi,(ys-1)*yl,ys*yl))
        if ys==zys :
            sl=(len(nlf)-1)%yl+1
        else :
            sl=yl
        print('当前显示第%s/%s页'%(ys,zys))
        if ys!=1 :
            print('a.上一页\t',end='')
        if ys!=zys :
            print('b.下一页\t',end='')
        print('c.上一文件夹\t',end='')
        if gg and gl==2 :
            print('d.不显示无后缀名文件\t',end='')
        elif gg and gl==0 :
            print('d.显示无后缀名文件\t',end='')
        if gg:
            print('e.显示所有文件\t',end='')
        else :
            print('e.显示过滤后文件\t',end='')
        print('f.手动输入其他文件夹')
        bs2=True
        while bs2:
            inp=input('请输入文件名之前的序号选中文件，或输入文件夹名之前的序号进入文件夹，或输入操作之前的字母进行该操作')
            if len(inp)>0 :
                if inp[0]=='a' and ys!=1 :
                    ys=ys-1
                    bs2=False
                elif inp[0]=='b' and ys!=zys :
                    ys=ys+1
                    bs2=False
                elif inp[0]=='c' :
                    tmp=abspath("%s/../"%(nml))
                    if exists(tmp) :
                        nml=tmp
                        nl=listd(nml)
                        if gg:
                            nlf=listf(nl,gl,lx)
                        else :
                            nlf=nl
                        nlfi=getinfod(nlf)
                        zys=int(len(nlf)/yl)+1
                        ys=1
                        bs2=False
                    else :
                        print('上一层文件夹不存在')
                elif inp[0]=='d' and gg :
                    if gl==2 :
                        gl=0
                    elif gl==0 :
                        gl=2
                    nlf=listf(nl,gl,lx)
                    nlfi=getinfod(nlf)
                    zys=int(len(nlf)/yl)+1
                    ys=1
                    bs2=False
                elif inp[0]=='e' :
                    if gg :
                        gg=False
                    else :
                        gg=True
                    if gg:
                        nlf=listf(nl,gl,lx)
                    else :
                        nlf=nl
                    nlfi=getinfod(nlf)
                    zys=int(len(nlf)/yl)+1
                    ys=1
                    bs2=False
                elif inp[0]=='f' :
                    inp2=input('请输入文件夹位置（支持绝对和相对位置）：')
                    tmp=abspath(inp2)
                    if exists(tmp) :
                        nml=tmp
                        nl=listd(nml)
                        if gg:
                            nlf=listf(nl,gl,lx)
                        else :
                            nlf=nl
                        nlfi=getinfod(nlf)
                        zys=int(len(nlf)/yl)+1
                        ys=1
                        bs2=False
                    else :
                        print('该文件不存在')
                elif inp.isnumeric() :
                    if int(inp)>0 and int(inp)<=sl :
                        tmp=nlf[(ys-1)*yl+int(inp)-1]
                        if isfile(tmp['a']) :
                            if ci>0 and checkcf(c,tmp) :
                                print('文件与已选择文件重复')
                            else :
                                bs3=True
                                while bs3 :
                                    inp2=input('是否选中\"%s\"？(y/n)' %(tmp['f']))
                                    if len(inp2)>0 :
                                        if inp2[0].lower()=='y' :
                                            c.append(tmp)
                                            ci=ci+1
                                            bs3=False
                                            bs2=False
                                        elif inp2[0].lower()=='n' :
                                            bs3=False
                        elif isdir(tmp['a']) :
                            nml=tmp['a']
                            nl=listd(nml)
                            if gg :
                                nlf=listf(nl,gl,lx)
                            else :
                                nlf=nl
                            nlfi=getinfod(nlf)
                            zys=int(len(nlf)/yl)+1
                            ys=1
                            bs2=False
        if ci==g :
            bs=False
    return c
def checkcf(list,t):
    "检查新文件是否与列表内有重复"
    for i in list :
        if i['a']==t['a'] :
            return True
    return False