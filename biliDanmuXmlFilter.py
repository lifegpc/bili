# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from re import search
def Filter(s,l) :
	"过滤弹幕"
	for i in l :
		if i['e']=='true' :
			if i['t']=='t' :
				if s['t'].find(i['w'])>-1 :
					return True
			elif i['t']=='r' :
				if search(i['w'],s['t']) != None :
					return True
			elif i['t']=='u' :
				if i['w']==s['si'] :
					return True
	return False