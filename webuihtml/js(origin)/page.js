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
    /**@typedef {Object} PageData
     * @property {number} page P数
     * @property {string} part 分P名
     * @property {number} cid 视频CID
     * @typedef {Object} NormalVideoData
     * @property {number} aid AV号
     * @property {string} bvid BV号
     * @property {number} ctime 上次修改时间
     * @property {string} desc 视频简介
     * @property {number|undefined} gv graph_version，仅互动视频有
     * @property {string} name UP主名称
     * @property {Array<PageData>} page 每一P的信息
     * @property {string} pic 封面图片地址
     * @property {number} pubdate 视频发布时间
     * @property {string} title 视频标题
     * @property {number} uid UP主ID
     * @property {number} videos 分P数
     * @typedef {Object} errorinfo
     * @property {number} code 错误状态码。
     * @property {string} message 错误信息。
     * @typedef {Object} infodata
     * @property {0|-1} code 状态码。0正常，-1有错误。
     * @property {errorinfo|undefined} re 错误信息。（仅当code为-1时存在）
     * @property {NormalVideoData|undefined} data 视频信息
     * @typedef {Object} ExtractorInfo
     * @property {0|-1|-404|-500} code 状态码。0正常，-1需要登录，-404匹配不到相应的解析器，-500程序错误。
     * @property {string|undefined} e 抛出的错误信息（仅code为-500时存在）
     * @property {string|undefined} type 解析器的类型（仅code为0时存在）
     * @property {string|undefined} url 仅当type为redirect时存在，重定向至的地址
     * @property {infodata|undefined} data 数据（仅当code为0时并type不为redirect时存在）
    */
    /**@type {ExtractorInfo}*/
    var info = window['info'];
    if (info.code == -1) {
        var uri = new URL(window.location.href);
        var param = {};
        var hl = uri.searchParams.get('hl');
        if (hl != null) param['hl'] = hl;
        param['p'] = window.location.href;
        param = $.param(param);
        window.location.href = '/bililogin?' + param;
    }
    var main = document.getElementById('main');
    /**新建一个需要翻译的Label
     * @param {string} s trans字段
     * @returns {HTMLLabelElement}
     */
    function createTransLabel(s) {
        var label = document.createElement('label');
        label.className = "trans";
        label.setAttribute('trans', s);
        return label;
    }
    /**新建一个普通label
     * @param {string|number} s label的内容
     * @returns {HTMLLabelElement}
    */
    function createLabel(s) {
        var label = document.createElement('label');
        label.innerText = s.toString();
        return label;
    }
    function newbr() { return document.createElement('br'); }
    /**格式化时间
     * @param {number} t 时间（秒）
     * @returns {string}
    */
    function formattime(t) {
        return new Date(t * 1000).format("yyyy-MM-dd hh:mm:ss");
    }
    if (info.code == -500) {
        if (!main.classList.has('e500')) {
            main.classList.add(['e500']);
        }
        main.innerText = info.e;
    }
    else if (info.code == -404) {
        if (!main.classList.has('e404')) {
            main.classList.add(['e404']);
        }
        main.append(createTransLabel('webui.page NOTEXT'));
        transobj.deal();
    }
    else if (info.code == 0) {
        if (info.type == "redirect") {
            var uri = new URL(window.location.href);
            var param = {};
            var hl = uri.searchParams.get('hl');
            if (hl != null) param['hl'] = hl;
            param = $.param(param);
            var url = '/page/' + encodeURIComponent(info.url);
            if (param != "") url += ("?" + param);
            window.location.href = url;
        }
        else {
            var data = info.data;
            if (data.code == -1) {
                var re = data.re;
                if (!main.classList.has('e1')) {
                    main.classList.add(['e1']);
                }
                main.innerText = re.code + " " + re.message;
            }
            else {
                if (info.type == "normal") dealnormalvideo();
            }
        }
    }
    /**@type {HTMLImageElement}*/
    var img;
    /**@type {HTMLDivElement}*/
    var smallinfod1;
    /**@type {HTMLDivElement}*/
    var smallinfod2;
    function dealnormalvideo() {
        var data = info.data.data;
        var videoinfo = document.createElement('div');
        videoinfo.className = "videoinfo";
        main.append(videoinfo);
        var title = document.createElement('h1');
        title.innerText = data.title;
        videoinfo.append(title);
        /**多列布局用*/
        var smallinfo = document.createElement('div');
        smallinfo.className = "flex";
        videoinfo.append(smallinfo);
        smallinfod1 = document.createElement('div');
        smallinfod2 = document.createElement('div');
        var smallinfod3 = document.createElement('div');
        smallinfo.append(smallinfod1);
        smallinfo.append(smallinfod2);
        smallinfo.append(smallinfod3);
        smallinfod1.append(createTransLabel('bili.PrintInfo O1'));//AV号
        smallinfod1.append(createLabel(data.aid));
        smallinfod2.append(createTransLabel('bili.PrintInfo O2'));//BV号
        smallinfod2.append(createLabel(data.bvid));
        img = document.createElement('img');
        img.src = "/pic/" + encodeURIComponent(data.pic);
        smallinfod3.append(img);
        smallinfod1.append(newbr());
        smallinfod1.append(createTransLabel('bili.PrintInfo O3'));//分P数
        smallinfod1.append(createLabel(data.videos));
        smallinfod2.append(newbr());
        smallinfod2.append(createTransLabel('bili.PrintInfo O5'));//发布时间
        smallinfod2.append(createLabel(formattime(data.pubdate)));
        smallinfod1.append(newbr());
        smallinfod1.append(createTransLabel('bili.PrintInfo O6'));//上次修改时间
        smallinfod1.append(createLabel(formattime(data.ctime)));
        smallinfod2.append(newbr());
        smallinfod2.append(createTransLabel('bili.PrintInfo O24'));//UP主名称
        smallinfod2.append(createLabel(data.name));
        smallinfod1.append(newbr());
        smallinfod1.append(createLabel('UID:'));
        smallinfod1.append(createLabel(data.uid));
        videoinfo.append(createTransLabel('bili.PrintInfo O7'));
        videoinfo.append(createLabel(data.desc));
        transobj.deal();
    }
    /**@type {HTMLStyleElement}*/
    var sty = null;
    function mainchange() {
        if (sty == null) {
            sty = document.createElement('style');
            document.head.append(sty);
        }
        if (main == null) {
            main = document.getElementById('main');
            if (main == null) return;
        }
        if (img != null && smallinfod1 != null && smallinfod2 != null) {
            var sm_h1 = smallinfod1.scrollHeight;
            var sm_h2 = smallinfod2.scrollHeight;
            img.height = sm_h1 > sm_h2 ? sm_h1 : sm_h2;
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
    window.addEventListener('resize', mainchange);
})
