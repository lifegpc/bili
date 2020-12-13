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
    /**@typedef {Object} PageData
     * @property {number} page P数
     * @property {string} part 分P名
     * @property {number} cid 视频CID
     * @property {number} duration 分P时长（s）
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
     * @property {0|-1|-404|-412|-500} code 状态码。0正常，-1需要登录，-404匹配不到相应的解析器，-412请求太过频繁被限制，-500程序错误。
     * @property {string|undefined} e 抛出的错误信息（仅code为-500时存在）
     * @property {"normal"|"redirect"|undefined} type 解析器的类型（仅code为0时存在）
     * @property {string|undefined} url 仅当type为redirect时存在，重定向至的地址
     * @property {string|undefined} errorurl 仅当code为-412时存在，发生请求太过频繁的页面地址
     * @property {number|undefined} vip VIP状态（仅当code为0时并type不为redirect时存在）
     * @property {infodata|undefined} data 数据（仅当code为0时并type不为redirect时存在）
     * @typedef {Object} DurlLink
     * @property {string} ahead 未知
     * @property {Array<string>|null} backup_url 备用地址
     * @property {number} length 该部分时间长短（ms）
     * @property {number} order 分段数
     * @property {number} size 该部分大小
     * @property {string} url 地址
     * @property {string} vhead 未知
     * @typedef {Object} DurlUrl
     * @property {number} id 视频流画质
     * @property {string} desc 画质描述
     * @property {number} size 流大小（B）
     * @property {Array<DurlLink>|undefined} url 视频地址（调用API时有vurl参数时才有）
     * @typedef {Object} DashUrl
     * @property {number} id 画/音质ID
     * @property {string|undefined} desc 画质描述
     * @property {string|undefined} codecs 编码信息
     * @property {number|undefined} width 视频宽度
     * @property {number|undefined} height 视频高度
     * @property {string} frame_rate 帧率（B站API返回值，不准确）
     * @property {number} size 流大小
     * @property {Array<string>|undefined} url 视频地址（调用API时有vurl参数时才有）
     * @typedef {Object} VideoUrl
     * @property {string} referer HTTP referer字符串
     * @property {"dash"|"durl"} type 视频链接格式
     * @property {number} timelength 视频时长（ms）
     * @property {Array<String>} accept_description 所有视频格式描述
     * @property {Array<number>} accept_quality 所有视频格式ID
     * @property {Object.<number,String>} accept_description_dict 以ID为key的视频格式描述
     * @property {Array<number>|null|undefined} accept_audio_quality 音频格式ID（仅dash流类型有。dash流不存在为null）
     * @property {Object.<number,DurlUrl>|{video:Array<DashUrl>,audio:Array<DashUrl>|null}} data 更具体的信息
     * @typedef {Object} VideoUrlRe videoUrl 系列API返回值
     * @property {0|-1|-2|-403|-404|-500|-501} code 返回值，-1 GET请求参数不正确，-2 API调用出错，-403 WEBUI未登录，-404 未匹配到对应的API，-500 内部错误，-501 bili未登录
     * @property {string|undefined} e 错误详细信息，仅code为-500时存在
     * @property {VideoUrl|undefined} data 数据，仅code为0时存在
     * @property {errorinfo|undefined} re 错误信息，仅code为-2时存在
    */
    /**重定向至BiliBili登录页 */
    function biliredir() {
        var uri = new URL(window.location.href);
        var param = {};
        var hl = uri.searchParams.get('hl');
        if (hl != null) param['hl'] = hl;
        param['p'] = window.location.href;
        param = $.param(param);
        window.location.href = '/bililogin?' + param;
    }
    var arel = "noreferrer noopener";
    var videoq = ['真彩 HDR', '超清 4K', '高清 1080P60', '高清 720P60', '高清 1080P+', '高清 1080P', '高清 720P', '清晰 480P', '流畅 360P']
    var videoid = [125, 120, 116, 74, 112, 80, 64, 32, 16]
    var audioid = [30280, 30232, 30216];
    /**重定向至webui登录页 */
    function redir() {
        var uri = new URL(window.location.href);
        var param = {};
        var hl = uri.searchParams.get('hl');
        if (hl != null) param['hl'] = hl;
        param['p'] = window.location.href;
        param = $.param(param);
        window.location.href = '/login?' + param;
    }
    /**@type {ExtractorInfo}*/
    var info = window['info'];
    if (info.code == -1) {
        biliredir();
    }
    var main = document.getElementById('main');
    /**新建一个需要翻译的Label或者其他元素
     * @param {string} s trans字段
     * @param {string} h 元素名称（默认为label）
     * @param {string} c innerText
     * @returns {HTMLLabelElement|HTMLElement}
     */
    function createTransLabel(s, h = "label", c = "") {
        var label = document.createElement(h);
        label.className = "trans";
        label.setAttribute('trans', s);
        label.innerText = c;
        return label;
    }
    /**创建一个td
     * @param {number|string|HTMLElement|Array<(string|HTMLElement)>} i 要添加的元素或者字符串内容
     * @param {string|Array<String>|DOMTokenList} c class名称
    */
    function createTd(i = null, c = null) {
        var td = document.createElement('td');
        if (i != null) {
            if (i instanceof HTMLElement) {
                td.append(i);
            }
            else if (i instanceof Array) {
                for (var j = 0; j < i.length; j++) {
                    td.append(i[j]);
                }
            }
            else if (i.constructor.name == "String") {
                td.innerText = i;
            }
            else if (i.constructor.name == "Number") {
                td.innerText = i.toString();
            }
        }
        if (c != null) {
            if (c instanceof Array) {
                td.classList.add(c);
            }
            else if (c instanceof DOMTokenList) {
                td.classList = c;
            }
            else if (c.constructor.name == "String") {
                td.classList.add([c]);
            }
        }
        return td
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
    /**将时长转换为字符串格式
     * @param {number} t 时间（秒）
     * @returns {string}
    */
    function durtostr(t) {
        var o = [Math.floor(t / 3600), Math.floor(t % 3600 / 60), t % 60];
        if (o[0] == 0) o.shift();
        var d = [];
        for (var i = 0; i < o.length; i++) {
            var e = o[i];
            d.push(("00" + e).substr(("" + e).length));
        }
        return d.join(':');
    }
    /**根据type创建Download Method选择元素
     * @param {string} t 解析器type
     * @returns {HTMLSelectElement}
    */
    function createsel(t) {
        /**为option元素设置value
         * @param {HTMLOptionElement} h
         * @param {string|number} s
        */
        function setValue(h, s) {
            h.value = s;
            return h;
        }
        if (t == "normal") {
            var sel = document.createElement('select');
            sel.append(setValue(createTransLabel('webui.page DMME1', 'option'), 1));
            sel.append(setValue(createTransLabel('webui.page DMME2', 'option'), 2));
            sel.append(setValue(createTransLabel('webui.page DMME3', 'option'), 3));
            sel.append(setValue(createTransLabel('webui.page DMME4', 'option'), 4));
            sel.append(setValue(createTransLabel('webui.page DMME5', 'option'), 5));
            sel.append(setValue(createTransLabel('webui.page DMME6', 'option'), 6));
            sel.append(setValue(createTransLabel('webui.page DMME8', 'option'), 7));
            return sel
        }
    }
    var size_list = ['B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'];
    /**计算大小
     * @param {number} s 大小
    */
    function calsize(s) {
        var b = 0;
        while (s >= 10240 && b < 8) {
            b = b + 1;
            s = s / 1024;
        }
        return s.toFixed(2) + size_list[b];
    }
    /**计算码率
     * @param {number} s 大小（B）
     * @param {number} t 时间（毫秒）
    */
    function calbitrate(s, t) {
        var k = s * 8 / t;
        return k.toFixed(2) + "kbps";
    }
    /**计算FPS（来自B站API，不准确）
     * @param {string} s
    */
    function calfps(s) {
        var re = s.match(/^([0-9]+)(\.[0-9]*)?$/)
        if (re != null) {
            if (re[2] != null) {
                re[2] = re[2].substr(0, 4);
                if (re[2].length == 1) re[2] += "0";
            }
            return re.slice(1).join("") + "fps";
        }
        re = s.match(/^([0-9]+)\/([0-9]+)$/)
        if (re != null) {
            var x = re[1] - 1 + 1;
            var y = re[2] - 1 + 1;
            var z = x / y;
            return z.toFixed(3) + "(" + s + ")fps";
        }
        return s + "fps";
    }
    /**毫秒转秒
     * @param {number} t
    */
    function mstos(t) {
        return (t / 1000).toFixed(3);
    }
    /**创建页面底部图质选择条*/
    function ctoolbarvqsel() {
        var sel = document.createElement('select');
        /**@type {HTMLOptionElement}*/
        var ops = createTransLabel('webui.page ASNOW', 'option');
        ops.value = 'asnow';
        sel.append(ops);
        ops = createTransLabel("webui.page DFE", "option");
        ops.value = 'dfe';
        sel.append(ops);
        for (var i = 0; i < videoq.length; i++) {
            var tsl = 'bili.videodownload ' + videoq[i];
            ops = createTransLabel(tsl, 'option');
            ops.value = videoid[i];
            sel.append(ops);
            ops = document.createElement('option');
            ops.append(createTransLabel(tsl));
            ops.append('(avc)')
            ops.value = videoid[i] + ',avc';
            sel.append(ops);
            ops = document.createElement('option');
            ops.append(createTransLabel(tsl));
            ops.append('(hev)')
            ops.value = videoid[i] + ',hev';
            sel.append(ops);
        }
        sel.addEventListener('input', toolbarvq_input)
        return sel;
    }
    /**把id,codec分开
     * @param {string} vqs
     * @returns {[vq: number, codec: string]}
    */
    function splitvqs(vqs) {
        var s = vqs.split(',');
        if (s.length > 2) {
            s = [s[0], s.slice(1).join()];
        }
        else if (s.length == 1) {
            s = [s[0], null];
        }
        s[0] = s[0] - 1 + 1;
        return s
    }
    /**根据目标图质和实际有的列表选择最终图质
     * @param {Array<number>} avq 实际的图质列表
     * @param {number} vq 目标图质
    */
    function getlowq(avq, vq) {
        var vqi = videoid.indexOf(vq);
        var avqi = [];
        for (var i = 0; i < avq.length; i++) {
            var t = videoid.indexOf(avq[i]);
            if (t > -1) avqi.push(t);
        }
        for (var i = 0; i < avqi.length; i++) {
            if (avqi[i] >= vqi) break;
        }
        return videoid[avqi[i]];
    }
    function toolbarvq_input() {
        var se = toolbarvqsel.value;
        if (se == "asnow") return;
        /**@type {HTMLCollectionOf<HTMLInputElement>} */
        var selc = document.getElementsByClassName('sel');
        for (var i = 0; i < selc.length; i++) {
            var sel = selc[i];
            if (sel.checked) {
                if (info.type == "normal") {
                    toolbarvqnor(videourl[i], i, se);
                }
            }
        }
    }
    /**创建页面底部音质选择条*/
    function ctoolbaraqsel() {
        var sel = document.createElement('select');
        /**@type {HTMLOptionElement}*/
        var ops = createTransLabel('webui.page ASNOW', 'option');
        ops.value = 'asnow';
        sel.append(ops);
        ops = createTransLabel("webui.page DFE", "option");
        ops.value = 'dfe';
        sel.append(ops);
        for (var i = 0; i < audioid.length; i++) {
            ops = document.createElement('option');
            ops.innerText = audioid[i];
            ops.value = audioid[i];
            sel.append(ops);
        }
        sel.style.display = "none";
        sel.addEventListener('input', toolbaraq_input);
        return sel;
    }
    /**根据目标图质和实际有的列表选择最终音质
     * @param {Array<number>} aaq 实际的音质列表
     * @param {number} aq 目标音质
    */
    function getlowaq(aaq, aq) {
        for (var i = 0; i < aaq.length; i++) {
            if (aq >= aaq[i]) break;
        }
        return aaq[i];
    }
    function toolbaraq_input() {
        var se = toolbaraqsel.value;
        if (se == "asnow") return;
        /**@type {HTMLCollectionOf<HTMLInputElement>} */
        var selc = document.getElementsByClassName('sel');
        for (var i = 0; i < selc.length; i++) {
            var sel = selc[i];
            if (sel.checked) {
                if (info.type == "normal") {
                    toolbaraqnor(videourl[i], i, se);
                }
            }
        }
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
    else if (info.code == -412) {
        var uri = new URL(window.location.href);
        var param = {};
        var hl = uri.searchParams.get('hl');
        if (hl != null) param['hl'] = hl;
        param['url'] = window.location.href;
        param['errorurl'] = info.errorurl;
        param = $.param(param);
        var url = '/dealwithcapcha';
        if (param != "") url += ("?" + param);
        window.location.href = url;
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
    /**@type {HTMLTableElement}*/
    var table;
    /**@type {HTMLTableRowElement} */
    var head;
    /**@type {HTMLInputElement}*/
    var all_selected;
    /**@type {Array<VideoUrl>} */
    var videourl;
    /**@type {HTMLButtonElement}*/
    var clipboardb;
    /**@type {HTMLTextAreaElement}*/
    var clipboardt;
    var clipboard;
    /**@type {HTMLDivElement} 当有选项选中时页面底部的框*/
    var toolbar;
    /**@type {HTMLLabelElement} 页面底部显示选中的数量*/
    var toolbarsn;
    /**@type {HTMLSelectElement} 页面底部批量选择画质*/
    var toolbarvqsel;
    /**@type {HTMLSelectElement} 页面底部批量选择音质*/
    var toolbaraqsel;
    function createclipboard() {
        clipboardb = document.createElement('button');
        clipboardb.className = 'clipb';
        clipboardb.setAttribute('data-clipboard-target', '#clipt');
        clipboardb.style.display = "none";
        clipboardt = document.createElement('textarea');
        clipboardt.style.width = "0";
        clipboardt.style.height = "0";
        clipboardt.style.position = "absolute";
        clipboardt.id = "clipt";
        clipboardt.innerText = '';
        main.append(clipboardt);
        main.append(clipboardb);
        clipboard = new ClipboardJS(".clipb");
    }
    function dealnormalvideo() {
        createclipboard();
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        var videoinfo = document.createElement('div');
        videoinfo.className = "videoinfo";
        main.append(videoinfo);
        var title = document.createElement('h1');
        var titlea = document.createElement('a');
        titlea.innerText = data.title;
        titlea.href = "https://www.bilibili.com/video/" + data.bvid;
        titlea.target = "_blank";
        titlea.rel = arel;
        title.append(titlea);
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
        var ip = { s: data.pic };
        img.src = "/pic/" + encodeURIComponent(data.title) + "?" + $.param(ip);
        var viewer = new Viewer(img);
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
        var upn = document.createElement('a');
        upn.innerText = data.name;
        upn.href = "https://space.bilibili.com/" + data.uid;
        upn.rel = arel;
        upn.target = "_blank";
        smallinfod2.append(upn);
        smallinfod1.append(newbr());
        smallinfod1.append(createLabel('UID:'));
        smallinfod1.append(createLabel(data.uid));
        videoinfo.append(createTransLabel('bili.PrintInfo O7'));
        videoinfo.append(createLabel(data.desc));
        var pagelist = document.createElement('div');
        pagelist.className = "pagelist";
        main.append(pagelist);
        table = document.createElement('table');
        pagelist.append(table);
        var thead = document.createElement('thead');
        var tbody = document.createElement('tbody');
        table.append(thead);
        table.append(tbody);
        head = document.createElement('tr');
        thead.append(head);
        /**全部选中复选框*/
        all_selected = document.createElement('input');
        all_selected.type = "checkbox";
        all_selected.className = "allsel";
        all_selected.addEventListener('click', allsel_click);
        head.append(createTd(all_selected));
        head.append(createTd(createTransLabel('webui.page PARTNO')));
        head.append(createTd(createTransLabel('webui.page PARTCID')));
        head.append(createTd(createTransLabel('webui.page PARTNAME')));
        head.append(createTd(createTransLabel('webui.page PARTDUR')));
        head.append(createTd(createTransLabel('webui.page DMME')));
        head.append(createTd(null, "last"));
        for (var i = 0; i < data.page.length; i++) {
            var pd = data.page[i];
            var tr = document.createElement('tr');
            if (i == data.page.length - 1) tr.className = "last";
            var sel = document.createElement('input');
            sel.type = "checkbox";
            sel.className = "sel";
            sel.setAttribute('i', i);
            sel.addEventListener('change', sel_change);
            tr.append(createTd(sel));
            tr.append(createTd(pd.page));
            tr.append(createTd(pd.cid));
            tr.append(createTd(pd.part));
            tr.append(createTd(durtostr(pd.duration)));
            tr.append(createTd(createsel(info.type)));
            tr.append(createTd(null, "last"));
            tbody.append(tr);
        }
        toolbar = document.createElement('div');
        toolbar.className = "toolbar";
        toolbar.style.display = "none";
        main.append(toolbar);
        toolbarsn = createTransLabel('webui.page SELNUM');
        toolbarsn.setAttribute('value', 0);
        toolbar.append(toolbarsn);
        toolbarvqsel = ctoolbarvqsel();
        toolbar.append(toolbarvqsel);
        toolbaraqsel = ctoolbaraqsel();
        toolbar.append(toolbaraqsel);
        transobj.deal();
        setTimeout(mainchange, 2000);
        getnormalvideourl(0);
    }
    /**获取视频URI
     * @param {number} 视频P数-1
    */
    function getnormalvideourl(i) {
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        var pages = data.page;
        if (i >= pages.length) {
            window['videourl'] = videourl;
            transobj.deal();
            setTimeout(mainchange, 2000);
            return;
        }
        var page = pages[i];
        var pa = { "aid": data.aid, "bvid": data.bvid, "cid": page.cid, "p": page.page, "vip": info.vip, "vurl": 1 }
        $.getJSON('/api/normalvideourl', pa,
            /**@param {VideoUrlRe} e*/
            (e, s) => {
                if (s != "success") {
                    transobj.deal();
                    return;
                }
                if (e.code == -1 || e.code == -404) {
                    console.error(e);
                    transobj.deal();
                    return;
                }
                if (e.code == -500) {
                    console.error(e.e);
                    transobj.deal();
                    return;
                }
                if (e.code == -2) {
                    var ef = e.re;
                    console.error(ef);
                    alert(ef.code + " " + ef.message);
                    transobj.deal();
                    return;
                }
                if (e.code == -501) {
                    biliredir();
                    return;
                }
                if (e.code == -403) {
                    redir();
                    return;
                }
                if (e.code == 0) {
                    if (videourl == null) {
                        videourl = [];
                        videourl.push(e.data);
                    }
                    else videourl.push(e.data);
                    dealnormalurl(e.data, i);
                    setTimeout(() => { getnormalvideourl(i + 1) }, 100);
                }
            })
    }
    /**处理Video Url
     * @param {VideoUrl} d 视频网址信息
     * @param {number} i P数-1
    */
    function dealnormalurl(d, i) {
        var row = table.tBodies[0].rows[i];
        var cell = row.cells[row.cells.length - 1];
        cell.setAttribute('p', i);
        if (d.type == "dash") {
            cell.append(createdashvideosel(d, i));
            if (d.data.audio != null) cell.append(createdashaudiosel(d, i));
            cell.append(createdashvideob(i));
            if (d.data.audio != null) cell.append(createdashaudiob(i));
            cell.append(createdashsel(d, i));
            cell.append(createdashb(i));
            if (d.data.audio != null) toolbaraqsel.style.display = null;
        }
        else if (d.type == "durl") {
            var durlb = createdurlvideob(d, i)
            var durlsel = createdurlvideosel(d, i, durlb)
            cell.append(durlsel);
            cell.append(durlb);
            cell.append(createdurlvideosel2(i));
            cell.append(createdurlvideob2(i));
        }
    }
    /**创建dash流的视频描述选择
     * @param {VideoUrl} d
     * @param {number} p P数-1
    */
    function createdashvideosel(d, p) {
        var sel = document.createElement('select')
        sel.id = "dashvp" + p;
        /**@type {HTMLOptionElement}*/
        var dop = createTransLabel("webui.page DFE", "option");
        dop.value = -1;
        sel.append(dop);
        /**@type {Array<DashUrl>}*/
        var viddat = d.data.video;
        for (var i = 0; i < viddat.length; i++) {
            var vd = viddat[i];
            var opi = document.createElement('option');
            opi.value = i;
            opi.append(createTransLabel("bili.videodownload " + vd.desc, "label", vd.desc));
            opi.append('(' + vd.codecs + "," + vd.width + "x" + vd.height + "," + calsize(vd.size) + "," + calbitrate(vd.size, videourl[p].timelength) + "," + calfps(vd.frame_rate) + ")");
            sel.append(opi);
        }
        sel.addEventListener('change', () => {
            /**@type {HTMLCollectionOf<HTMLInputElement>}*/
            var selc = document.getElementsByClassName('sel');
            var selb = selc[p];
            if (selb.checked) toolbarvqsel.value = 'asnow';
        })
        return sel;
    }
    /**创建dash流的音频描述选择
     * @param {VideoUrl} d
     * @param {number} p P数-1
    */
    function createdashaudiosel(d, p) {
        var sel = document.createElement('select')
        sel.id = "dashap" + p;
        /**@type {HTMLOptionElement}*/
        var dop = createTransLabel("webui.page DFE", "option");
        dop.value = -1;
        sel.append(dop);
        /**@type {Array<DashUrl>}*/
        var audat = d.data.audio;
        for (var i = 0; i < audat.length; i++) {
            var ad = audat[i];
            var opi = document.createElement('option');
            opi.value = i;
            opi.append(ad.id + "(" + ad.codecs + "," + calsize(ad.size) + "," + calbitrate(ad.size, videourl[p].timelength) + ")")
            sel.append(opi);
        }
        sel.addEventListener('change', () => {
            /**@type {HTMLCollectionOf<HTMLInputElement>}*/
            var selc = document.getElementsByClassName('sel');
            var selb = selc[p];
            if (selb.checked) toolbaraqsel.value = 'asnow';
        })
        return sel;
    }
    /**创建dash流视频轨链接复制按钮
     * @param {number} p P数-1
    */
    function createdashvideob(p) {
        /**@type {HTMLButtonElement}*/
        var bu = createTransLabel("webui.page VCB", "button");
        bu.setAttribute('p', p);
        bu.addEventListener('click', dashvideob_click);
        return bu;
    }
    /**dash流视频轨链接复制按钮鼠标单击事件*/
    function dashvideob_click() {
        /**@type {HTMLButtonElement}*/
        var bu = this;
        var p = bu.getAttribute('p') - 1 + 1;
        var id = "dashvp" + p;
        /**@type {HTMLSelectElement}*/
        var sel = document.getElementById(id);
        var i = sel.value - 1 + 1;
        if (i < 0) i = 0;
        var url = new URL(window.location.href);
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        /**@type {DashUrl}*/
        var vd = videourl[p].data.video[i];
        var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
        pa = $.param(pa)
        var uri = "/live/" + encodeURIComponent(data.title + " - " + data.page[p].part) + ".mp4?" + pa;
        var ur = new URL(uri, url.origin);
        clipboardt.value = ur.href;
        clipboardb.click();
    }
    /**创建dash流音频轨链接复制按钮
     * @param {number} p P数-1
    */
    function createdashaudiob(p) {
        /**@type {HTMLButtonElement}*/
        var bu = createTransLabel("webui.page ACB", "button");
        bu.setAttribute('p', p);
        bu.addEventListener('click', dashaudiob_click);
        return bu;
    }
    /**dash流音频轨链接复制按钮鼠标单击事件*/
    function dashaudiob_click() {
        /**@type {HTMLButtonElement}*/
        var bu = this;
        var p = bu.getAttribute('p') - 1 + 1;
        var id = "dashap" + p;
        /**@type {HTMLSelectElement}*/
        var sel = document.getElementById(id);
        var i = sel.value - 1 + 1;
        if (i < 0) i = 0;
        var url = new URL(window.location.href);
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        /**@type {DashUrl}*/
        var vd = videourl[p].data.audio[i];
        var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'audio/mp4' };
        pa = $.param(pa)
        var uri = "/live/" + encodeURIComponent(data.title + " - " + data.page[p].part) + ".m4a?" + pa;
        var ur = new URL(uri, url.origin);
        clipboardt.value = ur.href;
        clipboardb.click();
    }
    /**创建文件保存格式选择
     * @param {VideoUrl} d
     * @param {number} p P数-1
    */
    function createdashsel(d, p) {
        var sel = document.createElement('select')
        sel.id = "dashp" + p;
        sel.setAttribute('p', p);
        var opi = document.createElement('option');
        opi.value = "mpcpl";
        opi.innerText = "mpcpl";
        sel.append(opi);
        if (d.data.audio == null) {
            opi = document.createElement('option');
            opi.value = "pls";
            opi.innerText = "pls";
            sel.append(opi);
            opi = document.createElement('option');
            opi.value = "asx";
            opi.innerText = "asx";
            sel.append(opi);
            opi = document.createElement('option');
            opi.value = "xspf";
            opi.innerText = "xspf";
            sel.append(opi);
            opi = document.createElement('option');
            opi.value = "m3u8";
            opi.innerText = "m3u8";
            sel.append(opi);
        }
        return sel;
    }
    /**创建文件保存按钮
     * @param {number} p P数-1
    */
    function createdashb(p) {
        /**@type {HTMLButtonElement}*/
        var bu = createTransLabel("webui.page SMU", "button");
        bu.setAttribute('p', p);
        bu.addEventListener('click', dashb_click);
        return bu;
    }
    function dashb_click() {
        /**@type {HTMLButtonElement}*/
        var bu = this;
        var p = bu.getAttribute('p') - 1 + 1;
        var dash = videourl[p];
        var vid = "dashvp" + p;
        var id = "dashp" + p;
        /**@type {HTMLSelectElement}*/
        var vsel = document.getElementById(vid);
        /**@type {HTMLSelectElement}*/
        var sel = document.getElementById(id);
        var vi = vsel.value - 1 + 1;
        if (vi < 0) vi = 0;
        var typ = sel.value;
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        var has_audio = false;
        if (dash.data.audio != null) has_audio = true;
        if (has_audio) {
            var aid = "dashap" + p;
            /**@type {HTMLSelectElement}*/
            var asel = document.getElementById(aid);
            var ai = asel.value - 1 + 1;
            if (ai < 0) ai = 0;
        }
        if (typ == "mpcpl") {
            /**@type {DashUrl}*/
            var vd = dash.data.video[vi];
            var url = new URL(window.location.href);
            var mpc = "MPCPLAYLIST\n1,type,0\n1,label," + data.title + " - " + data.page[p].part + "\n";
            var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
            pa = $.param(pa);
            var uri = "/live/1.mp4?" + pa;
            var ur = new URL(uri, url.origin);
            mpc += ("1,filename," + ur.href + "\n");
            if (has_audio) {
                /**@type {DashUrl}*/
                var ad = dash.data.audio[ai];
                pa = { 's': ad.url[0], 'r': videourl[p].referer, 't': 'audio/mp4' };
                pa = $.param(pa);
                uri = "/live/1.m4a?" + pa;
                var ur = new URL(uri, url.origin);
                mpc += ("1,filename," + ur.href + "\n");
            }
            var mpcb = new Blob([mpc], { 'type': 'text/plain;charset=utf-8' });
            saveAs(mpcb, data.title + " - " + data.page[p].part + ".mpcpl");
        }
        else if (!has_audio && typ == "pls") {
            /**@type {DashUrl}*/
            var vd = dash.data.video[vi];
            var url = new URL(window.location.href);
            var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
            pa = $.param(pa);
            var uri = "/live/1.mp4?" + pa;
            var ur = new URL(uri, url.origin);
            var pls = "[playlist]\nFile1=" + ur.href + "\nTitle1=" + data.title + " - " + data.page[p].part + "\nNumberOfEntries=1\nVersion=2\n";
            var plsb = new Blob([pls], { 'type': 'text/plain;charset=utf-8' });
            saveAs(plsb, data.title + " - " + data.page[p].part + ".pls");
        }
        else if (!has_audio && typ == "asx") {
            /**@type {DashUrl}*/
            var vd = dash.data.video[vi];
            var url = new URL(window.location.href);
            var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
            pa = $.param(pa);
            var uri = "/live/1.mp4?" + pa;
            var ur = new URL(uri, url.origin);
            var par = new DOMParser();
            var dum = new XMLSerializer();
            /**@type {XMLDocument}*/
            var asxd = par.parseFromString('<asx  version="3.0"></asx>', 'text/xml');
            var asx = asxd.children[0];
            var title = asxd.createElement('title');
            title.append(data.title + " - " + data.page[p].part);
            asx.append(title);
            var entry = asxd.createElement('entry');
            title = asxd.createElement('title');
            title.append(data.title + " - " + data.page[p].part);
            entry.append(title);
            var ref = asxd.createElement('ref');
            ref.setAttribute('href', ur.href);
            entry.append(ref);
            asx.append(entry);
            var asxt = dum.serializeToString(asxd);
            var asxb = new Blob([asxt], { 'type': 'text/xml;charset=utf-8' });
            saveAs(asxb, data.title + " - " + data.page[p].part + ".asx");
        }
        else if (!has_audio && typ == "xspf") {
            /**@type {DashUrl}*/
            var vd = dash.data.video[vi];
            var url = new URL(window.location.href);
            var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
            pa = $.param(pa);
            var uri = "/live/1.mp4?" + pa;
            var ur = new URL(uri, url.origin);
            var par = new DOMParser();
            var dum = new XMLSerializer();
            /**@type {XMLDocument}*/
            var xspd = par.parseFromString('<playlist version="1" xmlns="http://xspf.org/ns/0/"></playlist>', 'text/xml');
            var pl = xspd.children[0];
            var tl = xspd.createElement('trackList');
            pl.append(tl);
            var t = xspd.createElement('track');
            var title = xspd.createElement('title');
            title.append(data.title + " - " + data.page[p].part);
            t.append(title);
            var loc = xspd.createElement('location');
            loc.append(ur.href);
            t.append(loc);
            tl.append(t);
            var xspt = dum.serializeToString(xspd);
            var xspb = new Blob([xspt], { 'type': 'text/xml;charset=utf-8' });
            saveAs(xspb, data.title + " - " + data.page[p].part + ".xspf");
        }
        else if (!has_audio && typ == "m3u8") {
            /**@type {DashUrl}*/
            var vd = dash.data.video[vi];
            var url = new URL(window.location.href);
            var pa = { 's': vd.url[0], 'r': videourl[p].referer, 't': 'video/mp4' };
            pa = $.param(pa);
            var uri = "/live/1.mp4?" + pa;
            var ur = new URL(uri, url.origin);
            var m3u = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXTINF:" + mstos(dash.timelength) + "," + data.title + " - " + data.page[p].part + "\n" + ur.href + "\n#EXT-X-ENDLIST\n";
            var m3ub = new Blob([m3u], { 'type': 'text/plain;charset=utf-8' });
            saveAs(m3ub, data.title + " - " + data.page[p].part + ".m3u8");
        }
    }
    /**创建durl流的视频描述选择
     * @param {VideoUrl} d
     * @param {number} p P数-1
     * @param {HTMLButtonElement} b 复制链接按钮
    */
    function createdurlvideosel(d, p, b) {
        var sel = document.createElement('select');
        sel.id = "durlp" + p;
        sel.setAttribute('p', p);
        /**@type {HTMLOptionElement}*/
        var dop = createTransLabel("webui.page DFE", "option");
        dop.value = -1;
        sel.append(dop);
        for (var i = 0; i < d.accept_quality.length; i++) {
            var q = d.accept_quality[i];
            /**@type {DurlUrl}*/
            var vd = d.data[q];
            var opi = document.createElement('option');
            opi.value = i;
            opi.append(createTransLabel('bili.videodownload ' + vd.desc, "label", vd.desc));
            opi.append('(' + calsize(vd.size) + "," + calbitrate(vd.size, videourl[p].timelength) + ")");
            if (vd.url.length > 1) opi.setAttribute('cpl', 1);
            else opi.setAttribute('cpl', 0);
            sel.append(opi);
        }
        ((b, sel) => { sel.addEventListener('change', () => { durlvideosel_change(b, sel); }) })(b, sel);
        return sel;
    }
    /**durl流的视频描述选择变化
     * @param {HTMLButtonElement} b 复制链接按钮
     * @param {HTMLSelectElement} sel sel元素
    */
    function durlvideosel_change(b, sel) {
        var op = sel.selectedOptions[0];
        var i = op.value - 1 + 1;
        var p = sel.getAttribute('p') - 1 + 1;
        /**@type {DurlUrl}*/
        var vd = videourl[p].data[videourl[p].accept_quality[i]];
        if (vd.url.length == 1) b.disabled = false;
        else b.disabled = true;
        /**@type {HTMLCollectionOf<HTMLInputElement>}*/
        var selc = document.getElementsByClassName('sel');
        var selb = selc[p];
        if (selb.checked) toolbarvqsel.value = 'asnow';
    }
    /**创建文件保存格式选择
     * @param {number} p P数-1
    */
    function createdurlvideosel2(p) {
        var sel = document.createElement('select');
        sel.id = "durl2p" + p;
        sel.setAttribute('p', p);
        var opi = document.createElement('option');
        opi.value = "mpcpl";
        opi.innerText = "mpcpl";
        sel.append(opi);
        opi = document.createElement('option');
        opi.value = "pls";
        opi.innerText = "pls";
        sel.append(opi);
        opi = document.createElement('option');
        opi.value = "asx";
        opi.innerText = "asx";
        sel.append(opi);
        opi = document.createElement('option');
        opi.value = "xspf";
        opi.innerText = "xspf";
        sel.append(opi);
        opi = document.createElement('option');
        opi.value = "m3u8";
        opi.innerText = "m3u8";
        sel.append(opi);
        return sel;
    }
    /**创建durl流链接复制按钮
     * @param {VideoUrl} d
     * @param {number} p P数-1
    */
    function createdurlvideob(d, p) {
        /**@type {HTMLButtonElement}*/
        var bu = createTransLabel("webui.page VCB", "button");
        /**@type {DurlUrl}*/
        var vd = d.data[d.accept_quality[0]];
        if (vd.url.length > 1) bu.disabled = true;
        bu.setAttribute('p', p);
        bu.addEventListener('click', durlvideob_click);
        return bu;
    }
    /**durl流链接复制按钮鼠标单击事件*/
    function durlvideob_click() {
        /**@type {HTMLButtonElement}*/
        var bu = this;
        var p = bu.getAttribute('p') - 1 + 1;
        var id = "durlp" + p;
        /**@type {HTMLSelectElement}*/
        var sel = document.getElementById(id);
        var i = sel.value - 1 + 1;
        if (i < 0) i = 0;
        var url = new URL(window.location.href);
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        /**@type {DurlUrl}*/
        var vd = videourl[p].data[videourl[p].accept_quality[i]];
        var pa = { 's': vd.url[0].url, 'r': videourl[p].referer, 't': 'video/mp4' };
        pa = $.param(pa)
        var uri = "/live/" + encodeURIComponent(data.title + " - " + data.page[p].part) + ".flv?" + pa;
        var ur = new URL(uri, url.origin);
        clipboardt.value = ur.href;
        clipboardb.click();
    }
    /**创建durl流保存为文件按钮
     * @param {number} p P数-1
    */
    function createdurlvideob2(p) {
        /**@type {HTMLButtonElement}*/
        var bu = createTransLabel("webui.page SMU", "button");
        bu.setAttribute('p', p);
        bu.addEventListener('click', durlvideob2_click);
        return bu;
    }
    function durlvideob2_click(p) {
        /**@type {HTMLButtonElement}*/
        var bu = this;
        var p = bu.getAttribute('p') - 1 + 1;
        var id = "durlp" + p;
        var id2 = "durl2p" + p;
        /**@type {HTMLSelectElement}*/
        var sel = document.getElementById(id);
        /**@type {HTMLSelectElement}*/
        var sel2 = document.getElementById(id2);
        var i = sel.value - 1 + 1;
        if (i < 0) i = 0;
        var typ = sel2.value;
        var url = new URL(window.location.href);
        /**@type {NormalVideoData}*/
        var data = info.data.data;
        /**@type {DurlUrl}*/
        var vd = videourl[p].data[videourl[p].accept_quality[i]];
        if (typ == "mpcpl") {
            var mpc = "MPCPLAYLIST\n";
            for (var j = 0; j < vd.url.length; j++) {
                var durl = vd.url[j];
                var pa = { 's': durl.url, 'r': videourl[p].referer, 't': 'video/mp4' };
                pa = $.param(pa);
                var uri = "/live/" + durl.order + ".flv?" + pa;
                var ur = new URL(uri, url.origin);
                mpc += ((j + 1) + ",type,0\n" + (j + 1) + ",label," + data.title + " - " + data.page[p].part + " - " + durl.order + "\n" + (j + 1) + ",filename," + ur.href + "\n")
            }
            var mpcb = new Blob([mpc], { 'type': 'text/plain;charset=utf-8' });
            saveAs(mpcb, data.title + " - " + data.page[p].part + ".mpcpl");
        }
        else if (typ == "pls") {
            var pls = "[playlist]\n";
            for (var j = 0; j < vd.url.length; j++) {
                var durl = vd.url[j];
                var pa = { 's': durl.url, 'r': videourl[p].referer, 't': 'video/mp4' };
                pa = $.param(pa);
                var uri = "/live/" + durl.order + ".flv?" + pa;
                var ur = new URL(uri, url.origin);
                pls += ("File" + (j + 1) + "=" + ur.href + "\nTitle" + (j + 1) + "=" + data.title + " - " + data.page[p].part + " - " + durl.order + "\n");
            }
            pls += ("NumberOfEntries=" + vd.url.length + "\nVersion=2\n");
            var plsb = new Blob([pls], { 'type': 'text/plain;charset=utf-8' });
            saveAs(plsb, data.title + " - " + data.page[p].part + ".pls");
        }
        else if (typ == "asx") {
            var par = new DOMParser();
            var dum = new XMLSerializer();
            /**@type {XMLDocument}*/
            var asxd = par.parseFromString('<asx  version="3.0"></asx>', 'text/xml');
            var asx = asxd.children[0];
            var title = asxd.createElement('title');
            title.append(data.title + " - " + data.page[p].part);
            asx.append(title);
            for (var j = 0; j < vd.url.length; j++) {
                var durl = vd.url[j];
                var pa = { 's': durl.url, 'r': videourl[p].referer, 't': 'video/mp4' };
                pa = $.param(pa);
                var uri = "/live/" + durl.order + ".flv?" + pa;
                var ur = new URL(uri, url.origin);
                var entry = asxd.createElement('entry');
                var title = asxd.createElement('title');
                title.append(data.title + " - " + data.page[p].part + " - " + durl.order);
                entry.append(title);
                var ref = asxd.createElement('ref');
                ref.setAttribute('href', ur.href);
                entry.append(ref);
                asx.append(entry);
            }
            var asxt = dum.serializeToString(asxd);
            var asxb = new Blob([asxt], { 'type': 'text/xml;charset=utf-8' });
            saveAs(asxb, data.title + " - " + data.page[p].part + ".asx");
        }
        else if (typ == "xspf") {
            var par = new DOMParser();
            var dum = new XMLSerializer();
            /**@type {XMLDocument}*/
            var xspd = par.parseFromString('<playlist version="1" xmlns="http://xspf.org/ns/0/"></playlist>', 'text/xml');
            var pl = xspd.children[0];
            var tl = xspd.createElement('trackList');
            pl.append(tl);
            for (var j = 0; j < vd.url.length; j++) {
                var durl = vd.url[j];
                var pa = { 's': durl.url, 'r': videourl[p].referer, 't': 'video/mp4' };
                pa = $.param(pa);
                var uri = "/live/" + durl.order + ".flv?" + pa;
                var ur = new URL(uri, url.origin);
                var t = xspd.createElement('track');
                var title = xspd.createElement('title');
                title.append(data.title + " - " + data.page[p].part + " - " + durl.order);
                t.append(title);
                var loc = xspd.createElement('location');
                loc.append(ur.href);
                t.append(loc);
                tl.append(t);
            }
            var xspt = dum.serializeToString(xspd);
            var xspb = new Blob([xspt], { 'type': 'text/xml;charset=utf-8' });
            saveAs(xspb, data.title + " - " + data.page[p].part + ".xspf");
        }
        else if (typ == "m3u8") {
            var m3u = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-PLAYLIST-TYPE:VOD\n";
            for (var j = 0; j < vd.url.length; j++) {
                var durl = vd.url[j];
                var pa = { 's': durl.url, 'r': videourl[p].referer, 't': 'video/mp4' };
                pa = $.param(pa);
                var uri = "/live/" + durl.order + ".flv?" + pa;
                var ur = new URL(uri, url.origin);
                m3u += ("#EXTINF:" + mstos(durl.length) + "," + data.title + " - " + data.page[p].part + " - " + durl.order + "\n" + ur.href + "\n");
            }
            m3u += "#EXT-X-ENDLIST\n";
            var m3ub = new Blob([m3u], { 'type': 'text/plain;charset=utf-8' });
            saveAs(m3ub, data.title + " - " + data.page[p].part + ".m3u8");
        }
    }
    /**处理选择后的变化
     * @param {VideoUrl} v
     * @param {number} i
     * @param {string} se 配置
    */
    function toolbarvqnor(v, i, se) {
        if (v.type == "dash") {
            /**@type {HTMLSelectElement}*/
            var dashvp = document.getElementById('dashvp' + i);
            if (dashvp == null) return;
            if (se == "dfe") {
                dashvp.value = -1;
                return;
            }
            var vq, codec;
            [vq, codec] = splitvqs(se);
            var avq = v.accept_quality;
            if (avq.indexOf(vq) == -1) vq = getlowq(avq, vq);
            var sl = [];
            for (var j = 0; j < v.data.video.length; j++) {
                /**@type {DashUrl}*/
                var vi = v.data.video[j];
                if (vi.id == vq) {
                    if (codec == null) {
                        dashvp.value = j;
                        return;
                    }
                    else sl.push(j);
                }
            }
            if (sl.length == 1) dashvp.value = sl[0];
            else {
                /**@type {DashUrl}*/
                var vi = v.data.video[sl[0]];
                if (vi.codecs.startsWith(codec)) dashvp.value = sl[0];
                else dashvp.value = sl[1];
            }
        }
        else if (v.type == "durl") {
            /**@type {HTMLSelectElement}*/
            var durlp = document.getElementById('durlp' + i);
            if (durlp == null) return;
            if (se == "dfe") {
                durlp.value = -1;
                return;
            }
            var vq, codec;
            [vq, codec] = splitvqs(se);
            var avq = v.accept_quality;
            if (avq.indexOf(vq) == -1) vq = getlowq(avq, vq);
            for (var j = 0; j < v.accept_quality.length; j++) {
                /**@type {DurlUrl}*/
                var vi = v.data[v.accept_quality[j]];
                if (vi.id == vq) {
                    durlp.value = j;
                    return;
                }
            }
        }
    }
    /**处理选择后的变化
     * @param {VideoUrl} v
     * @param {number} i
     * @param {string} se 配置
    */
    function toolbaraqnor(v, i, se) {
        if (v.type == "dash") {
            /**@type {HTMLSelectElement}*/
            var dashap = document.getElementById('dashap' + i);
            if (dashap == null) return;
            if (se == "dfe") {
                dashap.value = -1;
                return;
            }
            var aq = se - 1 + 1;
            var aaq = v.accept_audio_quality;
            if (aaq.indexOf(aq) == -1) aq = getlowaq(aaq, aq);
            for (var j = 0; j < v.data.audio.length; j++) {
                /**@type {DashUrl}*/
                var ai = v.data.audio[j];
                if (ai.id == aq) {
                    dashap.value = j;
                    return;
                }
            }
        }
    }
    function sel_change() {
        /**@type {HTMLInputElement}*/
        var inp = this;
        var selc = document.getElementsByClassName('sel');
        /**选中数*/
        var sel_n = 0;
        /**未选中数*/
        var nsel_n = 0;
        for (var i = 0; i < selc.length; i++) {
            /**@type {HTMLInputElement}*/
            var t = selc[i];
            if (t.checked) sel_n += 1; else nsel_n += 1;
        }
        if (sel_n > 0 && nsel_n == 0) {
            all_selected.checked = true;
            all_selected.indeterminate = false;
            all_selected.disabled = false;
        }
        else if (nsel_n > 0 && sel_n == 0) {
            all_selected.checked = false;
            all_selected.indeterminate = false;
            all_selected.disabled = false;
        }
        else if (nsel_n > 0 && sel_n > 0) {
            all_selected.checked = false;
            all_selected.indeterminate = true;
            all_selected.disabled = false;
        }
        else {
            all_selected.checked = false;
            all_selected.indeterminate = false;
            all_selected.disabled = true;
        }
        if (sel_n > 0) {
            toolbar.style.display = null;
        }
        else {
            toolbar.style.display = "none";
        }
        toolbarsn.setAttribute('value', sel_n);
    }
    /**@param {MouseEvent} e*/
    function allsel_click(e) {
        e.preventDefault();
        /**@type {HTMLInputElement}*/
        var inp = this;
        setTimeout(() => {//在调用setTimeout之前得到的inp状态是错误的
            /**@type {HTMLCollectionOf<HTMLInputElement>} */
            var selc = document.getElementsByClassName('sel');
            if (!inp.checked) {
                inp.checked = true;
                inp.indeterminate = false;
                for (var i = 0; i < selc.length; i++) {
                    selc[i].checked = true;
                }
                toolbar.style.display = null;
                toolbarsn.setAttribute('value', selc.length);
            }
            else {
                inp.checked = false;
                inp.indeterminate = false;
                for (var i = 0; i < selc.length; i++) {
                    selc[i].checked = false;
                }
                toolbar.style.display = "none";
                toolbarsn.setAttribute('value', 0);
            }
        });
    }
    /**@type {HTMLStyleElement}*/
    var sty = null;
    /**@type {HTMLStyleElement}*/
    var sty2 = null;
    var t_height = document.getElementsByClassName('topmenu first')[0].scrollHeight;
    function mainchange() {
        if (sty == null) {
            sty = document.createElement('style');
            sty2 = document.createElement('style');
            document.head.append(sty);
            document.head.append(sty2);
        }
        if (main == null) {
            main = document.getElementById('main');
            if (main == null) return;
        }
        if (img != null && smallinfod1 != null && smallinfod2 != null) {
            img.style.display = "none";
            var sm_h1 = smallinfod1.scrollHeight;
            var sm_h2 = smallinfod2.scrollHeight;
            img.height = sm_h1 > sm_h2 ? sm_h1 : sm_h2;
            img.style.display = null;
        }
        var w_height = window.innerHeight;
        if (head != null) {
            var mx = document.body.scrollLeft;
            var my = document.body.scrollTop;
            var w_width = window.innerWidth;
            sty2.innerText = "";
            var th_width = head.scrollWidth;
            sty2.innerText = ".pagelist * td.last{display:none;}";
            var th2_width = head.scrollWidth;
            if (th_width < w_width) {
                var wid = w_width - th2_width;
                sty2.innerText = ".pagelist * td.last{width:" + wid + "px;}";
            }
            else sty2.innerText = "";
            if (document.body.scrollLeft != mx || document.body.scrollTop != my) document.body.scrollTo(mx, my);
        }
        var m_height = main.scrollHeight;
        if (w_height <= (m_height + t_height)) {
            sty.innerText = "";
        }
        else {
            var top = (w_height - m_height) / 2;
            sty.innerText = "#main{top:" + top + "px;}"
        }
    }
    mainchange();
    window.addEventListener('resize', mainchange);
})
