from time import localtime,strftime
def printInfo(data) :
	"输出普通AV号获取的信息"
	print("视频av号："+data['aid'])
	print("bvid："+data['bvid'])
	print("分P数："+str(data['videos']))
	print("标题："+data['title'])
	print("发布时间："+strftime("%Y-%m-%d %H:%M:%S",localtime(data['pubdate'])))
	print("上次修改时间："+strftime("%Y-%m-%d %H:%M:%S",localtime(data['ctime'])))
	print("描述："+data['desc'])
	print("UP主信息：")
	print("UID："+str(data['uid']))
	print("名字："+data['name'])
	print("分P信息：")
	for i in data['page'] :
		print("第"+str(i['page'])+"P：")
		print("CID："+str(i['cid']))
		print("分P名："+i['part'])
def printInfo2(data) :
	"未完成"
	if 'mediaInfo' in data :
		t=data['mediaInfo']
		print("ID："+str(t['id']))
		print("SSID："+str(t['ssId']))
		print("名字："+t['title'])
		if t['jpTitle']!='' : 
			print("日本语名字："+t['jpTitle'])
		if t['series']!='' :
			print("系列名字："+t['series'])
		if t['alias']!='' :
			print("别名："+t['alias'])
		print("简介："+t['evaluate'])
		print("类型："+t['type'])