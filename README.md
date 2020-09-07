# BiliBili 弹幕/视频下载软件
- [BiliBili 弹幕/视频下载软件](#bilibili-弹幕视频下载软件)
  * [简介](#简介)
  * [依赖库](#依赖库)
    + [JavaScript依赖库](#javascript依赖库)
  * [配置文件](#配置文件)
    + [cookies.json](#cookiesjson)
    + [settings.json](#settingsjson)
    + [webui.json](#webuijson)
    + [sections.json](#sectionsjson)
    + [tv.bilibili.player.xml](#tvbilibiliplayerxml)
  * [开始使用](#开始使用)
    + [过滤弹幕](#过滤弹幕)
  * [翻译](#翻译)
  * [其他](#其他-1)
    + [全弹幕下载问题](#全弹幕下载问题)
  * [已知BUG](#已知bug)
    + [一直出现保存内容至文件失败或显示cgi库escape出错](#一直出现保存内容至文件失败或显示cgi库escape出错)
    + [登录时发生错误（使用ChromeDriver时）](#登录时发生错误使用chromedriver时)
  * [FAQ](#faq)
    + [无法输入密码](#无法输入密码)
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
[web.py](https://webpy.org/)  
自己写的file库   
如需自动合成视频，需要当前目录内或者环境变量PATH目录内有ffmpeg。   
如需使用aria2下载视频，需要当前目录内或者环境变量PATH目录内有aria2c。  
用户名密码登录部分参考了[Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit)的登录部分代码。  
识别Captcha使用了[该接口](https://bili.dev:2233/captcha)。
### JavaScript依赖库
[jQuery](https://jquery.com/)  
[js-sha256](https://github.com/emn178/js-sha256)  
[jsbn](http://www-cs-students.stanford.edu/~tjw/jsbn/)（注：已被合并到```webuihtml/js(origin)/rsa.js```）  
[js-base64](https://github.com/dankogai/js-base64)
## 配置文件
### cookies.json
该文件保存了登录B站后获取到的cookies信息，用于程序保持登录B站（调用历史弹幕接口用以及下载720P及以上视频使用）   

### settings.json
该文件保存了一些默认操作的设置，可以运行**setsettings.py**来设置。

### webui.json
保存了WEB用户界面的设置。

### sections.json
当WEB用户界面打开密码验证时，存储会话信息。

### tv.bilibili.player.xml
该文件不一定需要   
主要用来对弹幕进行过滤。   
可以直接将在PC网页端播放器的弹幕过滤设定中导出的文件放至程序目录下，并确保文件名为**tv.bilibili.player.xml**。

## 开始使用
直接运行start.py即可

### WEB用户界面
运行**startwebui.py**后，可以在浏览器访问。  
默认地址为```http://localhost:8080```。

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
现在已经支持用户名和密码登录。

## FAQ

### 无法输入密码
这是由于输入密码时关闭了输入内容在屏幕上输出（回显）导致的。  
解决方法是直接正常输入密码后按回车键即可。
