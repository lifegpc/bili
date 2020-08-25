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
var r = {
    "ip": /((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))/
}
window.addEventListener('load', () => {
    /**@type {HTMLButtonElement} 提交按钮*/
    var submit = document.getElementById('submit');
    /**@type {HTMLCollectionOf<HTMLElement>} 表单类元素*/
    var formlist = document.getElementsByClassName('form');
    /**将元素背景临时变成红色
     * @param {HTMLElement} i
    */
    function turnred(i) {
        var oldstyle = i.style.backgroundColor;
        i.style.backgroundColor = "red";
        ((i, oldstyle) => { setTimeout(() => { i.style.backgroundColor = oldstyle }, 3000) })(i, oldstyle);
    }
    submit.addEventListener('click', () => {
        var data = {}
        var type = 0
        for (var i = 0; i < formlist.length; i++) {
            /**@type {HTMLInputElement}*/
            var t = formlist[i];
            if (t.id == "type") {
                type = t.value;
            }
            else if (t.id != "form" && t.id != "submit")//排除按钮和表单元素
            {
                if (t.value != undefined && t.value != null && t.value != "") {
                    if (t.type == "text") {
                        if (t.validationMessage != "") {
                            alert(t.validationMessage);
                            turnred(t);
                            return;
                        }
                        else if (t.hasAttribute('regex')) {
                            var key = t.getAttribute('regex');
                            if (r.hasOwnProperty(key)) {
                                var trans = t.getAttribute('itrans');
                                if (trans == null) {
                                    console.warn(t);
                                    console.warn('This object do not contain itrans attribute.');
                                }
                                else {
                                    var re = t.value.match(r[key])
                                    var l = trans.split(' ', 2)
                                    if (re == null) {
                                        /**@type {string}*/
                                        var s = transobj[l[0]][l[1]];
                                        alert(s.replace('<value>', t.value));
                                        turnred(t);
                                        return;
                                    }
                                    else {
                                        data[t.id] = t.value;
                                    }
                                }
                            }
                            else {
                                console.warn(t);
                                console.warn('This object contains unknown regex value.')
                            }
                        }
                        else {
                            data[t.id] = t.value;
                        }
                    }
                    else if (t.type == "number") {
                        if (t.validationMessage != "") {
                            alert(t.validationMessage);
                            turnred(t);
                            return;
                        }
                        else {
                            data[t.id] = t.valueAsNumber;
                        }
                    }
                    else if (t.type == "select-one") {
                        data[t.id] = t.value;
                    }
                    else if (t.type == "checkbox") {
                        if (t.hasAttribute('targetid')) {
                            var targetid = t.getAttribute('targetid');
                            /**@type {HTMLInputElement}*/
                            var t2 = document.getElementById(targetid);
                            if (t2 == null) {
                                console.warn(t);
                                console.warn('Can not find targetid "' + targetid + '"');
                            }
                            else {
                                if (!t2.disabled && t2.value != undefined && t2.value != null && t2.value != "") {
                                    if (t2.type == "password") {
                                        if (t2.validationMessage != "") {
                                            alert(t2.validationMessage);
                                            turnred(t2);
                                            return;
                                        }
                                        else data[t2.id] = sha256(t2.value);
                                    }
                                }
                                else if (!t2.disabled && t2.type == "password") {
                                    data[t2.id] = 'c';
                                }
                            }
                        }
                        else {
                            data[t.id] = t.checked;
                        }
                    }
                }
            }
        }
        $.post("/settings", { "data": JSON.stringify(data), "type": type }, (data, stat) => {
            if (stat == "success") {
                if (data.code == 0) {
                    alert(transobj['webui.settings']['SUBOK'])//保存成功。
                }
                else {
                    alert(transobj['webui.settings']['SUBFA'])//保存设置失败。
                }
            }
        })
    })
    var checktlist = document.getElementsByClassName('checkt')
    for (var i = 0; i < checktlist.length; i++) {
        /**@type {HTMLInputElement}*/
        var t = checktlist[i];
        if (t.type == "checkbox") {
            if (t.hasAttribute('targetid')) {
                var targetid = t.getAttribute('targetid');
                if (targetid == "") {
                    console.warn(t);
                    console.warn('target is empty.')
                }
                else {
                    /**@type {HTMLInputElement}*/
                    var t2 = document.getElementById(targetid);
                    if (t2 == null) {
                        console.warn(t2);
                        console.warn('Can not find targetid "' + targetid + '"');
                    }
                    else {
                        if (t.hasAttribute('revert')) {
                            t2.disabled = t.checked;
                        }
                        else {
                            t2.disabled = !t.checked;
                        }
                        ((t, t2) => {
                            t.addEventListener('input', () => {
                                if (t.hasAttribute('revert')) {
                                    t2.disabled = t.checked;
                                }
                                else {
                                    t2.disabled = !t.checked;
                                }
                            })
                        })(t, t2);
                    }
                }
            }
            else {
                console.warn(t);
                console.warn('This object do not cotains tragetid attribute.')
            }
        }
        else {
            console.warn(t);
            console.warn('This object\'s type is not checkbox.');
        }
    }
    var datalist = document.getElementsByClassName('needdata');
    for (var i = 0; i < datalist.length; i++) {
        /**@type {HTMLDataListElement}*/
        var t = datalist[i];
        if (t.hasAttribute('loc')) {
            var uri = t.getAttribute('loc');
            ((t) => {
                $.getJSON(uri, (data, s) => {
                    if (s == "success") {
                        if (data.code == 0) {
                            var da = data.result;
                            var loc2 = t.getAttribute('loc2');
                            for (var j = 0; j < da.length; j++) {
                                var op = document.createElement('option')
                                op.value = da[j];
                                t.append(op);
                            }
                            if (t.hasAttribute('targetid')) {
                                var targetid = t.getAttribute('targetid');
                                /**@type {HTMLInputElement}*/
                                var t2 = document.getElementById(targetid);
                                if (t2 == null) {
                                    console.warn(t);
                                    console.warn('Can not find targetid "' + targetid + '".');
                                }
                                else {
                                    t2.addEventListener('click', () => {
                                        t2.setAttribute('val', t2.value);
                                        t2.value = "";
                                    })
                                    t2.addEventListener('mouseleave', () => {
                                        if (t2.value == "") {
                                            t2.value = t2.getAttribute('val');
                                        }
                                    })
                                    if (loc2 == "font") {
                                        t2.addEventListener('input', () => {
                                            t2.style.fontFamily = t2.value;
                                        })
                                    }
                                }
                            }
                            else {
                                console.warn(t)
                                console.warn('This object do not cotains targetid attribute.')
                            }
                        }
                        else {
                            console.warn(t)
                            console.warn('get list failed.')
                        }
                    }
                })
            })(t);
        }
        else {
            console.warn(t)
            console.warn('This Object do not contains loc attribute.')
        }
    }
})
