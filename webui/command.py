# (C) 2019-2020 lifegpc
# This file is part of bili.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from getopt import getopt
from lang import getdict, getlan, lan
from . import loadset
from hashl import sha256
from sys import exit


def ph():
    h = f'''{la['O1']}
    startwebui.py -h/-?/--help   {la['O2']}
    startwebui.py [--lan <LANGUAGECODE>] [-s/--host <IP>] [-p/--port <PORT>] [--sslc <PATH> --sslp <PATH>] [--sslcc <PATH>] [--pas <PASSWORD>]
    --lan <LANGUAGECODE>    {la['O3']}
    -s/--host <IP>      {la['O4']}
    -p/--port <PORT>    {la['O5']}
    --sslc <PATH>       {la['O6']}
    --sslp <PATH>       {la['O7']}
    --sslcc <PATH>      {la['O9']}
    --pas <PASSWORD>    {la['O10']}'''
    print(h)


def gopt(args):
    re = getopt(args, 'h?s:p:', ['help', 'lan=',
                                 'host=', 'port=', 'sslc=', 'sslp=', 'pas='])
    rr = re[0]
    r = {}
    h = False
    for i in rr:
        if i[0] == '-h' or i[0] == '-?' or i[0] == '--help':
            h = True
        if i[0] == '--lan' and not 'lan' in r and (i[1] == 'null' or i[1] in lan):
            r['lan'] = i[1]
        if (i[0] == '-s' or i[0] == '--host') and not 's' in r:
            r['s'] = i[1]
        if (i[0] == '-p' or i[0] == '--port') and not 'p' in r:
            r['p'] = int(i[1])
        if i[0] == '--sslc' and not 'sslc' in r:
            r['sslc'] = i[1]
        if i[0] == '--sslp' and not 'sslp' in r:
            r['sslp'] = i[1]
        if i[0] == '--sslcc' and not 'sslcc' in r:
            r['sslcc'] = i[1]
        if i[0] == '--pas' and not 'pas' in r:
            r['pas'] = i[1]
    global la
    if h:
        la = getdict('command', getlan(se, r), 'webui')
        ph()
        exit(0)
    if 'sslc' in r or 'sslp' in r:
        if 'sslc' in r and 'sslp' in r:
            pass
        else:
            la = getdict('command', getlan(se, r), 'webui')
            print(la['O8'])
            exit(0)
    if 'pas' in r:
        if len(r['pas']) >= 8 and len(r['pas']) <= 20:
            r['pas'] = sha256(r['pas'])
        else:
            la = getdict('command', getlan(se, r), 'webui')
            print(la['O11'].replace('<min>', '8').replace('<max>', '20'))
            exit(0)
    return r


la = None
se = loadset()
if se == -1 or se == -2:
    se = {}
la = getdict('command', getlan(se, {}), 'webui')
