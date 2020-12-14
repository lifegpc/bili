[中文(中国)](README.md) [日本語](README.ja.md)
# BiliBili Barrage/Video Downloader
- [BiliBili Barrage/Video Downloader](#bilibili-barragevideo-downloader)
    * [Introduction](#introduction)
    * [Program Features](#program-features)
## Introduction
This program is written in Python (Python3), use some Python libraries and ChromeDriver. (When using ChromeDriver, it is more convenient to log in or pass captcha. The program's main features will not be affected if without ChromeDriver.)  
The program now supports the command line.  
If you want to build your own Release, you can find build script on [bili.build.bat](https://github.com/lifegpc/bili.build.bat).
## Program Features
- [x] [Download with aria2c](#download-with-aria2c)
- [x] [Merge separated videos automatically](#merge-separated-videos-automatically)
- [x] [mp4/mkv format](#mp4mkv-format)
- [x] [m4a format](#m4a-format)
- [x] [flac format](#flac-format)
- [ ] [mp3 format](#mp3-format)
### Download with aria2c
The program now supports downloading with aria2c. Download with aria2c is recommended, because aria2c provide faster download speed.  
If you want to enable this feature, make sure the program can call aria2c by using command line (You can simply put aria2c in program directory.). Also make sure enable this feature in the settings.
### Merge separated videos automatically
This feature needs ffmpeg.  
If you want to enable this feature, make sure the program can call ffmpeg by using command line (You can simply put ffmpeg in program directory.). Also make sure you have not **disabled** this feature in the settings.
### mp4/mkv format
You can select the video format you want in the settings.
### m4a format
The program supports downloading audio as m4a files.
### flac format
Some audios may have lossless quality, the program can save these formats as flac files.
### mp3 format
mp3 is not supported now. (Because the author don't want to transcode the audio file.)
