window.onload = init;

function init() {
	$("form").onsubmit = do_submit;
	$("sign_out").onclick = do_sign_out;
	$("reboot").onclick = do_reboot;
}

function do_submit() {
	if(confirm("Do you really want to change the net config?")) {
		ajaxSubmit("netconf","/netconf/save/",null);
		//window.location = "http://" + $("ip").value.trim() + "/ip.html";
	}
}

function saved() {
}

function do_sign_out() {
	if(confirm('Are you sure?'))
	  window.location = '/sign_out/';
}

function do_reboot() {
	if(confirm("Do you really want to reboot the system?"))
		ajaxSubmit("rbt","/reboot/",null);
}

function rebooting() {
}
