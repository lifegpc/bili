# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from file.info import getinfo,getinfox,printinfo,spfn
from file.dir import getinfod,printinfod,listd
from file.filter import listf,listfd,listff,filtern
from file.get import getfilen
from file.info import geturlfe
from file.str import cml
#对后缀名过滤
LX_FILTER=0
#对文件名进行正则过滤
TEXT_FILTER=1
#对后缀名进行过滤时，保留无后缀名名文件
ILX_FILTER=2