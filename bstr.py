# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
def f(i:str):
    s=i.replace('\r','\\r')
    s=s.replace('\n','\\n')
    return s
