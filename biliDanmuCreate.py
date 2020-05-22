# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import cgi
def objtoxml(s) :
    try :
        return '<d p="%s,%s,%s,%s,%s,%s,%s,%s">%s</d>' % (s['ti'],s['mod'],s['fs'],s['fc'],s['ut'],s['dp'],s['si'],s['ri'],cgi.html.escape(s['t']))
    except :
        print('cgi库escape出错')
        exit()