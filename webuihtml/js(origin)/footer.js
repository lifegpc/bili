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
(() => {
    /**@type {HTMLStyleElement}*/
    var sty = null;
    function footerchange() {
        if (sty == null) {
            sty = document.createElement('style');
            document.head.append(sty);
        }
        var footer = document.getElementsByClassName('footer');
        var footer_h = 0;
        if (footer.length) {
            footer_h = footer[0].scrollHeight;
        }
        if (sty.hasAttribute('top')) {
            sty.innerText = ".footer{display:none;top:" + sty.getAttribute('top') + "px;}"
        }
        else {
            sty.innerText = ".footer{display:none;}"
        }
        var w_height = window.innerHeight;
        var b_height = document.body.scrollHeight;
        if (b_height + footer_h > w_height) {
            sty.innerText = ".footer{top:" + b_height + "px;padding-boto}"
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
