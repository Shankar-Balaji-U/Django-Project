/*##############################################################################################

	totalcell.setAttribute("class","total");
	serialcell.innerHTML = ItemCounter2()+")";
	itemcell.innerHTML = food;
	qtycell.innerHTML = quantity;
	ratecell.innerHTML = rate;
	totalcell.innerHTML = quantity*rate;

	var itemno = document.getElementById('bill-table').getElementsByClassName('total');
	var amount=0;
	for(let i = 0; i < itemno.length; i++){
		amount = amount+Number(itemno[i].innerHTML);
		totalAmount(amount);
	}
}


#############################################################################################
document.getElementById('bill-form').addEventListener(			// if submit event is occur inside the form group with a particular id. it takes the argument and run the function.
	"submit", function(event) {
		event.preventDefault();
		var food = document.getElementById('food-select').value;
		var quantity = document.getElementById('quantity').value;
		document.getElementById("food-select").value = "";
		document.getElementById("quantity").value = "";
		document.getElementById("food-select").focus();
		if (food != '' && quantity != '') {
			for(var key in foodRate){
				if(food == key){
					rate  = foodRate[key];
					addRow(food, quantity, rate);
				}
			}
		}
		
	}
);



document.getElementById("food-select").addEventListener("keydown", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  console.log(event.keyCode);
  if (event.keyCode === 13) {
	// Cancel the default action, if needed
	event.preventDefault();
	// Trigger the button element with a click
	document.getElementById("quantity").focus();
  }
});



function printTable(contentId) {
	var printContents = document.getElementById(contentId).innerHTML;
	var winprint = window.open();
	winprint.document.write(printContents);
	winprint.print();
}

*/



// document.getElementsByClassName("food-total");



// function addButtonAndTotalRow() {
// 	var row = bill_table.insertRow(-1);
// 	row.setAttribute("id", "item_add_total");

// 	var serialcell = row.insertCell(0);
// 	var addbuttoncell = row.insertCell(1);
// 	var subcell = row.insertCell(2);
// 	var totalAmountcell = row.insertCell(3);

// 	addbuttoncell.innerHTML = '<button class="btn" id="add-items">Add Item</button>';
// 	subcell.colSpan = "2";
// 	subcell.innerHTML = "Total Amount";
// }
/*

document.getElementById("bill-total-amount").value = 
	var itemno = document.getElementById('bill-table').getElementsByClassName('total');
	var amount=0;
	for(let i = 0; i < itemno.length; i++){
		amount = amount+Number(itemno[i].innerHTML);
		totalAmount(amount);
	}
}
*/



var bill_table = document.getElementById("bill-table").getElementsByTagName("tbody")[0];
var bill_total_amount = document.getElementById("bill-total-amount");


function addRow() {
	localStorage.tableheight = bill_table.getElementsByTagName('tr').length;
	var tablelen = localStorage.getItem("tableheight");
	var row = bill_table.insertRow(tablelen - 1);
	row.classList.add("tr-item");

	var serialcell = row.insertCell(0);
	var itemcell = row.insertCell(1);
	var qtycell = row.insertCell(2);
	var ratecell = row.insertCell(3);
	var totalcell = row.insertCell(4);
	var buttoncell = row.insertCell(5);

	serialcell.classList.add("food-no");
	serialcell.innerHTML = `${Number(tablelen)}`;

	itemcell.classList.add("food-item");
	itemcell.innerHTML = `<input type="text" placeholder="Enter the food name" id="foodItem${Number(tablelen)}" name="food-item${Number(tablelen)}">`;

	qtycell.classList.add("food-qty");
	qtycell.innerHTML = `<input type="number" placeholder="Pieces" id="foodQuantity${Number(tablelen)}" name="food-quantity${Number(tablelen)}">`;

	ratecell.classList.add("food-rate");
	ratecell.innerHTML = `<input type="number" placeholder="in &#8377;" id="foodRate${Number(tablelen)}" name="food-rate${Number(tablelen)}">`;

	totalcell.classList.add("food-total");
	totalcell.innerHTML = `<input disabled="true" type="number" value="0" id="foodTotal${Number(tablelen)}" name="food-total${Number(tablelen)}">`;

	buttoncell.classList.add("food-remove-btn");
	buttoncell.innerHTML = '<button type="button" class="btn delButton">×</button>';

	document.getElementById(`foodQuantity${Number(tablelen)}`).addEventListener("input", function() {
		document.getElementById(`foodTotal${Number(tablelen)}`).value = document.getElementById(`foodQuantity${Number(tablelen)}`).value * document.getElementById(`foodRate${Number(tablelen)}`).value;
		addingTotal();
	}); 

	document.getElementById(`foodRate${Number(tablelen)}`).addEventListener("input", function() {
		document.getElementById(`foodTotal${Number(tablelen)}`).value = document.getElementById(`foodQuantity${Number(tablelen)}`).value * document.getElementById(`foodRate${Number(tablelen)}`).value;
		addingTotal();
	});
	document.getElementById(`foodItem${Number(tablelen)}`).focus();

	

	delRow();
}

function addingTotal() {
	var addtotallen = localStorage.getItem("tableheight");
	var food_total = document.getElementsByClassName("food-total");
	var totalamount = 0;
	for (var i = 0; i < addtotallen; i++) {
		var foodtotal = food_total[i].getElementsByTagName("input")[0];
		var totalamount = totalamount + Number(foodtotal.value);
	}
	var foodtotal = food_total;
	console.log(foodtotal.innerHTML);
	console.log(addtotallen);
	bill_total_amount.value = totalamount;
}

function delRow() {
	var del_button = document.getElementsByClassName("delButton");
	for(var i = 0; i < del_button.length; i++) {
		del_button[i].addEventListener("click", function() {
			var trlen = bill_table.getElementsByTagName("tr").length - 1;
			if(trlen != 1) {
				this.closest("tr").remove();
				localStorage.tableheight = trlen;
				reListingNo();
			}
			addingTotal(); 
		});
	}
}

addRow();
addingTotal();

function reListingNo() {
	// var td = bill_table.getElementsByTagName('td');
	for (var i = 0; i < bill_table.rows.length-1; i++) {
		bill_table.rows[i].cells[0].innerHTML = i+1; //first column
	}
	console.log("Hi");
}


var add_button = document.getElementById("add-items");
add_button.addEventListener("click", function() {
	addRow();
});
