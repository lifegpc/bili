# (C) 2019-2020 lifegpc
# This file is part of bili.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from time import localtime,strftime
from biliTime import tostr2
from bstr import gettags
def printInfo(data) :
	"输出普通AV号获取的信息"
	print("视频av号："+str(data['aid']))
	print("视频bv号："+data['bvid'])
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
def printInfo2(data,ns:bool) :
	"未完成"
	if 'mediaInfo' in data and ns:
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
		print('发布时间：'+t['time'])
	ii=1
	if 'epList' in data:
		if ns:
			print('内容：')
		for i in data['epList'] :
			if not ns:
				ii=ii+1
				continue
			print(str(ii)+"、"+i['titleFormat'])
			ii=ii+1
			print('名字：'+i['longTitle'])
			print('AV号：'+str(i['aid']))
			print('BV号：'+str(i['bvid']))
			print('CID:'+str(i['cid']))
			print('ID:'+str(i['id']))
	if 'sections' in data:
		for i in data['sections'] :
			if ns:
				print(i['title']+":")
			for j in i['epList'] :
				if not ns:
					ii=ii+1
					continue
				print(str(ii)+"、"+j['titleFormat'])
				ii=ii+1
				print('名字：'+j['longTitle'])
				print('AV号：'+str(j['aid']))
				print('BV号：'+str(j['bvid']))
				print('CID:'+str(j['cid']))
				print('ID:'+str(j['id']))
	return ii-1
def printInfo3(d:dict) :
	print('收藏夹id：%s'%(d['id']))
	print('收藏夹名字：%s'%(d['title']))
	print('UP主名字：%s'%(d['author']))
	print('UID：%s'%(d['uid']))
	print('创建时间：%s'%(tostr2(d['ctime'])))
	print('修改时间：%s'%(tostr2(d['mtime'])))
	print('视频数量：%s'%(d['count']))
def printInfo4(l:list) :
	ii=1
	for i in l:
		print('视频%s：'%(ii))
		print('AV号：%s'%(i['id']))
		print('BV号：%s'%(i['bvid']))
		print('视频标题：%s'%(i['title']))
		print('UP主名称：%s'%(i['author']))
		print('收藏时间：%s'%(tostr2(i['ftime'])))
		ii=ii+1
def printInfo5(l:list) :
	e=1
	for i in l:
		print('%s、频道ID：%s'%(e,i['cid']))
		print('名字：%s'%(i['name']))
		print('介绍：%s'%(i['intro']))
		print('上次修改时间：%s'%(tostr2(i['mtime'])))
		print('视频数量：%s'%(i['count']))
		e=e+1
def printInfo6(l:list,d:dict) :
	print('频道ID：%s'%(d['cid']))
	print('名字：%s'%(d['name']))
	print('介绍：%s'%(d['intro']))
	print('上次修改时间：%s'%(tostr2(d['mtime'])))
	print('视频数量：%s'%(d['count']))
	e=1
	for i in l :
		print('视频%s：'%(e))
		print('AV号：%s'%(i['aid']))
		print('BV号：%s'%(i['bvid']))
		print('视频标题：%s'%(i['title']))
		e=e+1
def printInfo7(u:dict,l:list):
	print('UP主名字：%s'%(u['n']))
	print('UP主性别：%s'%(u['s']))
	print('UP主等级：%s'%(u['l']))
	print('个性签名：%s'%(u['sign']))
	print('生日：%s'%(u['b']))
	e=1
	for i in l:
		print('视频%s：'%(e))
		print('AV号：%s'%(i['aid']))
		print('BV号：%s'%(i['bvid']))
		print('视频标题：%s'%(i['title']))
		print('视频描述：%s'%(i['description']))
		print('创建时间：%s'%(tostr2(i['ctime'])))
		e=e+1
def printInfo8(d:dict) :
	k=1
	for i in d['data']['list'] :
		print('收藏夹%s：'%(k))
		print('收藏夹ID：%s'%(i['id']))
		print('收藏夹名字：%s'%(i['title']))
		k=k+1
def printInfo9(d:dict) :
	print('小视频ID：%s'%(d['id']))
	print('描述：%s'%(d['description']))
	print('标签：%s'%(gettags(d['tags'])))
	print('上传时间：%s'%(d['upload_time']))
	print('UP主名字：%s'%(d['name']))
	print('UID：%s'%(d['uid']))
def printcho(cho) :
	if len(cho)==0 :
		return
	print('你选中了',end='')
	for i in cho :
		print('%s,' %(i['titleFormat']),end='')
	print()
def pr() :
	print("""    bili  版权所有 (C) 2019-2020  lifegpc
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    本程序不负任何担保责任，欲知详情请键入'show w'。
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
    这是一个自由软件，欢迎您在特定条件下再发布本程序；欲知详情请键入'show c'。
    You can find the source code on <https://github.com/lifegpc/bili>.
    你可以在<https://github.com/lifegpc/bili>上找到源代码。
""")
def prc() :
	try :
		f=open("LICENSE","r",encoding="utf8")
		t=f.readline()
		while t :
			print(t)
			t=f.readline()
		f.close()
	except :
		print("Can't find GNU GPL3 LICENSE file, please see <http://www.gnu.org/licenses/>.")
		print("找不到GNU GPL3 LICENSE文件，请看<http://www.gnu.org/licenses/>。")
