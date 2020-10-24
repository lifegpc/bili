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
    /**@type {HTMLInputElement}*/
    var pass = document.getElementById('password');
    function direct() {
        var url = new URL(window.location.href);
        var uri = url.searchParams.get('p');
        var hl = url.searchParams.get('hl');
        var param = {}
        if (hl != null) param['hl'] = hl;
        param = $.param(param)
        if (uri == null) {
            if (param != "") uri = '/?' + param;
            else uri = '/';
        }
        else {
            var uri2 = new URL(uri, url.origin);
            if (param != "" && uri2.searchParams.get('hl') == null) {
                uri2.searchParams.set('hl', hl);
            }
            uri = uri2.href;
        }
        window.location.href = uri;
    }
    pass.addEventListener('keydown', (e) => {
        if (e.code == "Enter" || e.keyCode == 13) {
            if (pass.validationMessage != "") {
                alert(pass.validationMessage);
                return;
            }
            else {
                $.post("/login", { 'p': sha256(pass.value) }, function (data, s) {
                    if (s == "success") {
                        if (data.code == 0) {
                            alert(transobj['bili.biliLogin']['OUTPUT1']);
                            direct();
                        }
                        else if (data.code == -1) {
                            alert(transobj['bili.biliLogin']['ERROR2']);
                        }
                        else {
                            alert(transobj['webui.index']['NONELOG']);
                            direct();
                        }
                    }
                })
            }
        }
    })
    $.getJSON('/api/checkuilogin', (e, s) => {
        if (s != "success") return;
        if (e.code == 0) direct();
        else if (e.code == -500) {
            console.error(e.e);
            alert(e.e);
        }
    })
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
        if (w_height <= m_height) {
            sty.innerText = "";
        }
        else {
            var top = (w_height - m_height) / 2;
            sty.innerText = "#main{top:" + top + "px;}"
        }
    }
    mainchange();
    var timeout = () => {
        mainchange();
        setTimeout(timeout, 2000);
    }
    setTimeout(timeout, 2000);
    window.addEventListener('resize', mainchange)
})
