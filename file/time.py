# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from time import strftime,localtime
def ttos(tm) :
    "将时间戳转换为字符串（当地时间）"
    if tm=='N/A':
        return 'N/A'
    elif tm>=0:
        return strftime('%Y-%m-%d %H:%M:%S',localtime(tm))
    else :
        return str(tm)