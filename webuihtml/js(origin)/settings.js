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
window.addEventListener('load', () => {
    /**@type {HTMLButtonElement} 提交按钮*/
    var submit = document.getElementById('submit');
    /**@type {HTMLCollectionOf<HTMLElement>} 表单类元素*/
    var formlist = document.getElementsByClassName('form');
    submit.addEventListener('click', () => {
        var data = {}
        for (var i = 0; i < formlist.length; i++) {
            var t = formlist[i];
            if (t.id != "form" && t.id != "submit" && t.value != undefined && t.value != null && t.value != "")//排除按钮和表单元素
            {
                data[t.id] = t.value;
            }
        }
        $.post("/settings", data, (data, stat) => {
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
})
