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
    function calabselement() {
        var absc = document.getElementsByClassName('abs');
        var height = 0;
        for (var i = 0; i < absc.length; i++) {
            height += absc[i].scrollHeight;
        }
        return height;
    }
    /**@type {HTMLStyleElement}*/
    var sty = null;
    function footerchange() {
        if (sty == null) {
            sty = document.createElement('style');
            document.head.append(sty);
        }
        if (sty.hasAttribute('top')) {
            sty.innerText = ".footer{display:none;top:" + sty.getAttribute('top') + "px;}"
        }
        else {
            sty.innerText = ".footer{display:none;}"
        }
        var w_height = window.innerHeight;
        var b_height = document.body.scrollHeight;
        var abs_height = calabselement();
        if ((b_height + abs_height) > w_height) {
            sty.innerText = ".footer{top:" + (b_height + abs_height + 20) + "px;padding-boto}"
            sty.setAttribute('top', b_height);
        }
        else {
            sty.innerText = "";
            sty.removeAttribute('top');
        }
    }
    window.addEventListener('load', () => {
        footerchange();
        var timeout = () => {
            footerchange();
            setTimeout(timeout, 2000);
        }
        setTimeout(timeout, 2000);
    })
    window.addEventListener('resize', footerchange)
})();
