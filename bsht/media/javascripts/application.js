function show_mask(){
	var mask = $("mask");
	mask.style.width = document.documentElement.offsetWidth + "px"; 
	mask.style.height = document.documentElement.scrollHeight + "px";
	mask.style.display = "block";
}

function hide_mask() {
	$("mask").style.display = 'none';
}

function slFocus (classname) {
	var sfEls = document.getElementsByClassName(classname);
	for (var i=0; i<sfEls.length; i++) {
		if(sfEls[i].tagName == "INPUT") {
			sfEls[i].onfocus=function() {
				this.className+=" sffocus";	
			}

			sfEls[i].onblur=function() {
				this.className=this.className.replace(new RegExp(" sffocus\\b"), "");
			}
		} else {
			sfEls[i].onmouseover = function() {
				this.className+=" sffocus";	
			}

			sfEls[i].onmouseout=function() {
				this.className=this.className.replace(new RegExp(" sffocus\\b"), "");
			}

		}
	}
}
