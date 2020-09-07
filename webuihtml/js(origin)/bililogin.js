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
    /**将元素背景临时变成红色
     * @param {HTMLElement} i
    */
    function turnred(i) {
        var oldstyle = i.style.backgroundColor;
        i.style.backgroundColor = "red";
        ((i, oldstyle) => { setTimeout(() => { i.style.backgroundColor = oldstyle }, 3000) })(i, oldstyle);
    }
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
            var uri2 = new URL(uri, url.origin);
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
    var submittype = 0;
    /**@type {HTMLImageElement}*/
    var img = null;
    /**@type {HTMLInputElement}*/
    var cap = null;
    function addtoimg() {
        img.addEventListener('click', addtoimg);
        $.getJSON('/api/captcha', (e, s) => {
            if (s == "success") {
                if (e.code == 0) {
                    var type = e.type == null ? "image/jpeg;charset=UTF-8" : e.type;
                    var img2 = new Blob([Base64.toUint8Array(e.img)], { 'type': type });
                    img.src = URL.createObjectURL(img2);
                    var cap2 = e.cap == null ? "" : e.cap;
                    cap.value = cap2;
                }
                else console.warn(e)
            }
        })
    }
    function getpubkey(e) {
        if (e.code == 0) {
            var e2 = bytesToHex(Base64.toUint8Array(e.e));
            var k = bytesToHex(Base64.toUint8Array(e.k));
            pubkey = new RSAKey();
            pubkey.setPublic(k, e2);
            /**@type {HTMLInputElement}*/
            var sub = document.getElementById('submit');
            function addtosub() {
                sub.addEventListener('click', submit);
                sub.disabled = false;
            }
            if (sub == null) {
                window.addEventListener('load', () => {
                    sub = document.getElementById('submit');
                    addtosub()
                })
            }
            else addtosub();
            img = document.getElementById('captimg');
            cap = document.getElementById('captcha');
            if (img == null || cap == null) {
                window.addEventListener('load', () => {
                    img = document.getElementById('captimg');
                    cap = document.getElementById('captcha');
                    addtoimg();
                })
            }
            else addtoimg();
        }
        else {
            console.error(e);
        }
    }
    function submit() {
        $.getJSON('/api/getpubkey', (e, s) => {
            if (s == "success") {
                if (e.code == 0) {
                    if (submittype == 0) {
                        /**@type {HTMLInputElement}*/
                        var un = document.getElementById('username');
                        /**@type {HTMLInputElement}*/
                        var pa = document.getElementById('password');
                        /**@type {HTMLInputElement}*/
                        var ca = document.getElementById('captcha');
                        if (un.validationMessage != "") {
                            alert(un.validationMessage);
                            turnred(un);
                            return;
                        }
                        if (pa.validationMessage != "") {
                            alert(pa.validationMessage);
                            turnred(pa);
                            return;
                        }
                        var user = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(un.value))));
                        var pass = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(pa.value))));
                        var param = { type: submittype, username: user, password: pass };
                        if (ca.value != "") param['capt'] = ca.value;
                        $.getJSON('/api/login', param, (e, s) => {
                            if (s == "success") dealwithuserpass(e);
                        })
                    }
                }
                else {
                    console.error(e);
                }
            }
        })
    }
    function dealwithuserpass(e) {
        console.log(e);
        if (e.code == -2) {//解密失败，尝试获取新的公钥再次重试
            console.warn(e.e);
            /**@type {HTMLInputElement}*/
            var sub = document.getElementById('submit');
            sub.disabled = true;
            $.getJSON('/api/rsa', (e, s) => {
                if (s == "success") {
                    if (e.code == 0) {
                        var e2 = bytesToHex(Base64.toUint8Array(e.e));
                        var k = bytesToHex(Base64.toUint8Array(e.k));
                        pubkey = new RSAKey();
                        pubkey.setPublic(k, e2);
                        sub.disabled = false;
                        sub.click();//重新点击
                    }
                }
            })
        }
        else if (e.code == -3) {//需要验证码
            cap.required = true;
            alert(transobj['webui.bililogin']['NEEDCAP']);
        }
        else if (e.code == -4) {//服务繁忙
            console.log(e.result);
            alert(transobj['webui.bililogin']['SERISBUS'])
        }
        else if (e.code == -5) {//其他API返回值
            console.warn(e.result);
            alert(e.result.code + " " + e.result.message);
        }
        else if (e.code == -6) {//用户名或密码错误。
            alert(transobj['webui.bililogin']['INCOUSPA']);
        }
        else if (e.code == 0) {
            alert(transobj['bili.biliLogin']['OUTPUT1']);
            driect();
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
