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
window.addEventListener('load', () => {
    /**@type {HTMLStyleElement}*/
    var sty = null;
    /**@type {HTMLDivElement}*/
    var main = null;
    function mainchange() {
        if (sty == null) {
            sty = document.createElement('style');
            document.head.append(sty);
        }
        if (main == null) {
            main = document.getElementById('main');
            if (main == null) return;
        }
        var w_height = window.innerHeight;
        var m_height = main.scrollHeight;
        var m_width = main.scrollWidth;
        if (w_height <= m_height) {
            sty.innerText = "";
        }
        else {
            var top = (w_height - m_height) / 2;
            sty.innerText = "#main{top:" + top + "px;}"
        }
        if (m_width <= 640) {
            sty.innerText += "#main input{width:95%;}"
        }
    }
    window.addEventListener('resize', mainchange);
    mainchange();
    var timeout = () => {
        mainchange();
        setTimeout(timeout, 2000);
    }
    setTimeout(timeout, 2000);
})
