# (C) 2019-2020 lifegpc
# This file is part of bili.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
def downloadn(cid,r) :
    "下载当前弹幕"
    try :
        re=r.get('https://comment.bilibili.com/'+str(cid)+".xml")
    except :
        return -1
    re.encoding='utf8'
    return re.text
def downloadh(cid,r,date) :
    "下载历史弹幕"
    try :
        re=r.get('https://api.bilibili.com/x/v2/dm/history?type=1&date=%s&oid=%s' % (date,cid))
    except :
        return -1
    re.encoding='utf8'
    return re.text