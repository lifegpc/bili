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
    function bytesToHex(bytes) {
        for (var hex = [], i = 0; i < bytes.length; i++) {
            var current = bytes[i] < 0 ? bytes[i] + 256 : bytes[i];
            hex.push((current >>> 4).toString(16));
            hex.push((current & 0xF).toString(16));
        }
        var r = hex.join("");
        while (r.charCodeAt(0) == 48) r = r.substring(1);
        return r;
    }
    function hexToBytes(hex) {
        if (hex.length % 2 == 1) hex = "0" + hex;
        for (var bytes = [], c = 0; c < hex.length; c += 2)
            bytes.push(parseInt(hex.substr(c, 2), 16));
        return bytes;
    }
    function driect() {
        var url = new URL(window.location.href);
        var uri = url.searchParams.get('p');
        var hl = url.searchParams.get('hl');
        var param = {}
        if (hl != null) param['hl'] = hl;
        param = $.param(param)
        if (uri == null) {
            uri = '/?' + param;
        }
        else {
            var uri2 = new URL(uri);
            if (param != "" && uri2.searchParams.get('hl') == null) {
                uri2.searchParams.set('hl', hl);
            }
            uri = uri2.href;
        }
        window.location.href = uri;
    }
    $.getJSON('/api/checklogin', (e, s) => {
        if (s == "success") {
            if (e.code == 0) {
                if (e.islogin) {
                    driect();
                    return;
                }
            }
            else {
                console.error(e)
            }
            $.getJSON('/api/rsa', (e, s) => {
                if (s == "success") {
                    getpubkey(e);
                }
            })
        }
    })
    var pubkey;
    function getpubkey(e) {
        if (e.code == 0) {
            var e2 = bytesToHex(Base64.toUint8Array(e.e));
            var k = bytesToHex(Base64.toUint8Array(e.k));
            pubkey = new RSAKey();
            pubkey.setPublic(k, e2);
            $.getJSON('/api/getpubkey', (e, s) => {
                if (s == "success") {
                    if (e.code == 0) { }
                    else {
                        console.error(e);
                    }
                }
            })
        }
        else {
            console.error(e);
        }
    }
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
    window.addEventListener('load', () => {
        mainchange();
        var timeout = () => {
            mainchange();
            setTimeout(timeout, 2000);
        }
        setTimeout(timeout, 2000);
    })
    window.addEventListener('resize', mainchange);
})()
