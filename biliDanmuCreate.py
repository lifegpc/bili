import cgi
def objtoxml(s) :
    try :
        return '<d p="%s,%s,%s,%s,%s,%s,%s,%s">%s</d>' % (s['ti'],s['mod'],s['fs'],s['fc'],s['ut'],s['dp'],s['si'],s['ri'],cgi.html.escape(s['t']))
    except :
        print('cgi库escape出错')
        exit()