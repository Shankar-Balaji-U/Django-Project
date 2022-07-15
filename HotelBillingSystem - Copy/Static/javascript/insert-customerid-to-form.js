function getMobileNumberList(urlpath) {
	const origin = window.location.origin;   // Returns base URL (https://example.com)
	var abs_url = origin + urlpath;
	var data = null;
	$.ajax({
		url: abs_url,
		async: false,  
		method: "GET",
		dataType: 'json',
		success: function(response) {
		   data = response;
		}
	});
	return data;
}

function getCustomerData(urlpath) {
	const origin = window.location.origin;   // Returns base URL (https://example.com)
	var abs_url = origin + urlpath;
	var data = null;
	$.ajax({
		url: abs_url,
		async: false,  
		method: "GET",
		dataType: 'json',
		success: function(response) {
		   data = response;
		}
	});
	return data;
}