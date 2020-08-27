/* (C) 2019-2020 lifegpc
This file is part of bili.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. */
window.addEventListener('load', function () {
    function aload() {
        if (!transobj.hasOwnProperty('webui.dir')) {
            setTimeout(aload, 1000);
            return;
        }
        var a = document.getElementById('n');
        var da = document.getElementById('a');
        var db = document.getElementById('b');
        var dc = document.getElementById('c');
        var dd = document.getElementById('d');
        /**@param {HTMLElement} div */
        function ad(div) {
            div.addEventListener('click', function (e) {
                var i = e.srcElement.getAttribute('i') - 1 + 1;
                sc(i, e.srcElement);
            })
        }
        ad(da);
        ad(db);
        ad(dc);
        ad(dd);
        function sc(px = 0, e = null) {
            var fli;
            if (px == 0) fli = fl;
            /**@param {HTMLElement} div*/
            function getz(div, s = 'z') {
                if (s == 'z') return div.getAttribute(s) - 1 + 1;
                else return div.getAttribute(s);
            }
            function setz(zl, s = 'z') {
                var list = [transobj['webui.dir']['AO'], transobj['webui.dir']['DO']];//升序 降序
                da.setAttribute(s, zl[0]);
                function setzz(div, i) {
                    if (zl[i]) div.innerText = getz(div, 'n') + "(" + list[zl[i] - 1] + ")"; else div.innerText = getz(div, 'n');
                }
                setzz(da, 0);
                db.setAttribute(s, zl[1]);
                setzz(db, 1);
                dc.setAttribute(s, zl[2]);
                setzz(dc, 2);
                dd.setAttribute(s, zl[3]);
                setzz(dd, 3);
            }
            var zl = [getz(da), getz(db), getz(dc), getz(dd)];
            function sort(ml, zl) {
                var lista = [];
                var listb = [0, 2, 3];
                var listc = ['fn', 'ft', 'fs', 'lm'];
                var m = -1;
                for (var j = 0; j < listb.length; j++) {
                    if (zl[listb[j]]) m = listb[j];
                }
                for (var j = 0; j < ml.length; j++) {
                    lista[j] = ml[j];
                }
                var temp;
                var zj = 0;
                if (m != -1 && zl[1] == 0) zj = 1;
                if (m == -1) { m = 1; zj = 1; }
                if (zj)//直接排序
                {
                    for (var ii = 0; ii < lista.length - 1; ii++) {
                        for (var ij = lista.length - 1; ij > ii; ij--) {
                            if ((zl[m] == 1 && lista[ij - 1][listc[m]] > lista[ij][listc[m]]) || (zl[m] == 2 && lista[ij - 1][listc[m]] < lista[ij][listc[m]])) {
                                temp = lista[ij]; lista[ij] = lista[ij - 1]; lista[ij - 1] = temp;
                            }
                        }
                    }
                }
                else//混合排序
                {
                    /**@param i 类型排序 */
                    function compare(i, j, ij) {
                        if ((i == 1 && lista[ij - 1].ft > lista[ij].ft) || (i == 2 & lista[ij - 1].ft < lista[ij].ft)) return true;
                        else if (lista[ij - 1].ft == lista[ij].ft && ((j == 1 && lista[ij - 1][listc[m]] > lista[ij][listc[m]]) || (j == 2 && lista[ij - 1][listc[m]] < lista[ij][listc[m]])))
                            return true;
                        else return false;
                    }
                    for (var ii = 0; ii < lista.length - 1; ii++) {
                        for (var ij = lista.length - 1; ij > ii; ij--) {
                            if (compare(zl[1], zl[m], ij)) {
                                temp = lista[ij]; lista[ij] = lista[ij - 1]; lista[ij - 1] = temp;
                            }
                        }
                    }
                }
                return lista;
            }
            if (px != 2 && px != 0) {
                var tlist = [0, 2, 3];
                for (var j = 0; j < tlist.length; j++) {
                    if ((tlist[j] + 1) != px && zl[tlist[j]]) zl[tlist[j]] = 0;
                }
                zl[px - 1]++;
                if (zl[px - 1] == 3) zl[px - 1] = 0;
            }
            else {
                zl[1]++;
                if (zl[1] == 3) zl[1] = 0;
            }
            if (px != 0) {
                setz(zl);
                if (!zl[0] && !zl[1] && !zl[2] && !zl[3]) fli = fl;
                else fli = sort(fl, zl);
            }
            a.innerHTML = "";
            function scd(i) {
                function gsize(size, auto = 1) {
                    if (auto) {
                        if (size < 1024) return size + "B";
                        if (size < (1024 * 1024)) return (size / (1024)).toFixed(3) + "KiB";
                        if (size < (1024 * 1024 * 1024)) return (size / (1024 * 1024)).toFixed(3) + "MiB";
                        if (size < (1024 * 1024 * 1024 * 1024)) return (size / (1024 * 1024 * 1024)).toFixed(3) + "GiB";
                        else return (size / (1024 * 1024 * 1024 * 1024)).toFixed(3) + "TiB";
                    }
                    else return size + "B";
                }
                /**@param {HTMLTableDataCellElement} td*/
                function ssize(td, size) {
                    var i = td.getAttribute('i') - 1 + 1;
                    td.innerText = gsize(size, i);
                    if (i) i = 0; else i = 1;
                    td.setAttribute('i', i);
                }
                /**@param {HTMLTableDataCellElement} td*/
                function stime(td, time) {
                    var i = td.getAttribute('i') - 1 + 1;
                    td.innerText = gtime(time, i);
                    if (i) i = 0; else i = 1;
                    td.setAttribute('i', i);
                }
                function gtime(time, read = 1) {
                    if (read) {
                        var d = new Date(time * 1000);
                        return d.format('yyyy-MM-dd hh:mm:ss');
                    }
                    else return time + "";
                }
                var tr = document.createElement('tr');
                var td = document.createElement('td');
                var a = document.createElement('a');
                if (i.ft == "dir") {
                    a.innerText = i.fn + '/';
                    a.href = i.fn + '/';
                }
                else {
                    a.innerText = i.fn;
                    a.href = i.fn;
                }
                td.appendChild(a);
                tr.appendChild(td);
                var ft = i.ft;
                if (ft == "dir") ft = transobj['webui.dir']['DIR'];
                else if (ft == "file") ft = transobj['webui.dir']['FILE'];
                td = document.createElement('td');
                td.innerText = ft;
                tr.appendChild(td);
                td = document.createElement('td');
                td.innerText = gsize(i.fs);
                td.setAttribute('i', 0);
                (function (size) { td.addEventListener('click', function (e) { ssize(e.srcElement, size); }) })(i.fs);
                tr.appendChild(td);
                td = document.createElement('td');
                td.innerText = gtime(i.lm);
                td.setAttribute('i', 0);
                (function (time) { td.addEventListener('click', function (e) { stime(e.srcElement, time); }) })(i.lm);
                tr.appendChild(td);
                return tr;
            }
            if (l != '/') {
                a.appendChild(scd({ fn: '..', fs: 0, lm: lm, ft: "dir" }))
            }
            for (var i = 0; i < fli.length; i++) {
                a.appendChild(scd(fli[i]));
            }
        }
        sc();//第一次执行
    }
    aload();
})
