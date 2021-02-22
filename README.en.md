[中文(中国)](README.md) [日本語](README.ja.md)
# BiliBili Barrage/Video Downloader
- [BiliBili Barrage/Video Downloader](#bilibili-barragevideo-downloader)
    * [Introduction](#introduction)
    * [Program Features](#program-features)
    * [Dependent Libraries](#dependent-libraries)
        + [JavaScript Dependent Libraries](#javascript-dependent-libraries)
    * [Configuration Files](#configuration-files)
        + [cookies.json](#cookiesjson)
        + [settings.json](#settingsjson)
        + [webui.json](#webuijson)
        + [sections.json](#sectionsjson)
        + [tv.bilibili.player.xml](#tvbilibiliplayerxml)
## Introduction
This program is written in Python (Python3), use some Python libraries and ChromeDriver. (When using ChromeDriver, it is more convenient to log in or pass captcha. The program's main features will not be affected if without ChromeDriver.)  
The program now supports the command line.  
If you want to build your own Release, you can find build script on [bili.build.bat](https://github.com/lifegpc/bili.build.bat).  
All Release are signatured with [GPG](https://gnupg.org/).  
<details>
<summary>Public Key</summary>
<p>

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
=DTeS
-----END PGP PUBLIC KEY BLOCK-----
```

</p>
</details>

## Program Features
- [x] [Download with aria2c](#download-with-aria2c)
- [x] [Merge Separated Videos Automatically](#merge-separated-videos-automatically)
- [x] [mp4/mkv Format](#mp4mkv-format)
- [x] [m4a Format](#m4a-format)
- [x] [flac Format](#flac-format)
- [ ] [mp3 Format](#mp3-format)
- [x] [Normal AV/BV Number Video](#normal-avbv-number-video)
    * [x] Download Barrage
    * [x] Download All Barrage form Historical Records
    * [x] Download Video
    * [x] [Only Download Audio](#only-download-audio)
    * [x] Only Download Cover
    * [x] Only Download Subtitles
    * [x] 4K and HDR
    * [x] Parse Interactive Video
- [x] [Bangumi Video](#bangumi-video)
    * [x] Download Barrage
    * [x] Download All Barrage form Historical Records
    * [x] Download Video
    * [x] [Only Download Audio](#only-download-audio-1)
    * [x] [Only Download Cover](#only-download-cover)
    * [x] 4K
    * [ ] HDR (May support, the author can't find test video)
- [x] [Purchased Courses](#purchased-courses)
	* Almost same as [Bangumi Video](#bangumi-video).
	* [x] [Only Download Cover](#only-download-cover-1)
- [x] [Purchased Courses List](#purchased-courses-list)
- [x] [Favorites](#favorites)
	* [x] [Supported GET Parameters](#supported-get-parameters)
- [x] [Channel List](#channel-list)
- [x] [Channel](#channel)
    * [x] [Supported GET Parameters](#supported-get-parameters-1)
- [x] [Uploaded Video List](#uploaded-video-list)
    * [x] [Supported GET Parameters](#supported-get-parameters-2)
- [x] [Live Record](#live-record)
    * [x] [Download Video](#download-video)
    * [x] [Download Barrage](#download-barrage)
- [x] [Live](#live)
    * [x] [Download Video](#download-video-1)
- [x] [AU Number Audio](#au-number-audio)
    * [x] [Download Audio](#download-audio)
    * [x] [Only Download Lyrics](#only-download-lyrics)
    * [x] Only Download Cover
- [x] [Songs List](#songs-list)
### Download with aria2c
The program now supports downloading with aria2c. Download with aria2c is recommended, because aria2c provide faster download speed.  
If you want to enable this feature, make sure the program can call aria2c by using command line (You can simply put aria2c in program directory.). Also make sure enable this feature in the settings.
### Merge Separated Videos Automatically
This feature needs ffmpeg.  
If you want to enable this feature, make sure the program can call ffmpeg by using command line (You can simply put ffmpeg in program directory.). Also make sure you have not **disabled** this feature in the settings.
### mp4/mkv Format
You can select the video format you want in the settings.
### m4a Format
The program supports downloading audio as m4a files.
### flac Format
Some audios may have lossless quality, the program can save these formats as flac files.
### mp3 Format
mp3 is not supported now. (Because the author don't want to transcode the audio file.)
### Normal AV/BV Number Video
This program supports following input format (Take av9 for example. The program ignores case.):
- ```9```
- ```av9```
- ```BV1xx411c7mC```
- ```bilibili.com/video/av9``` (The former ```https://```, ```www.``` will be ignored.)
- ```bilibili.com/video/BV1xx411c7mC```
- ```b23.tv/av9```
- ```b23.tv/BV1xx411c7mC```
- ```bilibili.com/s/video/av9```
- ```bilibili.com/s/video/BV1xx411c7mC```
- ```bilibili.com/festival/2021bnj?bvid=BV1j5411n7s9```

If the video is an episode of Bangumi, the program will redirect it to [Bangumi video](#bangumi-video). 
#### Only Download Audio
Only supports DASH stream video. (Most videos are DASH streams now.)
### Bangumi Video
This program supports following input format (Take SS26291 for example. The program ignores case.):
- ```ss26291```
- ```ep259653```
- ```md4316442```
- ```bilibili.com/bangumi/play/ss26291```
- ```bilibili.com/bangumi/play/ep259653```
- ```bilibili.com/bangumi/media/md4316442```
- ```b23.tv/ss26291```
- ```b23.tv/ep259653```
- ```40240711``` and so on (Input as [Normal AV/BV Number Video](#normal-avbv-number-video).)

If the program can't find this season, it will be redirected to [Purchased Courses](#purchased-courses).
#### Only Download Audio
Only supports DASH stream video.
#### Only Download Cover
When downloading an episode's cover of a season, the season's cover will also be downloaded.
### Purchased Courses
This program supports following input format (Take SS150 for example. The program ignores case.):
- ```bilibili.com/cheese/play/ss150```
- ```bilibili.com/cheese/play/ep2425```
#### Only Download Cover
This feature can't download current episode's cover. But it can download courses' cover and description image.
### Purchased Courses List
This program supports following input format:
- ```bilibili.com/cheese/mine/list```
- ```bilibili.com/v/cheese/mine/list```

This feature can get a list of all purchased courses and let you select courses you want to download.
### Favorites
This program supports following input format (Take UID1 for example.):
- ```space.bilibili.com/1/favlist```

This feature can get a list of videos from Favorites and let you select videos you want to download.
#### Supported GET Parameters
- ```fid```: to specify which Favorites you want to parse
- ```keyword```: the keyword if you want to search in Favorites
- ```type```: to specify the search range. 0 is current Favorites, 1 is all Favorites.
- ```tid```: to specify the video type, 0 is all types. You can use ```--ltid```(command line parameter) to get all available tid for current Favorites.
- ```order```: to specify video's order. ```mtime``` is added time, ```view``` is views, ```pubtime``` is publish time.
### Channel List
This program supports following input format (Take UID1 for example.):
- ```space.bilibili.com/1/channel/index```

This feature can get a list of channels and let you select the channel you want to download.
### Channel
This program supports following input format (Take UID928123 for example.):
- ```space.bilibili.com/928123/channel/detail?cid=42271```
#### Supported GET Parameters
- ```cid```: to specify the channel (Must have this parameter).
- ```order```: to specify the order of videos. 0 is default order, 1 is reverse order.

This feature can get a list of videos from the channel and let you select videos you want to download.
### Uploaded Video List
This program supports following input format (Take UID1 for example.):
- ```space.bilibili.com/1/video```
- ```bilibili.com/medialist/play/225910184```
#### Supported GET Parameters
- ```tid```: to specify the video type, 0 is all types. You can use ```--ltid```(command line parameter) to get all available tid for current uploaded video list.
- ```keyword```: the keyword if you want to search in uploaded video list
- ```order```: to specify video's order. ```pubdate``` is publish time, ```click``` is views, ```stow``` is favorited times.

This feature can get a list of videos from a uploader's uploaded video list and let you select videos you want to download.
### Live Record
This program supports following input format (Take R1mx411c7En for example.):
- ```live.bilibili.com/record/R1mx411c7En```
#### Download Video
This feature now only support the default video format (origin quality). If a live record have other video formats, you can see the warning in downloader. If you see that warning, please submit an [issue](https://github.com/lifegpc/bili/issues).
#### Download Barrage
This feature now only support normal barrage. The barrage file will be converted from the original format to XML format.
### Live
This program supports following input format (Take ROOMID1 for example.):
- ```live.bilibili.com/1```
#### Download Video
This feature supports selecting the video quality. You can also select the URL by using command line.
### AU Number Audio
This program supports following input format (Take AU1 for example.):
- ```au1```
- ```bilibili.com/audio/au1```
- ```b23.tv/au1```
#### Download Audio
Now support multiply audio quality.  
If the audio has the related video, the program will try to get more audio formats from the related video.
#### Only Download Lyrics
The program will standardize lyrics by default. After standardizing, the lyrics can be adapted to more audio players.  
If the audio has the related video, the program will try to get more lyrics(subtitles) from the related video.
### Songs List
This program supports following input format (Take AM29931432 for example.):
- ```am29931432```
- ```bilibili.com/audio/am29931432```
- ```bilibili.com/audio/mycollection/29981833```
## Dependent Libraries
[requests](https://pypi.org/project/requests/)   
[selenium](https://pypi.org/project/selenium/)  
[rsa](https://pypi.org/project/rsa/)  
[polib](https://pypi.org/project/polib/)  
[web.py](https://webpy.org/)  
[regex](https://pypi.org/project/regex/)  
[iso-639](https://pypi.org/project/iso-639/)  
[pywin32](https://pypi.org/project/pywin32/)  
[qrcode](https://github.com/lincolnloop/python-qrcode)  
The login part refers to the login part of [Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit).
### JavaScript Dependent Libraries
[jQuery](https://jquery.com/)  
[js-sha256](https://github.com/emn178/js-sha256)  
[jsbn](http://www-cs-students.stanford.edu/~tjw/jsbn/) (PS. It has been merged into [```webuihtml/js(origin)/rsa.js```](webuihtml/js(origin)/rsa.js).)  
[js-base64](https://github.com/dankogai/js-base64)  
[QRCode.js](https://github.com/davidshimjs/qrcodejs)  
[Viewer.js](https://github.com/fengyuanchen/viewerjs)  
[clipboard.js](https://github.com/zenorocha/clipboard.js)  
[FileSaver.js](https://github.com/eligrey/FileSaver.js)
## Configuration Files
### cookies.json
This file including the cookies information, which is used by the program to keep logging in.

### settings.json
This file including some settings. You can run ```setsettings.py``` to configure.

### webui.json
This file including the settings for WEB User Interface.

### sections.json
This file including the section information for WEB User Interface if you enable password verification.

### tv.bilibili.player.xml
This file including the filter rules for barrages.  
You can export this file from bilibili WEB player.
