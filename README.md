# BiliBili 弹幕下载软件
## 简介
程序用python(python3)语言编写而成，使用了部分python库和ChromeDriver。   
软件只有控制台界面，萌新不会可以看[这里](easyuse.md)
## 依赖库
[requests](https://pypi.org/project/requests/)   
[selenium](https://pypi.org/project/selenium/)   
自己写的file库   
### 其他
程序目录下需要有相应系统版本的ChromeDriver。   
没有ChromeDriver将无法进行登录操作（同理，由于手机平台没有ChromeDriver，也无法进行登录，但可以用[其他方法](#a)绕过）
## 配置文件
### cookies.json
该文件保存了登录B站后获取到的cookies信息，用于程序保持登录B站（调用历史弹幕接口用）   
<a name='a'></a>**当某些平台无法登录时，可以在其他平台先登录，再将cookies.json复制到程序目录下。**

### tv.bilibili.player.xml
该文件不一定需要   
主要用来对弹幕进行过滤。   
可以直接将在PC网页端播放器的弹幕过滤设定中导出的文件放至程序目录下，并确保文件名为**tv.bilibili.player.xml**。

## 开始使用
直接运行start.py即可

### 过滤弹幕
运行filter.py即可   
注意：必须要有**tv.bilibili.player.xml**文件才能进行弹幕过滤。

## 其他
完美支持**普通视频**的弹幕下载   
现已支持**SS号（番剧）**的普通弹幕和全弹幕下载，但全弹幕下载**开始时间**[可能](#b)需要**手动调整**（目前暂未发现每1P的具体时间戳）   
**全弹幕下载建议使用自动模式，不建议自己输入间隔天数**   
<a name='b'></a>注：第1P一般是准确的。

## 已知BUG

### 一直出现保存内容至文件失败或显示cgi库escape出错
全弹幕下载一直出现**保存内容至文件失败**或显示**cgi库escape出错**   
原因：  
**BiliDanmuCreate.py**下cgi没有正确引用**escape()**   
低版本python可以使用cgi.escape()而高版本可以使用cgi.html.escape()