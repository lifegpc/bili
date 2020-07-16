# BiliBili 弹幕/视频下载软件
- [BiliBili 弹幕/视频下载软件](#bilibili-弹幕视频下载软件)
  * [简介](#简介)
  * [依赖库](#依赖库)
    + [其他](#其他)
  * [配置文件](#配置文件)
    + [cookies.json](#cookiesjson)
    + [settings.json](#settingsjson)
    + [tv.bilibili.player.xml](#tvbilibiliplayerxml)
  * [开始使用](#开始使用)
    + [过滤弹幕](#过滤弹幕)
  * [翻译](#翻译)
  * [其他](#其他-1)
    + [全弹幕下载问题](#全弹幕下载问题)
  * [已知BUG](#已知bug)
    + [一直出现保存内容至文件失败或显示cgi库escape出错](#一直出现保存内容至文件失败或显示cgi库escape出错)
    + [登录时发生错误（使用ChromeDriver时）](#登录时发生错误使用chromedriver时)
## 简介
程序用python(python3)语言编写而成，使用了部分python库和ChromeDriver。   
软件只有控制台界面，萌新不会可以看[这里](easyuse.md)   
现在已支持命令行  
RELEASE构建脚本见[bili.build.bat](https://github.com/lifegpc/bili.build.bat)。
## 依赖库
[requests](https://pypi.org/project/requests/)   
[selenium](https://pypi.org/project/selenium/)  
[rsa](https://pypi.org/project/rsa/)  
[polib](https://pypi.org/project/polib/)  
自己写的file库   
如需自动合成视频，需要当前目录内或者环境变量PATH目录内有ffmpeg。   
如需使用aria2下载视频，需要当前目录内或者环境变量PATH目录内有aria2c。  
用户名密码登录部分参考了[Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit)的登录部分代码。  
识别Captcha使用了[该接口](https://bili.dev:2233/captcha)。
### 其他
程序目录下需要有相应系统版本的ChromeDriver。   
~~没有ChromeDriver将无法进行登录操作（同理，由于手机平台没有ChromeDriver，也无法进行登录，但可以用[其他方法](#a)绕过）~~
## 配置文件
### cookies.json
该文件保存了登录B站后获取到的cookies信息，用于程序保持登录B站（调用历史弹幕接口用以及下载720P及以上视频使用）   
<a name='a'></a>**~~当某些平台无法登录时，可以在其他平台先登录，再将cookies.json复制到程序目录下。~~**  
现在已经支持用户名和密码登录。

### settings.json
该文件保存了一些默认操作的设置，可以运行**setsettings.py**来设置。

### tv.bilibili.player.xml
该文件不一定需要   
主要用来对弹幕进行过滤。   
可以直接将在PC网页端播放器的弹幕过滤设定中导出的文件放至程序目录下，并确保文件名为**tv.bilibili.player.xml**。

## 开始使用
直接运行start.py即可

### 过滤弹幕
运行filter.py即可   
注意：必须要有**tv.bilibili.player.xml**文件才能进行弹幕过滤。

## 翻译
你可以在[Transifex](https://www.transifex.com/lifegpc/bili/)上为该程序提供翻译。  
感谢Kum4423提供日语翻译。

## 其他
完美支持**普通视频**的弹幕下载   
现已支持**SS号（番剧）**的普通弹幕和全弹幕下载，但全弹幕下载**开始时间**[可能](#b)需要**手动调整**（目前暂未发现每1P的具体时间戳）   
**全弹幕下载建议使用自动模式，不建议自己输入间隔天数**   
<a name='b'></a>注：第1P一般是准确的。

### 全弹幕下载问题
由于B站限制了历史弹幕的调用次数，大概12h内可以调用1000次左右，所以在弹幕较多的时候请设定较大的时间间隔。   
被限制后大约12h后会恢复正常

## 已知BUG

### 一直出现保存内容至文件失败或显示cgi库escape出错
全弹幕下载一直出现**保存内容至文件失败**或显示**cgi库escape出错**   
原因：  
**BiliDanmuCreate.py**下cgi没有正确引用**escape()**   
低版本python可以使用cgi.escape()而高版本可以使用cgi.html.escape()

### 登录时发生错误（使用ChromeDriver时）
这是由于你的电脑未安装Chrome或者Chrome版本与Chrome Driver版本不一致导致的，请安装Chrome或下载匹配Chrome版本的Chrome Driver。  
**可以到这里[下载](https://chromedriver.chromium.org/downloads)Chrome Driver的其他版本**  
具体的错误提示可以参考[#9](https://github.com/lifegpc/bili/issues/9)和[#11](https://github.com/lifegpc/bili/issues/11)。
