from requests.structures import CaseInsensitiveDict
def copydict(x) :
    if isinstance(x,dict):
        r={}
    elif isinstance(x,CaseInsensitiveDict) :
        r=CaseInsensitiveDict()
    else :
        return {}
    for i in x.keys() :
        t=x[i]
        if isinstance(t,(dict,CaseInsensitiveDict)) :
            r[i]=copydict(t)
        elif isinstance(t,list) :
            r[i]=copylist(t)
        else :
            r[i]=t
    return r
def copylist(x) :
    r=[]
    for i in x :
        if isinstance(i,(dict,CaseInsensitiveDict)) :
            r.append(copydict(i))
        elif isinstance(i,list) :
            r.append(copylist(i))
        else :
            r.append(i)
    return r
