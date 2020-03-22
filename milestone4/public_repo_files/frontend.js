function submit_form() {  
	var textbox = document.getElementById("textbox");
	alert(textbox.value)
	// if (textbox.value == "") {
	// 	alert("Please enter a search term to proceed!");	
	// }
	// else {
	var form = document.getElementById("form");         
	var formData = new FormData(form);
	var searchParams = new URLSearchParams(formData);
	var queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest( )
	xmlHttpRqst.onload = function(e) {update_page(xmlHttpRqst.response);} 
	xmlHttpRqst.open( "GET", "/?" + queryString);
	xmlHttpRqst.send();}
// }

function update_page(response) {
	var div = document.getElementById("results");
	div.innerHTML = response;
}

function check_empty() {
	var textbox = document.getElementById("textbox");
	var radiotable = document.getElementById("radiotable");
	// if (textbox.value == "" && radiotable.checked) {
	// 	alert("Please enter a search term.");	
	// }
	// else {
		var form = document.getElementById("form")
		form.submit()
	// }
}

function openTab(tabName) {
    var i;
    var x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";  
    }
    document.getElementById(tabName).style.display = "block";  
  }
