window.onload = init;

function init(){
	$("form").onsubmit = doSubmit;
}

function doSubmit(){
	ajaxSubmit("signin", "sign_in/",null);
}

function signIn() {
	var result = $("signin").innerHTML.trim();
	if(result == "0")
		window.location = "/netconf/";
//	else
//$("signin").innerHTML = "Invalid Password!";
}
