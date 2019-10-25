from re import search
def Filter(s,l) :
	"过滤弹幕"
	for i in l :
		if i['e']=='true' :
			if i['t']=='t' :
				if s['t'].find(i['w'])>-1 :
					return True
			elif i['t']=='r' :
				if search(i['w'],s['t']) != None :
					return True
			elif i['t']=='u' :
				if i['w']==s['si'] :
					return True
	return False