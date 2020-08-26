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
    /**@type {HTMLInputElement}*/
    var pass = document.getElementById('password');
    function direct() {
        var url = new URL(window.location.href);
        var uri = url.searchParams.get('p');
        if (uri == null) uri = '/';
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
})
