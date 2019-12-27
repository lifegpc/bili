def getcho(cho,data) :
    "将选中的数字转为相应信息"
    m=0
    if 'epList' in data :
        m=len(data['epList'])
    n=[]
    if 'sections' in data :
        for j in data['sections'] :
            n.append(len(j['epList']))
    re=[]
    for i in cho :
        if i <= m :
            #data['epList'][i-1]['i']=i
            data['epList'][i-1]['s']='e'
            re.append(data['epList'][i-1])
            continue
        r=m
        q=m
        for j in range(0,len(n)) :
            r=r+n[j]
            if i<=r :
                #data['sections'][j]['epList'][i-q-1]['i']=i
                data['sections'][j]['epList'][i-q-1]['s']='s'
                re.append(data['sections'][j]['epList'][i-q-1])
                break
            q=q+n[j]
    return re