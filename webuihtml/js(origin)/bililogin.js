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
    /**@typedef {Object} RSAKey
     * @property {(pubkeyhex:string,ehex:string)=>void} setPublic 设置公钥
     * @property {(con:string)=>string} encrypt 加密内容，返回为hex
    */
    /**@type {RSAKey}*/
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
        if (submittype == 2) {
            loginwithSMS();
            return;
        }
        else if (submittype == 3) {
            loginwithpassweb();
            return;
        }
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
    /**重新获得PubKey
     * @param {callback} f
     */
    function regetpubkey(f) {
        $.getJSON('/api/rsa', (e, s) => {
            if (s == "success") {
                if (e.code == 0) {
                    var e2 = bytesToHex(Base64.toUint8Array(e.e));
                    var k = bytesToHex(Base64.toUint8Array(e.k));
                    pubkey = new RSAKey();
                    pubkey.setPublic(k, e2);
                    f();
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
            regetpubkey(() => {
                sub.disabled = false;
                sub.click();//重新点击
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
    /**@type {HTMLCollectionOf<HTMLLabelElement>}*/
    var switc = document.getElementsByClassName('switch');
    if (switc.length == 0) {
        window.addEventListener('load', () => {
            switc = document.getElementsByClassName('switch');
            switc_thendo();
        })
    }
    else switc_thendo();
    function switc_thendo() {
        for (var i = 0; i < switc.length; i++) {
            var sw = switc[i];
            sw.addEventListener('click', switc_click);
        }
    }
    /**@param {MouseEvent} e*/
    function switc_click(e) {
        /**@type {HTMLLabelElement}*/
        var src = this
        if (src.hasAttribute('switch')) {
            var sw = src.getAttribute('switch');
            try {
                sw = sw - 1 + 1;
            } catch (error) {
                console.warn(error)
                return;
            }
            submittype = sw;
            src.parentElement.style.display = "none";
            if (src.hasAttribute('switch2')) {
                var targetid = src.getAttribute('switch2');
                var target = document.getElementById(targetid);
                if (target == null) {
                    console.warn(src);
                    console.warn('This target id have wrong.')
                    return;
                }
                target.style.display = null;
                /**@type {HTMLInputElement}*/
                var sub = document.getElementById('submit');
                sub.disabled = false;
                if (targetid == "qrc") {
                    sub.disabled = true;
                    makeqrcode();
                }
                else if (targetid == "phocode") {
                    init_smslogin();
                    sub.disabled = true;
                }
            }
            else {
                console.warn(src);
                console.warn('This object do not have switch2 attribute.');
                return;
            }
            for (var i = 0; i < switc.length; i++) {
                var te = switc[i];
                if (te != src) {
                    te.parentElement.style.display = null;
                    if (!te.hasAttribute('switch2')) {
                        console.warn(te);
                        console.warn('This object do not have switch2 attribute.');
                        return;
                    }
                    var targetid = te.getAttribute('switch2');
                    var target = document.getElementById(targetid);
                    if (target == null) {
                        console.warn(te);
                        console.warn('This target id have wrong.')
                        return;
                    }
                    target.style.display = "none";
                }
            }
        }
        else {
            console.warn(src)
            console.warn('This object do not have switch attribute.')
        }
    }
    var qrcode = null;
    /**@type {HTMLDivElement}*/
    var qrdiv = null;
    /**生成QRCODE
     * @param {string} c
     * @param {(e:string)=>void} f 回调函数
     */
    function getqrcode(c, f) {
        if (qrcode == null) {
            qrdiv = document.createElement('div');
            qrcode = new QRCode(qrdiv, { text: c, width: 140, height: 140, colorcolorDark: "#000000", colorLight: "#ffffff", correctLevel: QRCode.CorrectLevel.H })
        }
        else qrcode.makeCode(c);
        function getcode() {
            if (qrdiv.children[1].src == "") {
                setTimeout(getcode, 100);
            }
            else {
                var arr = Base64.toUint8Array(qrdiv.children[1].src.split(',')[1]);
                f(URL.createObjectURL(new Blob([arr], { "type": "image/png" })));
            }
        }
        getcode();
    }
    /**@type {number} 存储检查是否登录成功的定时器句柄*/
    var qrcode_loop = null;
    /**@type {string} QRCode URL*/
    var qrcode_url = null;
    /**@type {string} QRCode 生成时间*/
    var qrcode_ts = null;
    /**@type {string} QRCode oauthKey*/
    var qrcode_oauthKey = null;
    function makeqrcode() {
        if (qrcode_loop != null) {
            clearInterval(qrcode_loop);
            qrcode_loop = null;
        }
        $.getJSON('/api/qrgetloginurl', (e, s) => {
            if (s == "success") {
                if (e.code == 0) {
                    var result = e.result;
                    if (result.code == 0 && result.status) {
                        qrcode_ts = result.ts;
                        qrcode_url = result.data.url;
                        qrcode_oauthKey = result.data.oauthKey;
                        /**@type {HTMLImageElement}*/
                        var qrc = document.getElementById('qrcimg');
                        /**@type {HTMLLabelElement}*/
                        var qrcl = document.getElementById('qrcl');
                        getqrcode(qrcode_url, (q_img) => {
                            qrc.src = q_img;
                            qrcl.style.display = "none";
                            if (!qrcl.hasAttribute('add')) {
                                qrcl.addEventListener('click', makeqrcode);
                                qrcl.setAttribute('add', '1');
                            }
                            checkislogin();
                        });
                    }
                }
                else {
                    console.error(e)
                }
            }
        })
    }
    /**判断是否登录成功 */
    function checkislogin() {
        /**当前时间*/
        var now = Math.round(new Date().getTime() / 1000);
        if (now < qrcode_ts + 180) {
            $.getJSON('/api/qrgetlogininfo', { 'key': qrcode_oauthKey }, (e, s) => {
                if (e.code == 0) {
                    if (e.status) {//登录成功
                        alert(transobj['bili.biliLogin']['OUTPUT1']);
                        driect();
                    }
                    else qrcode_loop = setTimeout(checkislogin, 3000);
                }
                else {
                    console.error(e);
                }
            })
        }
        else {
            /**@type {HTMLLabelElement}*/
            var qrcl = document.getElementById('qrcl');
            qrcl.style.display = null;
            qrcode_loop = null;
        }
    }
    /**@typedef {()=>void} callback
     * @typedef {(error:{error_code:string,msg:string})=>void} GeetestErrorCallback
     * @typedef {{"success":number,"gt":string,"challenge":string,"key":string}} CapcomInfo
     * @typedef {Object} GeetestObj 
     * @property {(position:(string|HTMLElement))=>void} appendTo 用于将验证按钮插到宿主页面，使其显示在页面上。接受的参数可以是 id 选择器（例如 #captcha-box），或者 DOM 元素对象。
     * @property {(position:(string|HTMLElement))=>void} bindForm 接受的参数类型与 appendTo 方法一致。该该接口的作用是插入验证结果的三个 input 标签到指定的表单中。
     * @property {()=>{geetest_challenge:string,geetest_validate:string,geetest_seccode:string}} getValidate 获取用户进行成功验证(onSuccess)所得到的结果，该结果用于进行服务端 SDK 进行二次验证。
     * @property {()=>void} reset 让验证回到初始状态。一般是在用户后台发现验证成功但其他信息不对的情况（比如用户名密码错误），或者验证出现错误的情况。因此，该接口只能在成功或者出错的时候调用才有效。
     * @property {()=>void} verify 当product为bind类型时，可以调用该接口进行验证。这种形式的好处是，允许开发者先对用户所填写的数据进行检查，没有问题之后在调用验证接口。
     * @property {(callback:callback)=>void} onReady 监听验证按钮的 DOM 生成完毕事件。
     * @property {(callback:callback)=>void} onSuccess 监听验证成功事件。
     * @property {(callback:GeetestErrorCallback)=>void} onError 监听验证出错事件。刷新过多、静态资源加载失败、网络不给力等验证码能捕获到的错误，都会触发onError回调。当出错事件触发时，可以提示用户刷新页面重试。
     * @property {(callback:callback)=>void} onClose 对于product为bind形式的验证。当用户关闭弹出来的验证时，会触发该回调。
     * @property {()=>void} destroy 销毁验证实例，验证相关UI以及验证注册的事件监听器都会被移除。
    */
    /**@type {GeetestObj}*/
    var captchaObj = null;
    /**@type {string} 手机号码*/
    var PHONE_NUM;
    /**@type {string} 国家ID*/
    var CONID;
    function init_smslogin() {
        var phoarea = document.getElementById('phoarea');
        if (!phoarea.hasAttribute('geted')) {
            $.getJSON('/api/getcountrylist', (e, s) => {
                if (s == "success") {
                    if (e.code == 0) {
                        /**@typedef {{"id":number,"cname":string,"country_id":string}} country*/
                        /**@type {Array<country>} */
                        var code_list = e.result;
                        for (var i = 0; i < code_list.length; i++) {
                            var country = code_list[i];
                            var op = document.createElement('option');
                            op.value = country.id;
                            op.innerText = country.cname;
                            op.setAttribute('country_id', country.country_id);
                            phoarea.append(op);
                        }
                        phoarea.setAttribute('geted', 1);
                    }
                    else {
                        console.error(e)
                    }
                }
            })
        }
        var sendSMS = document.getElementById('sendSMS');
        if (!sendSMS.hasAttribute('adde')) {
            sendSMS.addEventListener('click', init_sendSMS);
            sendSMS.setAttribute('adde', 1);
        }
    }
    function init_sendSMS() {
        /**@type {HTMLSelectElement}*/
        var phoarea = document.getElementById('phoarea');
        /**@type {HTMLInputElement}*/
        var phonum = document.getElementById('phonum');
        if (phonum.validationMessage != "") {
            alert(phonum.validationMessage);
            turnred(phonum);
            return;
        }
        /**区域码*/
        var area = phoarea.value;
        /**电话号码*/
        var phon = phonum.value;
        if (area == "1" && (phon[0] != "1" || phon.length != 11)) {
            alert(transobj['webui.bililogin']['INVALIDCPN']);
            turnred(phonum);
            turnred(phoarea);
            return;
        }
        $.getJSON('/api/getcaptchacombine', (e, s) => {
            if (s == "success") {
                var rtype = e.data.type;
                if (rtype == 1) {
                    /**@type {CapcomInfo}*/
                    var re = e.data.result;
                    initGeetest({ gt: re.gt, challenge: re.challenge, new_captcha: true, offline: !re.success, next_width: "270px", product: "bind" }, function (obj) {
                        captchaObj = obj;
                        captchaObj.onClose(() => {
                            alert(transobj['webui.bililogin']['MUSTCAPT']);
                            captchaObj.destroy();
                        })
                        captchaObj.onError((error) => {
                            var str = transobj['webui.bililogin']['CAPERROR'] + '\n' + error.error_code + ":" + error.msg;
                            alert(str);
                            captchaObj.destroy();
                        })
                        captchaObj.onSuccess(() => {
                            var capres = captchaObj.getValidate();
                            var ephon = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(phon))));//加密电话号码
                            var par = { cid: area, tel: ephon, key: re.key, captchaType: 6, type: 21, challenge: capres.geetest_challenge, validate: capres.geetest_validate, seccode: capres.geetest_seccode }
                            function sendlogin_sms() {
                                $.getJSON('/api/sendloginsms', par, (e, s) => {
                                    if (s != "success") return;
                                    if (e.code == -1) {//加密解密错误
                                        console.warn(e.e);
                                        /**@type {HTMLInputElement}*/
                                        var sendSMS = document.getElementById('sendSMS');
                                        sendSMS.disabled = true;
                                        regetpubkey(() => {
                                            ephon = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(phon))));
                                            par['tel'] = ephon;
                                            sendSMS.disabled = false;
                                            sendlogin_sms();
                                        })
                                    }
                                    else if (e.code == 0) {
                                        PHONE_NUM = phon;
                                        CONID = area;
                                        /**@type {HTMLInputElement}*/
                                        var sub = document.getElementById('submit');
                                        sub.disabled = false;
                                        alert(transobj['webui.bililogin']['SMSSEND'])
                                    }
                                    else if (e.code == -2) {
                                        captchaObj.destroy();
                                        console.warn(e)
                                        var errmsg = transobj['webui.bililogin']['CAPERROR'] + '\n' + e.result.code + ':' + e.result.message;
                                        alert(errmsg);
                                    }
                                    else {
                                        console.error(e);
                                        captchaObj.destroy();
                                    }
                                })
                            }
                            sendlogin_sms();
                        })
                        captchaObj.onReady(() => {
                            captchaObj.verify();
                        })
                    })
                }
                else {
                    console.error(e.data);
                }
            }
        })
    }
    function loginwithSMS() {
        /**@type {HTMLInputElement}*/
        var phocapt = document.getElementById('phocapt');
        if (phocapt.validationMessage != "") {
            alert(phocapt.validationMessage);
            turnred(phocapt);
            return;
        }
        var captcode = phocapt.value;
        var capres = captchaObj.getValidate();
        if (!capres) {
            alert(transobj['webui.bililogin']['MUSTCAPT']);
            return;
        }
        var ephon = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(PHONE_NUM))));//加密电话号码
        var par = { cid: CONID, tel: ephon, smsCode: captcode, source: "main-mini", keep: true, degrade: true, gourl: "https://passport.bilibili.com/ajax/miniLogin/redirect" };
        function send_login_with_SMS() {
            $.getJSON('/api/loginwithsms', par, (e, s) => {
                if (s != "success") return;
                if (e.code == -1) {
                    console.warn(e.e);
                    /**@type {HTMLInputElement}*/
                    var sub = document.getElementById('submit');
                    sub.disabled = true;
                    regetpubkey(() => {
                        ephon = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(phon))));
                        par['tel'] = ephon;
                        sub.disabled = false;
                        send_login_with_SMS();
                    })
                }
                else if (e.code == -2) {
                    captchaObj.destroy();
                    console.warn(e)
                    var errmsg = transobj['webui.bililogin']['CAPERROR'] + '\n' + e.result.code + ':' + e.result.message;
                    alert(errmsg);
                }
                else if (e.code == 0) {
                    alert(transobj['bili.biliLogin']['OUTPUT1']);
                    driect();
                }
                else {
                    console.error(e);
                    captchaObj.destroy();
                }
            })
        }
        send_login_with_SMS();
    }
    function loginwithpassweb() {
        /**@type {HTMLInputElement}*/
        var userw = document.getElementById('usernamew');
        /**@type {HTMLInputElement}*/
        var passw = document.getElementById('passwordw');
        if (userw.validationMessage != "") {
            alert(userw.validationMessage);
            return;
        }
        if (passw.validationMessage != "") {
            alert(passw.validationMessage);
            return;
        }
        /**用户名*/
        var un = userw.value;
        /**密码*/
        var pa = passw.value;
        $.getJSON('/api/getpubkeyweb', (e, s) => {
            if (s != "success") return;
            if (e.code != 0) {
                console.error(e);
                return;
            }
            $.getJSON('/api/getcaptchacombine', (e, s) => {
                if (s != "success") return;
                if (e.code == -1) {
                    console.error(e);
                    var errmsg = transobj['webui.bililogin']['CAPERROR'] + '\n' + e.result.code + ':' + e.result.message;
                    alert(errmsg)
                    return;
                }
                else if (e.code != 0) {
                    console.error(e.e);
                    return;
                }
                if (e.data.type != 1) {
                    console.error(e.data);
                    return;
                }
                /**@type {CapcomInfo}*/
                var re = e.data.result;
                initGeetest({ gt: re.gt, challenge: re.challenge, new_captcha: true, offline: !re.success, next_width: "270px", product: "bind" }, function (obj) {
                    captchaObj = obj;
                    captchaObj.onClose(() => {
                        alert(transobj['webui.bililogin']['MUSTCAPT']);
                        captchaObj.destroy();
                    })
                    captchaObj.onError((error) => {
                        var str = transobj['webui.bililogin']['CAPERROR'] + '\n' + error.error_code + ":" + error.msg;
                        alert(str);
                        captchaObj.destroy();
                    })
                    captchaObj.onSuccess(() => {
                        var capres = captchaObj.getValidate();
                        var eun = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(un))));//加密用户名
                        var epa = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(pa))));//加密密码
                        var par = { username: eun, password: epa, keep: true, key: re.key, captchaType: 6, goUrl: "https://passport.bilibili.com/ajax/miniLogin/minilogin", challenge: capres.geetest_challenge, validate: capres.geetest_validate, seccode: capres.geetest_seccode }
                        function sendlogin() {
                            $.getJSON('/api/loginwithuserpassweb', par, (e, s) => {
                                if (s != "success") return;
                                if (e.code == -1) {
                                    console.warn(e.e);
                                    /**@type {HTMLInputElement}*/
                                    var sub = document.getElementById('submit');
                                    sub.disabled = true;
                                    regetpubkey(() => {
                                        epa = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(pa))));
                                        eun = Base64.fromUint8Array(new Uint8Array(hexToBytes(pubkey.encrypt(un))));
                                        par['password'] = epa;
                                        par['username'] = eun;
                                        sub.disabled = false;
                                        sendlogin();
                                    })
                                    return;
                                }
                                if (e.code == -2) {
                                    captchaObj.destroy();
                                    console.warn(e)
                                    var errmsg = transobj['webui.bililogin']['CAPERROR'] + '\n' + e.result.code + ':' + e.result.message;
                                    alert(errmsg);
                                    return;
                                }
                                if (e.code != 0) {
                                    console.error(e);
                                    captchaObj.destroy();
                                    return;
                                }
                                alert(transobj['bili.biliLogin']['OUTPUT1']);
                                driect();
                            })
                        }
                        sendlogin();
                    })
                    captchaObj.onReady(() => {
                        captchaObj.verify();
                    })
                })
            })
        })
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
