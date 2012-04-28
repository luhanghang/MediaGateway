function getXMLHttp() {
    return Try.these(
            function() {
                return new ActiveXObject('Msxml2.XMLHTTP')
            },
            function() {
                return new ActiveXObject('Microsoft.XMLHTTP')
            },
            function() {
                return new XMLHttpRequest()
            }
            ) || false;
}

function fixImage(img, width, height) {
    var isIE = navigator.userAgent.toLowerCase().indexOf("msie") >= 0;
    if (!isIE)
        return;

    var currentSrc = img.src;

    var imgStyle = "progid:DXImageTransform.Microsoft.AlphaImageLoader(src='" + currentSrc + "', sizingMethod='scale')";
    img.src = 'images/clearpixel.gif';
    img.style.width = width + "px";
    img.style.height = height + "px";
    img.style.filter = imgStyle;
}

var navigationPages = [ "home.page", "eatures.page", "demos.page", "docs.page", "downloads.page", "about.page" ];
var navigationLinks = [ "homeLink", "featuresLink", "demosLink", "docsLink", "downloadsLink", "aboutLink" ];

function showMenuContext() {
    var currentLocation = document.location.href;
    for (var i = 0; i < navigationPages.length; i++)
        if (currentLocation.indexOf(navigationPages[i]) != -1) {
            setLinkStyle($(navigationLinks[i]));
            break;
        }
}

function setLinkStyle(link) {
    link.style.fontWeight = 'bold';
    var currentFontSize = parseInt(RicoUtil.getElementsComputedStyle(link, "fontSize", "font-size"));
    link.style.fontSize = (currentFontSize + 2) + "px";
    link.style.color = 'white';
}

function ajaxSubmit(tagID, reqURL, paras, formObj) {
    if (arguments.length == 1) {
        reqURL = 'pagecontrol.do';
        formObj = document.forms[0];
        paras = null;
    }
    if (arguments.length == 2) {
        paras = null;
    }
    if (arguments.length == 3) {
        formObj = document.forms[0];
    }
    ajaxEngine.registerAjaxText(tagID);
    ajaxEngine.registerRequest(tagID, reqURL);
    ajaxEngine.sendRequestArrayAndUpdate(tagID, convertFormObjs2Array(paras, formObj));
}

function ajaxSubmitXML(tagID, reqURL, paras, formObj) {
    if (arguments.length == 1) {
        reqURL = 'pagecontrol.do';
        formObj = document.forms[0];
        paras = null;
    }
    if (arguments.length == 2) {
        paras = null;
    }
    if (arguments.length == 3) {
        formObj = document.forms[0];
    }
    ajaxEngine.registerAjaxText(tagID);
    ajaxEngine.registerRequest(tagID, reqURL);
    ajaxEngine.sendRequestArrayAndUpdateXML(tagID, convertFormObjs2Array(paras, formObj));
}

function convertFormObjs2Array(paras, formObj) {
    var paramArray = new Array();
    var paraLen = 0;
    var d = -1;
    if (formObj) {
        if(formObj[0].tagName != "FORM"){
            formObj = new Array(formObj);
        }
        for(var x = 0; x < formObj.length; x++){
            for (var i = 0; i < formObj[x].length; i++) {
                ++d;
                var item = formObj[x][i];
                if(item.disabled){
                    paramArray[d] = 'null=null';
                    continue;
                }
                if (item.type == 'radio' || item.type == 'checkbox') {
                    if (item.checked) {
                        paramArray[d] = (item.name == ''?'undefined':item.name) + '=' + item.value.replace(/\%/g, 'ppppCCCeNNt');
                    } else {
                        paramArray[d] = 'null=null';
                    }
                } else {
                        paramArray[d] = (item.name == ''?'undefined':item.name) + '=' + item.value.replace(/\%/g, 'ppppCCCeNNt');
                }
                paramArray[d] = paramArray[d].replace(/&/g, 'ANDandAND');
            }
            paraLen += formObj[x].length;
        }
    }
    if (paras != null) {
        paras += '&';
        do {
            paramArray[paraLen++] = paras.substring(0, paras.indexOf('&'));
            paras = paras.substring(paras.indexOf('&') + 1, paras.length);
        }
        while (paras.indexOf('&') > 0)
    }
    return paramArray;
}

function abbreviate(src, length) {
    if (src.length <= length) {
        return src;
    }

    length = length - 3;
    return src.substring(0, length) + '...';
}


if (window.event) {// 修正Event的DOM
    /*
                                                            IE5                MacIE5                Mozilla                Konqueror2.2                Opera5
    event                                                yes                yes                        yes                        yes                                        yes
    event.returnValue                        yes                yes                        no                        no                                        no
    event.cancelBubble                        yes                yes                        no                        no                                        no
    event.srcElement                        yes                yes                        no                        no                                        no
    event.fromElement                        yes                yes                        no                        no                                        no

    */
    event.prototype.__defineSetter__("returnValue", function(b) {//
        if (!b)this.preventDefault();
        return b;
    });
    event.prototype.__defineSetter__("cancelBubble", function(b) {// 设置或者检索当前事件句柄的层次冒泡
        if (b)this.stopPropagation();
        return b;
    });
    event.prototype.__defineGetter__("srcElement", function() {
        var node = this.target;
        while (node.nodeType != 1)node = node.parentNode;
        return node;
    });
    event.prototype.__defineGetter__("fromElement", function() {// 返回鼠标移出的源节点
        var node;
        if (this.type == "mouseover")
            node = this.relatedTarget;
        else if (this.type == "mouseout")
            node = this.target;
        if (!node)return;
        while (node.nodeType != 1)node = node.parentNode;
        return node;
    });
    event.prototype.__defineGetter__("toElement", function() {// 返回鼠标移入的源节点
        var node;
        if (this.type == "mouseout")
            node = this.relatedTarget;
        else if (this.type == "mouseover")
            node = this.target;
        if (!node)return;
        while (node.nodeType != 1)node = node.parentNode;
        return node;
    });
    event.prototype.__defineGetter__("offsetX", function() {
        return this.layerX;
    });
    event.prototype.__defineGetter__("offsetY", function() {
        return this.layerY;
    });
}

if (window.Document) {// 修正Document的DOM
    /*
                                                            IE5                MacIE5                Mozilla                Konqueror2.2                Opera5
    document.documentElement        yes                yes                        yes                        yes                                        no
    document.activeElement                yes                null                no                        no                                        no

    */
}
if (window.Node) {// 修正Node的DOM
    /*
                                                            IE5                MacIE5                Mozilla                Konqueror2.2                Opera5
    Node.contains                                yes                yes                        no                        no                                        yes
    Node.replaceNode                        yes                no                        no                        no                                        no
    Node.removeNode                                yes                no                        no                        no                                        no
    Node.children                                yes                yes                        no                        no                                        no
    Node.hasChildNodes                        yes                yes                        yes                        yes                                        no
    Node.childNodes                                yes                yes                        yes                        yes                                        no
    Node.swapNode                                yes                no                        no                        no                                        no
    Node.currentStyle                        yes                yes                        no                        no                                        no

    */
    Node.prototype.replaceNode = function(Node) {// 替换指定节点
        this.parentNode.replaceChild(Node, this);
    }
    Node.prototype.removeNode = function(removeChildren) {// 删除指定节点
        if (removeChildren)
            return this.parentNode.removeChild(this);
        else {
            var range = document.createRange();
            range.selectNodeContents(this);
            return this.parentNode.replaceChild(range.extractContents(), this);
        }
    }
    Node.prototype.swapNode = function(Node) {// 交换节点
        var nextSibling = this.nextSibling;
        var parentNode = this.parentNode;
        Node.parentNode.replaceChild(this, Node);
        parentNode.insertBefore(Node, nextSibling);
    }
}
if (window.HTMLElement) {
    HTMLElement.prototype.__defineGetter__("all", function() {
        var a = this.getElementsByTagName("*");
        var node = this;
        a.tags = function(sTagName) {
            return node.getElementsByTagName(sTagName);
        }
        return a;
    });
    HTMLElement.prototype.__defineGetter__("parentElement", function() {
        if (this.parentNode == this.ownerDocument)return null;
        return this.parentNode;
    });
    HTMLElement.prototype.__defineGetter__("children", function() {
        var tmp = [];
        var j = 0;
        var n;
        for (var i = 0; i < this.childNodes.length; i++) {
            n = this.childNodes[i];
            if (n.nodeType == 1) {
                tmp[j++] = n;
                if (n.name) {
                    if (!tmp[n.name])
                        tmp[n.name] = [];
                    tmp[n.name][tmp[n.name].length] = n;
                }
                if (n.id)
                    tmp[n.id] = n;
            }
        }
        return tmp;
    });
    HTMLElement.prototype.__defineGetter__("currentStyle", function() {
        return this.ownerDocument.defaultView.getComputedStyle(this, null);
    });
    HTMLElement.prototype.__defineSetter__("outerHTML", function(sHTML) {
        var r = this.ownerDocument.createRange();
        r.setStartBefore(this);
        var df = r.createContextualFragment(sHTML);
        this.parentNode.replaceChild(df, this);
        return sHTML;
    });
    HTMLElement.prototype.__defineGetter__("outerHTML", function() {
        var attr;
        var attrs = this.attributes;
        var str = "<" + this.tagName;
        for (var i = 0; i < attrs.length; i++) {
            attr = attrs[i];
            if (attr.specified)
                str += " " + attr.name + '="' + attr.value + '"';
        }
        if (!this.canHaveChildren)
            return str + ">";
        return str + ">" + this.innerHTML + "</" + this.tagName + ">";
    });
    HTMLElement.prototype.__defineGetter__("canHaveChildren", function() {
        switch (this.tagName.toLowerCase()) {
            case "area":
            case "base":
            case "basefont":
            case "col":
            case "frame":
            case "hr":
            case "img":
            case "br":
            case "input":
            case "isindex":
            case "link":
            case "meta":
            case "param":
                return false;
        }
        return true;
    });

    HTMLElement.prototype.__defineSetter__("innerText", function(sText) {
        var parsedText = document.createTextNode(sText);
        this.innerHTML = parsedText;
        return parsedText;
    });
    HTMLElement.prototype.__defineGetter__("innerText", function() {
        var r = this.ownerDocument.createRange();
        r.selectNodeContents(this);
        return r.toString();
    });
    HTMLElement.prototype.__defineSetter__("outerText", function(sText) {
        var parsedText = document.createTextNode(sText);
        this.outerHTML = parsedText;
        return parsedText;
    });
    HTMLElement.prototype.__defineGetter__("outerText", function() {
        var r = this.ownerDocument.createRange();
        r.selectNodeContents(this);
        return r.toString();
    });
    HTMLElement.prototype.attachEvent = function(sType, fHandler) {
        var shortTypeName = sType.replace(/on/, "");
        fHandler._ieEmuEventHandler = function(e) {
            window.event = e;
            return fHandler();
        }
        this.addEventListener(shortTypeName, fHandler._ieEmuEventHandler, false);
    }
    HTMLElement.prototype.detachEvent = function(sType, fHandler) {
        var shortTypeName = sType.replace(/on/, "");
        if (typeof(fHandler._ieEmuEventHandler) == "function")
            this.removeEventListener(shortTypeName, fHandler._ieEmuEventHandler, false);
        else
            this.removeEventListener(shortTypeName, fHandler, true);
    }
    HTMLElement.prototype.contains = function(Node) {// 是否包含某节点
        do if (Node == this)return true;
        while (Node = Node.parentNode);
        return false;
    }
    HTMLElement.prototype.insertAdjacentElement = function(where, parsedNode) {
        switch (where) {
            case "beforeBegin":
                this.parentNode.insertBefore(parsedNode, this);
                break;
            case "afterBegin":
                this.insertBefore(parsedNode, this.firstChild);
                break;
            case "beforeEnd":
                this.appendChild(parsedNode);
                break;
            case "afterEnd":
                if (this.nextSibling)
                    this.parentNode.insertBefore(parsedNode, this.nextSibling);
                else
                    this.parentNode.appendChild(parsedNode);
                break;
        }
    }
    HTMLElement.prototype.insertAdjacentHTML = function(where, htmlStr) {
        var r = this.ownerDocument.createRange();
        r.setStartBefore(this);
        var parsedHTML = r.createContextualFragment(htmlStr);
        this.insertAdjacentElement(where, parsedHTML);
    }
    HTMLElement.prototype.insertAdjacentText = function(where, txtStr) {
        var parsedText = document.createTextNode(txtStr);
        this.insertAdjacentElement(where, parsedText);
    }
    HTMLElement.prototype.attachEvent = function(sType, fHandler) {
        var shortTypeName = sType.replace(/on/, "");
        fHandler._ieEmuEventHandler = function(e) {
            window.event = e;
            return fHandler();
        }
        this.addEventListener(shortTypeName, fHandler._ieEmuEventHandler, false);
    }
    HTMLElement.prototype.detachEvent = function(sType, fHandler) {
        var shortTypeName = sType.replace(/on/, "");
        if (typeof(fHandler._ieEmuEventHandler) == "function")
            this.removeEventListener(shortTypeName, fHandler._ieEmuEventHandler, false);
        else
            this.removeEventListener(shortTypeName, fHandler, true);
    }
}

if (window.addEventListener)
{
    if (navigator.userAgent.indexOf('AppleWebKit/') == -1)
        FixPrototypeForGecko();
}

function FixPrototypeForGecko()
{
    HTMLElement.prototype.__defineGetter__("runtimeStyle", element_prototype_get_runtimeStyle);
    window.constructor.prototype.__defineGetter__("event", window_prototype_get_event);
    Event.prototype.__defineGetter__("srcElement", event_prototype_get_srcElement);
}
function element_prototype_get_runtimeStyle()
{
    //return style instead...
    return this.style;
}
function window_prototype_get_event()
{
    return SearchEvent();
}
function event_prototype_get_srcElement()
{
    var srcElement = this.target;
    if (srcElement.nodeType != 1) {
        srcElement = srcElement.parentNode;
    }
    return srcElement;
}

function SearchEvent()
{
    //IE
    if (document.all)
        return window.event;

    var func = SearchEvent.caller;
    while (func != null)
    {
        var arg0 = func.arguments[0];
        if (arg0)
        {
            if (arg0 instanceof Event)
                return arg0;
        }
        func = func.caller;
    }
    return null;
}

// check for XPath implementation
if (document.implementation.hasFeature("XPath", "3.0"))
{
    // prototying the XMLDocument
    XMLDocument.prototype.selectNodes = function(cXPathString, xNode)
    {
        if (!xNode) {
            xNode = this;
        }

        var oNSResolver = this.createNSResolver(this.documentElement)
        var aItems = this.evaluate(cXPathString, xNode, oNSResolver,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)
        var aResult = [];
        for (var i = 0; i < aItems.snapshotLength; i++)
        {
            aResult[i] = aItems.snapshotItem(i);
        }
        return aResult;
    }

    // prototying the Element
    Element.prototype.selectNodes = function(cXPathString)
    {
        if (this.ownerDocument.selectNodes)
        {
            return this.ownerDocument.selectNodes(cXPathString, this);
        }
        else {
            throw "For XML Elements Only";
        }
    }
}

// check for XPath implementation
if (document.implementation.hasFeature("XPath", "3.0"))
{
    // prototying the XMLDocument
    XMLDocument.prototype.selectSingleNode = function(cXPathString, xNode)
    {
        if (!xNode) {
            xNode = this;
        }
        var xItems = this.selectNodes(cXPathString, xNode);
        if (xItems.length > 0)
        {
            return xItems[0];
        }
        else
        {
            return null;
        }
    }

    // prototying the Element
    Element.prototype.selectSingleNode = function(cXPathString)
    {
        if (this.ownerDocument.selectSingleNode)
        {
            return this.ownerDocument.selectSingleNode(cXPathString, this);
        }
        else {
            throw "For XML Elements Only";
        }
    }
}

function getStyleProperty(ob, prop) {
    var s = ob.currentStyle || window.getComputedStyle(ob, '') || document.defaultView.getComputedStyle(ob, '');
    return s[prop] || s.getPropertyValue(prop);
}

function setCapture(ob) {
    if (ISIE) {
        ob.setCapture();
    }
    else {
        document.captureEvents(Event.MOUSEMOVE);
    }
}

function releaseCapture(ob) {
    if (ISIE) {
        ob.releaseCapture();
    }
    else {
        document.releaseEvents(Event.MOUSEMOVE);
        document.onmousemove = null;
    }
}

String.prototype.trim = function()
{
    return this.replace(/(^[\s]*)|([\s]*$)/g, "");
}

function getNodeText(node, tag, nullVal, returnNullVal) {
    if (tag) {
        node = node.selectSingleNode(tag);
    }
    if (!node) {
        return returnNullVal?returnNullVal:"&nbsp;";
    }
    var value = node.text || node.textContent;
    if(value.trim() == '' || value == nullVal){
        return returnNullVal?returnNullVal:"&nbsp;";
    }
    return value;
}

function URLEncoding(str) {
	return str;
}

var ISIE = navigator.userAgent.toLowerCase().indexOf("msie") >= 0;
