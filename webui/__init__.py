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
from .range import getrange, checkrange, getcontentbyrange, DashRange
from .headers import getheader, getstatus, getcontenttype, mimetype, getacceptlanguage
from .template import gettemplate
from .loadsettings import loadset, getdfset, saveset
from .command import gopt
from file import getEtag, getlanEtag
from urllib.parse import urlencode, quote
import web
from .pas import passw
pa = passw()
from .section import sectionlist
sect = sectionlist()
from .section2 import logincheck, apilogincheck, logincheck2
from .index import index
from .translate import translate
from .js import js
from .css import css
from .settings import setting
from .json import jsong
from .login import login
from .font import font
from .video import video
from .favicon import favicon
from .about import about
