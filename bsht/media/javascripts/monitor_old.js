var mapview = false;
var map,container;

(function(){
function load_script(xyUrl, callback){
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = xyUrl;
    //借鉴了jQuery的script跨域方法
    script.onload = script.onreadystatechange = function(){
        if((!this.readyState || this.readyState === "loaded" || this.readyState === "complete")){
            callback && callback();
            // Handle memory leak in IE
            script.onload = script.onreadystatechange = null;
            if ( head && script.parentNode ) {
                head.removeChild( script );
            }
        }
    };
    // Use insertBefore instead of appendChild  to circumvent an IE6 bug.
    head.insertBefore( script, head.firstChild );
}
function transMore(points,type,callback){
	var xyUrl = "http://api.map.baidu.com/ag/coord/convert?from=" + type + "&to=4&mode=1";
	var xs = [];
	var ys = [];
	var maxCnt = 20;//每次发送的最大个数
	var send = function(){
		var url = xyUrl + "&x=" + xs.join(",") + "&y=" + ys.join(",") + "&callback=callback";
	    //动态创建script标签
	    load_script(url);
		xs = [];
		ys = [];
	}
    for(var index in points){
		if(index % maxCnt == 0 && index != 0){
			send();
		}
    	xs.push(points[index].lng);
    	ys.push(points[index].lat);
		if(index == points.length - 1){
			send();
		}
    }
    
}

window.BMap = window.BMap || {};
BMap.Convertor = {};
BMap.Convertor.transMore = transMore;
})();

function init() {
	container = document.getElementById("container");
	adjust_size();
	window.onresize = adjust_size;
	setInterval('refresh_list()',3000);
}

function refresh_list() {
	$.post('/monitor/spots',{}, function(result) {
		document.getElementById("div_spot_list").innerHTML = result;
		correctPNG();
	});
}

function adjust_size() {
	document.getElementById("col_main").style.width = (document.documentElement.clientWidth - 172 - 173) + 'px';
	var h = parseInt(document.getElementById("col_main").style.width) * 9 / 11 + 'px';
	if(parseInt(h) > document.documentElement.clientHeight) {
		h = (document.documentElement.clientHeight - 5) + "px";
		document.getElementById("col_main").style.width = parseInt(h) * 11 / 9 + 'px';
	}
	container.style.height = h;
	document.getElementById("div_spot_list").style.height = (parseInt(h) - 30) + "px";
	if(!mapview) {
		player.style.height = h;
	}
}

function play_video(name, global_id) {
	player.StartCallEx(name,global_id);
}

function set_player_mode(mode) {
	player.SetDisplayMode(mode);
}

function button_spot_over(b) {
	b.style.background = "url(/media/images/bd.jpg)";
}

function button_spot_out(b) {
	b.style.background = "url(/media/images/bu.jpg)";
}
