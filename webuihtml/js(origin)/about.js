/* (C) 2019-2020 lifegpc
This file is part of bili.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>. */
(() => {
    /**@type {HTMLStyleElement}*/
    var sty = null;
    /**@type {HTMLTableElement}*/
    var table = null;
    function tablechange() {
        if (sty == null) {
            sty = document.createElement('style');
            document.head.append(sty);
        }
        if (table == null) {
            table = document.getElementById('third');
            if (table == null) return;
        }
        var w_width = window.innerWidth;
        var t_width = table.scrollWidth;
        if (t_width > w_width) sty.innerText = "";
        else {
            var left = (w_width - t_width) / 2;
            sty.innerText = "#third{left:" + left + "px;}";
        }
    }
    window.addEventListener('load', () => {
        tablechange();
        var timeout = () => {
            tablechange();
            setTimeout(timeout, 2000);
        }
        setTimeout(timeout, 2000);
    })
    window.addEventListener('resize', tablechange)
})();
window.addEventListener('load', () => {
    /**@type {HTMLTableElement}*/
    var table = document.getElementById('third');
    var le = table.tBodies.length;
    for (var i = 0; i <= le; i++) {
        var tbody = null;
        if(i==le)tbody = table.tHead;
        else tbody = table.tBodies[i];
        for (var j = 0; j < tbody.rows.length; j++) {
            var row = tbody.rows[j];
            if (row.cells.length > 0) {
                var cell = row.cells[0];
                cell.classList.add(['first']);
            }
        }
    }
})
