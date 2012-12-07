var mapview = false;
var map,container;

var points = [];
var gis_array;

(function(){
function load_script(xyUrl, callback){
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = xyUrl;
    script.onload = script.onreadystatechange = function(){
        if((!this.readyState || this.readyState === "loaded" || this.readyState === "complete")){
            callback && callback();
            script.onload = script.onreadystatechange = null;
            if ( head && script.parentNode ) {
                head.removeChild( script );
            }
        }
    };
    head.insertBefore( script, head.firstChild );
}
function transMore(points,type,callback){
	var xyUrl = "http://api.map.baidu.com/ag/coord/convert?from=" + type + "&to=4&mode=1";
	var xs = [];
	var ys = [];
	var maxCnt = 20;//每次发送的最大个数
	var send = function(){
		var url = xyUrl + "&x=" + xs.join(",") + "&y=" + ys.join(",") + "&callback=callback";
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
	map = new BMap.Map("container");
	var point = new BMap.Point(116.404, 39.915);  
 	map.centerAndZoom(point, 15);
	var opts = {anchor: BMAP_ANCHOR_TOP_RIGHT};
	map.addControl(new BMap.NavigationControl(opts)); 
	get_gis_inf();
	setInterval('get_gis_inf()',1000);
}

function refresh_list() {
	$.post('/monitor/get_onlines',{}, function(result) {
		//document.getElementById("div_spot_list").innerHTML = result;
		var lights = $(".online");
		if(result == '') {
			result = new Array();
		} else {
			result = result.split(",");
		}
		for(var i = 0;i < lights.length; i++) {
			var id = lights[i].id;
			id = id.split('_')[1];
			if(jQuery.inArray(id,result) == -1) {
				lights[i].src = "/media/images/s0.png";
				lights[i].className = "offiline";
				var sp = document.getElementById("button_" + id);
				sp.className = "spot_disabled";
			}
		}
		
		for(var i = 0; i < result.length; i++) {
			var id = result[i];
			var sp = document.getElementById("button_" + id);
			if(sp.className == "spot_disabled") {
				var light = document.getElementById("light_" + id);
				light.src = "/media/images/s1.png";
				light.className = "online";
				if($(".spot_button").length > 0) {
					$(".spot_button:first").before(sp);	
				} else {
					$(".spot_disabled:first").before(sp);
				}
				sp.className = "spot_button";
			}
		}
		correctPNG();
	});
}

function get_gis_inf() {
	$.post('/monitor1/spots',{}, function(result) {
		points = [];
		map.clearOverlays();
		gis_array = eval("(" + result + ")");
		for(var i in gis_array) {
			var gis = gis_array[i].gis.split(":")[1].split(",");
			points.push(new BMap.Point(gis[1],gis[0]));
		}
		if(gis_array.length > 0) {
			magic();
		}
	});
}

function callback(xyResults){
	var xyResult = null;
	for(var index in xyResults){
		var spot = gis_array[index];
		xyResult = xyResults[index];
		if(xyResult.error != 0){continue;}
		var point = new BMap.Point(xyResult.x, xyResult.y);
		var marker = new BMap.Marker(point);
		map.addOverlay(marker);
		marker.addEventListener("click", function(){  
 			play_video(spot.name,spot.global_id);  
		});
		label = new BMap.Label(spot.name);
		label.setPosition(point);
		label.setStyle({ backgroundColor:"#005493",color:"#fff",border:"0",padding:"5px" })
		map.addOverlay(label);
		label.addEventListener("click", function(){  
 			play_video(spot.name,spot.global_id);  
		});
		map.centerAndZoom(point, 15);
	}
}

function magic(){
	BMap.Convertor.transMore(points,0,callback);
}

function toggle_mapview() {
	if(mapview = !mapview) {
		player.style.width = "400px";
		player.style.height = "345px";
		player.style.left = "5px";
		player.style.top = "5px";
	} else {
		player.style.width = "100%";
		player.style.left = "0";
		player.style.top = "0";
		adjust_size();
	}
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
