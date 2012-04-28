window.onload = init;

function init(){
	$("form").onsubmit = do_submit;
	var pp = new Gateway_Properties();
	pp.load();
}

function do_submit(){
	ajaxSubmit("save","/cgi-bin/properties/save.py/",null);
}

function saved(){
}

var Gateway_Properties = Class.create();

Gateway_Properties.prototype = {

initialize:function(){
			   this.src = "/cgi-bin/properties/get_info.py/";
			   this.xml = this.createXmlDocument();
		   },

createXmlDocument:function(){
					  if (document.implementation && document.implementation.createDocument) {
						  var doc = document.implementation.createDocument("", "", null);
						  if (!doc.readyState) {
							  doc.readyState = 1;
							  doc.addEventListener("load", function () {
												   doc.readyState = 4;
												   if (typeof doc.onreadystatechange == "function")
												   doc.onreadystatechange();
												   },false);
						  }
						  return doc;
					  }

					  if(window.ActiveXObject)
						return Try.these(
										 function(){
										 return new AcvtiveXObject('MSXML2.DomDocument');
										 },
										 function(){
										 return new ActiveXObject('Microsoft.DomDocument');
										 },
										 function() {
										 return new ActiveXObject('MSXML.DomDocument');
										 },
										 function() {
										 return new ActiveXObject('MSXML3.DomDocument');
										 }
						) || false;
					  return null;
				  },

load: function() {
		  this.xml.onreadystatechange = this.fnLoadComplete.bind(this);
		  this.xml.load(this.src);
	  },

fnLoadComplete: function() {
					if (this.xml.readyState != 4)  return;
					this.dataLoaded();
					//alert(this.xml.selectSingleNode("/config/net/ip"));
				},

dataLoaded:function(){
			   var prefix = "/config/net/";	
			   var pArray = new Array("ip","mask","gateway");
			   for(var i = 0; i < pArray.length; i++) {
				   $(pArray[i]).value = this.getValue(prefix + pArray[i]);
			   }
		   },

getValue:function(node_path){
			 return getNodeText(this.xml.selectSingleNode(node_path));		 
		 }
};	
