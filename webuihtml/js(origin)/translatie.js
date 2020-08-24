/**@type {Object} 存放翻译内容*/
var transobj = Object();
/**@param {string} name
 * @param {HTMLCollectionOf<HTMLElement>} list
 * @param {number} i
 * @param {(o:HTMLElement,i:number)=>null} dealwith 
*/
var gettrans = (name, list, i, dealwith) => {
    var le = list.length;
    $.getJSON('/translate/' + name, {}, (ob, stat) => {
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
window.addEventListener('load', () => {
    /**@type {HTMLCollectionOf<HTMLElement>}*/
    var list = document.getElementsByClassName('trans');
    var le = list.length;
    /** 处理每个元素
     * @param {HTMLElement} o 元素
     * @param {number} i 正在处理的元素索引*/
    function dealwith(o, i) {
        var a = o.getAttribute('trans');
        if (a != null) {
            var l = a.split(' ');
            if (transobj.hasOwnProperty(l[0])) {
                /**@type {Object} 翻译词典*/
                var obj2 = transobj[l[0]];
                if (obj2.hasOwnProperty(l[1])) {
                    o.innerText = obj2[l[1]]
                    if (i < le - 1) {
                        setTimeout(() => { dealwith(list[i + 1], i + 1); }, 10);
                    }
                }
                else {
                    console.warn(o);
                    console.warn('This object do not have translated text.')
                }
            }
            else {
                gettrans(l[0], list, i, dealwith);
            }
        }
        else {
            console.warn(o);
            console.warn('This object do not have trans attribute.')
        }
    }
    if (le > 0) {
        dealwith(list[0], 0);
    }
})
