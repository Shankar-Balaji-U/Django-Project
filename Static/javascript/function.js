var pagehref = '', filter_name = '', filter_date = '';
const pre_order = $("#pre-order").val();
const url = $("#current-url").val();

if($("#page-no").length) {
	const page_no = $("#page-no").val();
	pagehref = `page=${page_no}&`;
}

if($("#filter-by-name").length) {
	const name = $("#filter-by-name").val();
	filter_name = `by=${name}&`;
	$('#sort-name').hide()
}

if($("#filter-by-date").length) {
	const date = $("#filter-by-date").val();
	filter_date = `on_date=${date}&`;
	$('#sort-date').hide()
}


$('#sort-name').ready(function() {
	var $this, addClass, href;

	if(pre_order == "customer_id") {
		href = `${url}?${pagehref}${filter_name}${filter_date}ordering=-customer_id`;
		addClass = "fa-solid fa-sort-up";
		$this = $(this);
	} else if(pre_order == "-customer_id") {
		href = `${url}?${pagehref}${filter_name}${filter_date}`;
		addClass = "fa-solid fa-sort-down";
		$this = $(this);
	} else {
		href = `${url}?${pagehref}${filter_name}${filter_date}ordering=customer_id`;
		addClass = "fa-solid fa-sort";
		$this = $(this);
	}
	$('#sort-name').find('.fa-solid').removeClass().addClass(addClass);
	$('#sort-name').attr('href', href);
});


$('#sort-date').ready(function() {
	var $this, addClass, href; 

	if(pre_order == "created_date") {
		href = `${url}?${pagehref}${filter_name}${filter_date}ordering=-created_date`;
		addClass = "fa-solid fa-sort-up";
		$this = $(this);
	} else if(pre_order == "-created_date") {
		href = `${url}?${pagehref}${filter_name}${filter_date}`;
		addClass = "fa-solid fa-sort-down";
		$this = $(this);
	} else {
		href = `${url}?${pagehref}${filter_name}${filter_date}ordering=created_date`;
		addClass = "fa-solid fa-sort";
		$this = $(this);
	}
	$('#sort-date').find('.fa-solid').removeClass().addClass(addClass);
	$('#sort-date').attr('href', href);
});