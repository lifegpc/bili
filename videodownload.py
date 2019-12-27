#pylint:disable=W0612
import requests
import JSONParser
import json
import file
#https://api.bilibili.com/x/player/playurl?cid=<cid>&qn=<图质大小>&otype=json&avid=<avid>&fnver=0&fnval=16 番剧也可，但不支持4K
#https://api.bilibili.com/pgc/player/web/playurl?avid=<avid>&cid=<cid>&bvid=&qn=<图质大小>&type=&otype=json&ep_id=<epid>&fourk=1&fnver=0&fnval=16 貌似仅番剧
#result -> dash -> video/audio -> [0-?](list) -> baseUrl/base_url
#第二个需要带referer，可以解析4K
def avvideodownload(i,url,data,r) :
	"""下载av号视频
	-1 cookies.json读取错误"""
	r2=requests.Session()
	r2.headers=r.headers
	read=JSONParser.loadcookie(r2)
	if read!=0 :
		print("读取cookies.json出现错误")
		return -1
	r2.headers.update({'referer':url})
	uri="https://api.bilibili.com/x/player/playurl?cid=%s&qn=120&otype=json&avid=%s&fnver=0&fnval=16"%(data["page"][i-1]["cid"],data["aid"])
	re=r2.get(uri)
	re.encoding="utf8"
	re=re.json()
	print(re)
	if re["code"]!=0 :
		print({"code":re["code"],"message":re["message"]})
	if "data" in re:
		vq=re["data"]["quality"]
		vqd=re["data"]["accept_description"]
		avq=re["data"]["accept_quality"]
if __name__=="__main__" :
	print("请使用start.py")
