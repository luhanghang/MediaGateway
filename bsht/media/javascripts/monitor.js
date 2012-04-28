function init() {
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
	player.style.height = parseInt(document.getElementById("col_main").style.width) * 9 / 11 + 'px';
	if(parseInt(player.style.height) > document.documentElement.clientHeight) {
		player.style.height = (document.documentElement.clientHeight - 5) + "px";
		document.getElementById("col_main").style.width = parseInt(player.style.height) * 11 / 9 + 'px';
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
