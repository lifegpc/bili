# BiliBili 弹幕/视频下载软件
- [BiliBili 弹幕/视频下载软件](#bilibili-弹幕视频下载软件)
    * [简介](#简介)
    * [程序功能](#程序功能)
    * [依赖库](#依赖库)
        + [JavaScript依赖库](#javascript依赖库)
    * [配置文件](#配置文件)
        + [cookies.json](#cookiesjson)
        + [settings.json](#settingsjson)
        + [webui.json](#webuijson)
        + [sections.json](#sectionsjson)
        + [tv.bilibili.player.xml](#tvbilibiliplayerxml)
    * [开始使用](#开始使用)
        + [prepare.py](#preparepy)
        + [过滤弹幕](#过滤弹幕)
    * [翻译](#翻译)
    * [其他](#其他)
        + [全弹幕下载问题](#全弹幕下载问题)
    * [已知BUG](#已知bug)
        + [登录时发生错误（使用ChromeDriver时）](#登录时发生错误使用chromedriver时)
    * [FAQ](#faq)
        + [Release中每个文件的区别](#release中每个文件的区别)
        + [无法输入密码](#无法输入密码)
        + [大会员账号提示仅大会员可以观看](#大会员账号提示仅大会员可以观看)
        + [默认下载位置在哪](#默认下载位置在哪)
        + [要不要使用ffmpeg, arai2c](#要不要使用ffmpeg-arai2c)
        + [如何批量下载](#如何批量下载)
        + [闪退怎么办](#闪退怎么办)
        + [aria2c的几个下载设置是什么意思](#aria2c的几个下载设置是什么意思)
## 简介
程序用python(python3)语言编写而成，使用了部分python库和ChromeDriver（有ChromeDriver在登录和解决验证码时较方便，对主要功能不影响）。   
软件只有控制台界面，萌新不会可以看[这里](easyuse.md)   
现在已支持命令行  
RELEASE构建脚本见[bili.build.bat](https://github.com/lifegpc/bili.build.bat)。
## 程序功能
- [x] [使用aria2c下载](#使用aria2c下载)
- [x] [自动合并分离的视频](#自动合并分离的视频)
- [x] [mp4和mkv格式](#mp4和mkv格式)
- [x] [m4a格式](#m4a格式)
- [x] [flac格式](#flac格式)
- [ ] [mp3格式](#mp3格式)
- [x] [普通AV/BV号视频](#普通avbv号视频)
    * [x] 弹幕下载
    * [x] 全弹幕（历史弹幕）下载
    * [x] 视频下载
    * [x] [仅下载音频](#仅下载音频)
    * [x] 仅下载封面
    * [x] 仅下载字幕
    * [x] 4K和HDR
    * [x] 互动视频解析
- [x] [番剧](#番剧)
    * [x] 弹幕下载
    * [x] 全弹幕（历史弹幕）下载
    * [x] 视频下载
    * [x] [仅下载音频](#仅下载音频-1)
    * [x] [仅下载封面](#仅下载封面)
    * [x] 4K
    * [ ] HDR（可能支持，目前没有可测试的视频）
- [x] [已购买课程](#已购买课程)
    * 与番剧几乎相同
    * [仅下载封面](#仅下载封面-1)
- [x] [已购买课程列表](#已购买课程列表)
- [x] [收藏夹](#收藏夹)
    * [支持的GET参数](#支持的get参数)
- [x] [频道列表](#频道列表)
- [x] [频道](#频道)
    * [支持的GET参数](#支持的get参数-1)
- [x] [投稿视频列表](#投稿视频列表)
    * [支持的GET参数](#支持的get参数-2)
- [x] [直播回放](#直播回放)
    * [x] [视频下载](#视频下载)
    * [x] [弹幕下载](#弹幕下载)
- [x] [直播](#直播)
    * [x] [视频下载](#视频下载-1)
- [x] [AU号音频](#au号音频)
    * [x] [音频下载](#音频下载)
    * [x] [仅下载歌词](#仅下载歌词)
    * [x] 仅下载封面
### 使用aria2c下载
本程序支持使用aria2c下载并推荐使用aria2c下载已获得更好的下载体验。  
启用该功能需要确保能够直接命令行调用aria2c（一般而言放在程序目录即可）并确保在设置里已启用使用aria2c。
### 自动合并分离的视频
本程序使用ffmpeg来自动合并分离的视频。  
启用该功能需要确保能够直接命令行调用ffmpeg（一般而言放在程序目录即可）并确保在设置里没有**禁用**ffmpeg。
### mp4和mkv格式
本程序支持合并为mp4文件或mkv文件，设置中可以选择视频格式。
### m4a格式
本程序支持直接下载音频文件为m4a文件。
### flac格式
部分音频含有无损音质，可以保存为flac文件。
### mp3格式
本程序暂不支持mp3格式。（因为不想转码）
### 普通AV/BV号视频
本程序支持以下的输入（以AV9为例，忽略大小写）：
- ```9```
- ```av9```
- ```BV1xx411c7mC```
- ```bilibili.com/video/av9``` （前面的```https:\\```,```www.```等内容可以加可以不加，后同）
- ```bilibili.com/video/BV1xx411c7mC```
- ```b23.tv/av9```
- ```b23.tv/BV1xx411c7mC```
- ```bilibili.com/s/video/av9```
- ```bilibili.com/s/video/BV1xx411c7mC```

如果视频指向的是番剧，将会自动重定向到番剧。
#### 仅下载音频
目前只支持DASH流的解析结果。（目前只有极个别的解析结果不是DASH。）
### 番剧
本程序支持以下的输入（以SS26291为例，忽略大小写）：
- ```ss26291```
- ```ep259653```
- ```md4316442```
- ```bilibili.com/bangumi/play/ss26291```
- ```bilibili.com/bangumi/play/ep259653```
- ```bilibili.com/bangumi/media/md4316442```
- ```b23.tv/ss26291```
- ```b23.tv/ep259653```
- ```40240711```等AV/BV号视频输入

如果根据现有的SS或EP号找不到内容，将会尝试使用相同的SS和EP号去访问已购买课程。
#### 仅下载音频
目前只支持DASH流的解析结果。
#### 仅下载封面
在下载当前话的封面时，会自动下载整个番剧的封面。
### 已购买课程
本程序支持以下的输入（以SS150为例，忽略大小写）：
- ```bilibili.com/cheese/play/ss150```
- ```bilibili.com/cheese/play/ep2425```
#### 仅下载封面
不会下载当前话的封面，而是下载整个课程的封面以及介绍图。
### 已购买课程列表
本程序支持以下的输入：
- ```bilibili.com/cheese/mine/list```
- ```bilibili.com/v/cheese/mine/list```

会将所有已购买课程解析出来以供选择需要下载的课程。
### 收藏夹
本程序支持以下的输入（以UID1为例）：
- ```space.bilibili.com/1/favlist```
#### 支持的GET参数
- ```fid```：用来指定是哪一个收藏夹
- ```keyword```：用来搜索收藏夹
- ```type```：指定是搜索全部收藏夹还是当前收藏夹。0为当前收藏夹，1为全部收藏夹。
- ```tid```：用来指定是哪个分区，全部分区是0。可以使用```--ltid```命令行参数来获得当前收藏夹所有可用的tid。
- ```order```：指定投稿视频列表排序。```mtime```为最近收藏，```view```为最多播放，```pubtime```为最新投稿。

会将所有收藏夹内的视频解析出来以供选择需要下载的视频。
### 频道列表
本程序支持以下的输入（以UID1为例）：
- ```space.bilibili.com/1/channel/index```

会将一个UP主的所有频道解析出来以供选择需要下载的频道。
### 频道
本程序支持以下的输入（以UID928123为例）：
- ```space.bilibili.com/928123/channel/detail?cid=42271```
#### 支持的GET参数
- ```cid```：用来指明是哪个频道（必须带有cid才能进行解析）
- ```order```：指明视频排序顺序，0为默认排序，1为倒序排序。

会将一个频道的所有视频解析出来以供选择需要下载的视频。
### 投稿视频列表
本程序支持以下的输入（以UID1为例）：
- ```space.bilibili.com/1/video```
- ```bilibili.com/medialist/play/225910184```
#### 支持的GET参数
- ```tid```：用来指明视频类型
- ```keyword```：用来搜索投稿视频列表
- ```order```：指定投稿视频列表排序。```pubdate```为最新发布，```click```为最多播放，```stow```为最多收藏。

会将一个UP主的所有投稿视频解析出来以供选择需要下载的频道。
### 直播回放
本程序支持以下的输入（以R1mx411c7En为例）：
- ```live.bilibili.com/record/R1mx411c7En```
#### 视频下载
目前只支持下载原画，如果出现其他画质，下载器应该会有提示，请将视频链接提交至[issues](https://github.com/lifegpc/bili/issues)。
#### 弹幕下载
目前只支持普通类型的弹幕，礼物等不支持。弹幕将会由原始格式转换为XML格式。
### 直播
本程序支持以下的输入（以房间号1为例）：
- ```live.bilibili.com/1```
#### 视频下载
支持多种画质选择。支持选择主线和备线（需要使用命令行）。
### AU号音频
本程序支持以下的输入（以AU1为例）：
- ```au1```
- ```bilibili.com/audio/au1```
- ```b23.tv/au1```
#### 音频下载
~~目前只支持下载默认音质，如果有出现其他音质，下载器应该会有提示，请将AU号提交至[issues](https://github.com/lifegpc/bili/issues)。~~ 现已支持多种音质，且用且珍惜。  
如果音频有关联的普通视频，将会尝试从关联的视频页获取更多的音质。
#### 仅下载歌词
程序默认会对下载的歌词文件进行过滤修正，从而以适应更多的播放器。  
如果音频有关联的普通视频，将会尝试从关联的视频页获取更多的歌词（即字幕）。
## 依赖库
[requests](https://pypi.org/project/requests/)   
[selenium](https://pypi.org/project/selenium/)  
[rsa](https://pypi.org/project/rsa/)  
[polib](https://pypi.org/project/polib/)  
[web.py](https://webpy.org/)  
[regex](https://pypi.org/project/regex/)  
[iso-639](https://pypi.org/project/iso-639/)  
自己写的file库   
如需自动合成视频，需要当前目录内或者环境变量PATH目录内有ffmpeg。   
如需使用aria2下载视频，需要当前目录内或者环境变量PATH目录内有aria2c。  
用户名密码登录部分参考了[Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit)的登录部分代码。  
~~识别Captcha使用了[该接口](https://bili.dev:2233/captcha)。~~（接口已挂）
### JavaScript依赖库
[jQuery](https://jquery.com/)  
[js-sha256](https://github.com/emn178/js-sha256)  
[jsbn](http://www-cs-students.stanford.edu/~tjw/jsbn/)（注：已被合并到```webuihtml/js(origin)/rsa.js```）  
[js-base64](https://github.com/dankogai/js-base64)  
[QRCode.js](https://github.com/davidshimjs/qrcodejs)  
[Viewer.js](https://github.com/fengyuanchen/viewerjs)  
[clipboard.js](https://github.com/zenorocha/clipboard.js)  
[FileSaver.js](https://github.com/eligrey/FileSaver.js)
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

### prepare.py
运行后可以取得运行WEB用户界面必须的一些文件。  
运行时确保可以直接访问```java```。  
~~由于死🐴的Cloudflare的防BOT检测，现在已经无法自动更新/下载```compiler.jar```，请去[这里](https://mvnrepository.com/artifact/com.google.javascript/closure-compiler/latest)下载```compiler.jar```，没有该文件将无法进行编译。~~（貌似目前没有防BOT检测）

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
### 登录时发生错误（使用ChromeDriver时）
这是由于你的电脑未安装Chrome或者Chrome版本与Chrome Driver版本不一致导致的，请安装Chrome或下载匹配Chrome版本的Chrome Driver。  
**可以到这里[下载](https://chromedriver.chromium.org/downloads)Chrome Driver的其他版本**  
具体的错误提示可以参考[#9](https://github.com/lifegpc/bili/issues/9)和[#11](https://github.com/lifegpc/bili/issues/11)。  
现在已经支持用户名和密码登录。

## FAQ

### Release中每个文件的区别
- ```bili_版本.7z``` 最简单的版本，需要自己下载/安装aria2c, chromedriver, ffmpeg, Python3.6+
- ```bili_版本_linux.7z``` 最简单的版本加上Linux版的chromedriver
- ```bili_版本_mac.7z``` 最简单的版本加上Mac版的chromedriver
- ```bili_版本_windows.7z``` 最简单的版本加上Windows版的chromedriver
- ```bili_版本_windows10_x64.7z``` 编译成exe的版本，可以直接在64位Windows10上运行。自带aria2c, chromedriver, ffmpeg
- ```bili_版本_windows10_x64.exe``` ```bili_版本_windows10_x64.7z```的安装包版本
- ```bili_版本_windows_x64.7z``` 自带Python3.8.6, aria2c, chromedriver, ffmpeg，双击bat文件即可直接在windows7及以上的64位系统中运行
- ```bili_版本_windows_x64.exe``` ```bili_版本_windows_x64.7z```的安装包版本
- ```bili_版本_windows_x86.7z``` 自带Python3.8.6, aria2c, chromedriver, ffmpeg，双击bat文件即可直接在windows7及以上的32位系统中运行
- ```bili_版本_windows_x86.exe``` ```bili_版本_windows_x86.7z```的安装包版本

建议选择后4个版本。

### 无法输入密码
这是由于输入密码时关闭了输入内容在屏幕上输出（回显）导致的。  
解决方法是直接正常输入密码后按回车键即可。

### 大会员账号提示仅大会员可以观看
先删除```cookies.json```，然后使用Chrome Driver登录，不要使用WEB UI登录。（WEB UI登录目前存在BUG）

### 默认下载位置在哪
默认下载位置在程序所在目录下的```Download```文件夹。  
如果使用安装包安装的话，程序所在目录默认在```%appdata%/bili```或```%appdata%/bili x86```或```%appdata%/bili x64```。

### 要不要使用ffmpeg, arai2c
建议都使用。  
ffmpeg是用来自动合并分离的视频的。  
aria2c可以极大地改善下载的体验。

### 如何批量下载
目前可以使用,隔开多个输入，也可以采用收藏夹等方式批量下载。  
批量下载时建议配合命令行使用。（命令行的基础知识请自己搜索）  
例如每次都选择下载方法4，可以使用```py start.py -d4```。  
更多的命令行指令可以采用```py start.py -h```查看。

### 闪退怎么办
目前除了windows_x64和windows_x86的batch脚本外，另外的版本都会在运行完毕后直接退出（无论程序是否出现错误）。  
如果是主程序，可以在设置里启用写入日志到文件，然后去程序所在目录下的```log```文件夹寻找日志。如果出现错误，你可以在最后面看到错误的具体信息。

### aria2c的几个下载设置是什么意思
aria2c是一个多线程下载工具。  
多线程下载简单理解就是把1个文件分成n部分，每一部分同时下载。  
同时下载的部分数越多，一般速度也就越快。  
有关aria2c的设置：  
是否启用aria2c：建议是，使用aria2c可以提供更好的下载体验（下载速度快）  
使用aria2c时单个服务器最大连接数和单个文件最大连接数：这两者共同来限制最多能有多少部分能够同时下载。因此调大这两者可以增加同时下载的部分数，从而使速度加快。  
使用aria2c时文件分片大小：aria2c是根据文件分片大小来将1个文件分成n部分。假设有1个100M的文件，文件分片大小是20M，因此这个文件将会被分成5部分。当文件大小不足文件分片大小的2倍时，这个文件将不会被分成n部分，而是当作一个整体下载。调小这个可以时文件被分成的部分数加多，一定程度上可以加快速度。  
注：如果出现0b/s的情况，说明暂时被BiliBili CDN封禁，请适当调整上述参数以降低同时下载的部分数。  
在使用aria2c下载时使用备用网址：建议开着，这样可以同时从多个CDN服务器下载内容，加快下载速度。  
使用aria2c下载时文件预分配方式：这个一般建议保持默认值。  
在使用aria2c时最大总体速度(B/s)：这个根据个人需求设置吧。
