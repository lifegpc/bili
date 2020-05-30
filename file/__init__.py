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
from file.info import getinfo,getinfox,printinfo,spfn,spfln
from file.dir import getinfod,printinfod,listd
from file.filter import listf,listfd,listff,filtern,filterd
from file.get import getfilen
from file.info import geturlfe
from file.str import cml
from file.md import mkdir
#对后缀名过滤
LX_FILTER=0
#对文件名进行正则过滤
TEXT_FILTER=1
#对后缀名进行过滤时，保留无后缀名名文件
ILX_FILTER=2