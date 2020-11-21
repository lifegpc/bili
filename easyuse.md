# 简单使用
这篇文章用来教萌新如何使用该软件   
对于大佬，可以看[README](README.md)

## 现已提供自带 windows版 python3.8.6 的压缩包/安装包
该版本可以在**win7**上正常使用，并且适用于32位或64位。（win7以上的系统当然也可以运行）  
去[RELEASE](../../releases)那下载```bili_x.x.x_windows_x64.7z```或```bili_x.x.x_windows_x86.7z```的文件解压运行start.bat即可。   
也可以选择下载exe版本(```bili_x.x.x_windows_x64.exe```或```bili_x.x.x_windows_x86.exe```)直接双击安装使用。

## 现已提供适用于windows10 64位系统的exe
去[RELEASE](../../releases)那下载bili_x.x.x_windows10_x64.7z的文件解压运行start.exe即可   
**建议先运行setsettings.exe以避免不必要的询问**

## 安装Python3
[下载](https://www.python.org/downloads/)Python安装包   
**安装时选中最下面的ADD Python X.X(版本号) to PATH**   
然后点Install NOW。

### pip3安装依赖库
打开命令提示符   
输入
``` bash
pip3 install --upgrade requests selenium rsa polib web.py regex iso-639
```
等待依赖库安装完毕

## 下载程序
去[RELEASE](../../releases)那下载程序  
对于**windows**用户，下载**bili_x.x_windows.7z**文件   
解压文件，双击里面的start.py   
如果出现请输入av号，说明程序可以正常使用
