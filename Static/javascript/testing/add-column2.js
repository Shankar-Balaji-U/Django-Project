
var bill_table = document.getElementById("bill-table").getElementsByTagName("tbody")[0];
var bill_total_amount = document.getElementById("bill-total-amount");



function addingTotal() {
	var addtotallen = localStorage.getItem("tableheight");
	var food_total_input = document.getElementsByClassName("fooditem-total-input");
	var totalamount = 0;
	for (var i = 0; i < addtotallen; i++) {
		var foodtotal = food_total_input[i].value;
		var totalamount = totalamount + Number(foodtotal);
	}
	console.log(addtotallen);
	bill_total_amount.value = totalamount;
}


function addRow() {
	localStorage.tableheight = bill_table.getElementsByTagName('tr').length;
	var tablelen = localStorage.getItem("tableheight");
	var row = bill_table.insertRow(tablelen - 1); 
	row.classList.add("tr-item");
	// row.setAttribute("id","tr-item-");

	var serialcell = row.insertCell(0);
	var itemcell = row.insertCell(1);
	var qtycell = row.insertCell(2);
	var ratecell = row.insertCell(3);
	var totalcell = row.insertCell(4);
	var buttoncell = row.insertCell(5);

	serialcell.classList.add("food-no");
	serialcell.innerHTML = `${Number(tablelen)}`;

	itemcell.classList.add("food-item");
	itemcell.innerHTML = `<input type="text" placeholder="Enter the food name" class="fooditem-name-input" id="foodItem${Number(tablelen)}" name="food-item${Number(tablelen)}">`;

	qtycell.classList.add("food-qty");
	qtycell.innerHTML = `<input type="number" placeholder="Pieces" class="fooditem-qty-input" id="foodQuantity${Number(tablelen)}" name="food-quantity${Number(tablelen)}">`;

	ratecell.classList.add("food-rate");
	ratecell.innerHTML = `<input type="number" placeholder="in &#8377;" class="fooditem-rate-input" id="foodRate${Number(tablelen)}" name="food-rate${Number(tablelen)}">`;

	totalcell.classList.add("food-total");
	totalcell.innerHTML = `<input disabled="true" type="number" value="0" class="fooditem-total-input" id="foodTotal${Number(tablelen)}" name="food-total${Number(tablelen)}">`;

	buttoncell.classList.add("food-remove-btn");
	buttoncell.innerHTML = '<button type="button" class="btn delButton" onclick=delRow(event);>×</button>';

	document.getElementById(`foodQuantity${Number(tablelen)}`).addEventListener("input", function() {
		document.getElementById(`foodTotal${Number(tablelen)}`).value = document.getElementById(`foodQuantity${Number(tablelen)}`).value * document.getElementById(`foodRate${Number(tablelen)}`).value;
		addingTotal();
	}); 

	document.getElementById(`foodRate${Number(tablelen)}`).addEventListener("input", function() {
		document.getElementById(`foodTotal${Number(tablelen)}`).value = parseInt(document.getElementById(`foodQuantity${Number(tablelen)}`).value) * parseInt(document.getElementById(`foodRate${Number(tablelen)}`).value);
		addingTotal();
	});
	document.getElementById(`foodItem${Number(tablelen)}`).focus();
}


function reListingNo() {
	// var td = bill_table.getElementsByTagName('td');
	for (var i = 0; i < bill_table.rows.length-1; i++) {
		bill_table.rows[i].cells[0].innerHTML = i+1; //first column
	}
}

function delRow(event) {
	if(localStorage.tableheight != 1) {
		event.target.closest("tr").remove();
		--localStorage.tableheight;

		// document.body.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'center' });
		reListingNo();
		addingTotal();
		reNamingRows();
	} else {
		event.target.closest("tr").remove();
		--localStorage.tableheight;
		addRow();
		addingTotal();
	}
}



document.getElementById("add-items").addEventListener("click", function() {
	addRow();
});
addRow();


// itemcell.innerHTML = `<inpum-name-input" id="foodItem${Number(tablelen)}" name="food-item${Number(tablelen)}">`;

// 	qtycell.classList.add("food-qty");
// 	qtycell.innerHTML = `<input type="number" placeholder="Pieces" class="fooditem-qty-input" id="foodQuantity${Number(tablelen)}" name="food-quantity${Number(tablelen)}">`;

// 	ratecell.classList.add("food-rate");
// 	ratecell.innerHTML = `<input type="number" placeholder="in &#8377;" class="fooditem-rate-input" id="foodRate${Number(tablelen)}" name="food-rate${Number(tablelen)}">`;

// 	totalcell.classList.add("food-total");
// 	totalcell.innerHTML = `<input disabled="true" type="number" value="0" class="fooditem-total-input" id="foodTotal${Number(tablelen)}" name="food-total${Number(tablelen)}">`;


function reNamingRows() {
	tr_item = document.getElementsByClassName("tr-item");
	for(let j=0; j < tr_item.length; j++) {
		var food_item_input = tr_item[j].getElementsByClassName("food-item")[0].getElementsByTagName("input")[0];
		var food_qty_input = tr_item[j].getElementsByClassName("food-qty")[0].getElementsByTagName("input")[0];
		var food_rate_input = tr_item[j].getElementsByClassName("food-rate")[0].getElementsByTagName("input")[0];
		var food_total_input = tr_item[j].getElementsByClassName("food-total")[0].getElementsByTagName("input")[0];

		food_item_input.id = `foodItem${j+1}`;
		food_qty_input.id = `foodQuantity${j+1}`;
		food_rate_input.id = `foodRate${j+1}`;
		food_total_input.id = `foodTotal${j+1}`;

		food_item_input.name = `foodItem${j+1}`;
		food_qty_input.name = `foodQuantity${j+1}`;
		food_rate_input.name = `foodRate${j+1}`;
		food_total_input.name = `foodTotal${j+1}`;
	}
}

reNamingRows();