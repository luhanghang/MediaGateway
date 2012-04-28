window.onload = init;

var cb_select_all, spot_edit, button_remove;
var cbs;

function init() {
	spot_edit = $("spot_edit");
	button_remove = $("button_remove_spots");
	cb_select_all = $("cb_select_all");
	cbs = document.getElementsByClassName("checkbox");
	cb_select_all.onclick = toggle_select_all;
	$("button_add_spot").onclick = add_spot;
	slFocus('spot');
}

function toggle_select_all() {
	for(var i = 0; i < cbs.length; i++) {
		cbs[i].checked = cb_select_all.checked;
		toggle_remove_button(cbs[i]);
	}
}

function add_spot() {
	modify_spot('None')
}

function close_spot_edit() {
	hide_mask();
	spot_edit.style.display = "none";
}

function show_spot_edit() {
	spot_edit.style.display = "block";
	spot_edit.style.left = (document.documentElement.clientWidth - eval(spot_edit.offsetWidth)) / 2 + "px";
	show_mask();
}

function modify_spot(id) {
	new Ajax.Updater('spot_edit','/spots/' + id + '/', {asynchronous:true, oncomplete:show_spot_edit()});
}


function toggle_remove_button(cb) {
	var div = $("div_" + cb.id);
	div.className = div.className.replace(new RegExp(" sselect\\b"),"");
	if(cb.checked) {
		button_remove.disabled = false;
		div.className += " sselect";
		return;
	} 

	button_remove.disabled = true;
		
	for(var i = 0; i < cbs.length; i++) {
		if(cbs[i].checked) {
			button_remove.disabled = false;
			return;
		}
	}
}

function save_spot() {
	new Ajax.Updater('spot_edit','/spots/save', {asynchronous:true, method:'post', parameters:Form.serialize('edit_form'), evalScripts: true});
}

