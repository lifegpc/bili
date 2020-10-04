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
/**@typedef {Object} TransObj
 * @property {()=>void} deal 处理新的元素
 * @property {MutationObserver} observer DOM检测器
*/
/**@type {TransObj} 存放翻译内容*/
var transobj = Object();
/**@param {string} name
 * @param {HTMLCollectionOf<HTMLElement>} list
 * @param {number} i
 * @param {(o:HTMLElement,i:number)=>null} dealwith 
*/
var gettrans = (name, list, i, dealwith) => {
    var le = list.length;
    var param = {};
    var hl = new URL(window.location.href).searchParams.get('hl');
    if (hl != null) param['hl'] = hl;
    $.getJSON('/translate/' + name, param, (ob, stat) => {
        if (stat == "success") {
            if (ob.code == 0) {
                transobj[name] = ob.dict;
                setTimeout(() => { dealwith(list[i], i); }, 10);
            }
            else {
                console.warn('Can not get translate file "' + name + '".')
                if (i < le - 1) {
                    setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
                }
            }
        }
    })
}
/**获得新的翻译
 * @param {string} name
 * @param {()=>{}} f
*/
function gettrans2(name, f) {
    var param = {};
    var hl = new URL(window.location.href).searchParams.get('hl');
    if (hl != null) param['hl'] = hl;
    $.getJSON('/translate/' + name, param, (ob, stat) => {
        if (stat != "success") return;
        if (ob.code != 0) console.warn('Can not get translate file "' + name + '".');
        transobj[name] = ob.dict;
        f();
    })
}
transobj.observer = new MutationObserver((mutationsList, observer) => {
    mutationsList.forEach((v) => {
        if (v.type == "attributes" && !["style"].includes(v.attributeName)) {
            /**@type {HTMLElement}*/
            var o = v.target;
            function dealwithtar(o) {
                var a = o.getAttribute('trans');
                if (a != null) {
                    var l = a.split(' ');
                    if (l.length > 2) {
                        l = [l[0], l.slice(1).join(" ")];
                    }
                    if (transobj.hasOwnProperty(l[0])) {
                        /**@type {Object} 翻译词典*/
                        var obj2 = transobj[l[0]];
                        if (obj2.hasOwnProperty(l[1])) {
                            /**@type {string}*/
                            var t = obj2[l[1]]
                            /**@type {Array} */
                            var t_list = [...t.matchAll(/<([^>]+)>/g)]
                            if (t_list.length == 0) o.innerText = t;
                            else {
                                for (var j = 0; j < t_list.length; j++) {
                                    var key1 = t_list[j][0];
                                    var key2 = t_list[j][1];
                                    if (o.hasAttribute(key2)) {
                                        t = t.replace(key1, o.getAttribute(key2));
                                    }
                                    else {
                                        console.warn(o);
                                        console.warn('This object do not contain ' + key2 + ' attributes.')
                                    }
                                }
                                o.innerText = t;
                            }
                            if (o.hasAttribute('n') && o.getAttribute('n') != t) {
                                o.setAttribute('n', t);
                            }
                            if (o.classList.has('tvalue') && o.getAttribute('value') != t) {
                                o.setAttribute('value', t);
                            }
                        }
                        else {
                            console.warn(o);
                            console.warn('This object do not have translated text.')
                        }
                    }
                    else {
                        gettrans2(l[0], () => { dealwithtar(o); });
                    }
                }
                else {
                    console.warn(o);
                    console.warn('This object do not have trans attribute.')
                }
            }
            dealwithtar(o);
        }
    })
})
transobj.deal = () => {
    /**@type {HTMLCollectionOf<HTMLElement>}*/
    var list = document.getElementsByClassName('trans');
    var le = list.length;
    /** 处理每个元素
     * @param {HTMLElement} o 元素
     * @param {number} i 正在处理的元素索引*/
    function dealwith(o, i) {
        if (o.hasAttribute('t')) {
            if (i < le - 1) {
                setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
            }
            return;
        }
        var a = o.getAttribute('trans');
        if (a != null) {
            var l = a.split(' ');
            if (l.length > 2) {
                l = [l[0], l.slice(1).join(" ")];
            }
            if (transobj.hasOwnProperty(l[0])) {
                /**@type {Object} 翻译词典*/
                var obj2 = transobj[l[0]];
                if (obj2.hasOwnProperty(l[1])) {
                    /**@type {string}*/
                    var t = obj2[l[1]]
                    /**@type {Array} */
                    var t_list = [...t.matchAll(/<([^>]+)>/g)]
                    if (t_list.length == 0) o.innerText = t;
                    else {
                        for (var j = 0; j < t_list.length; j++) {
                            var key1 = t_list[j][0];
                            var key2 = t_list[j][1];
                            if (o.hasAttribute(key2)) {
                                t = t.replace(key1, o.getAttribute(key2));
                            }
                            else {
                                console.warn(o);
                                console.warn('This object do not contain ' + key2 + ' attributes.')
                            }
                        }
                        o.innerText = t;
                    }
                    if (o.hasAttribute('n')) {
                        o.setAttribute('n', t);
                    }
                    if (o.classList.has('tvalue')) {
                        o.setAttribute('value', t);
                    }
                    o.setAttribute('t', 1);//标记为已翻译过
                    transobj.observer.observe(o, { 'attributes': true, 'characterData': false, 'childList': false, 'subtree': false })
                    if (i < le - 1) {
                        setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
                    }
                }
                else {
                    console.warn(o);
                    console.warn('This object do not have translated text.')
                    setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
                }
            }
            else {
                gettrans(l[0], list, i, dealwith);
            }
        }
        else {
            console.warn(o);
            console.warn('This object do not have trans attribute.')
            setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
        }
    }
    if (le > 0) {
        dealwith(list[0], 0);
    }
    var uri = new URL(window.location.href);
    var param = {};
    var hl = uri.searchParams.get('hl');
    if (hl != null) param['hl'] = hl;
    param = $.param(param)
    if (param != "") {
        var alist = document.getElementsByTagName('a');
        for (var i = 0; i < alist.length; i++) {
            var a = alist[i];
            if (a.hasAttribute('hl')) {
                continue;
            }
            var url = new URL(a.href);
            if (url.origin == uri.origin) {
                if (url.search == "") {
                    a.href = url.href + "?" + param;
                }
                else {
                    a.href = url.href + "&" + param;
                }
            }
            a.setAttribute('hl', 1)
        }
    }
}
window.addEventListener('load', transobj.deal)
