from file.info import getinfo,getinfox,printinfo
from file.dir import getinfod,printinfod,listd
from file.filter import listf,listfd,listff
#对后缀名过滤
LX_FILTER=0
#对文件名进行正则过滤
TEXT_FILTER=1
#对后缀名进行过滤时，保留无后缀名名文件
ILX_FILTER=2