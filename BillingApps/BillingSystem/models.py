from datetime import datetime   
from datetime import date
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from .validators import isGST, no_zero
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models import (
	ForeignKey, CASCADE, Model, Avg, Count, Min, Sum)

import os, re
today = date.today()


""" If you decide to change the date format in create and edit views 
	you typically need to change this value. 
	If you delete this field this will affect in views.py file
"""
CUSTOM_DATE_FORMAT = '%d %B %Y'


def _getattr_or_zero(obj, attr):
	if getattr(obj, attr) and hasattr(obj, attr):
		return getattr(obj, attr)
	else:
		return 0


def get_invoiceid():
	date = today.strftime('%Y%m%d')						# returns todays date

	bill_no = BillCounter.objects.last().billno			# returns todays bill count of the next bill.	
	return f"#INVOICE{date}-{str(bill_no).rjust(2, '0')}"


class BillCounter(models.Model):
	created_date = models.DateField(auto_now_add=True)
	billno = models.IntegerField(default=1)

	def __str__(self):
		return str(self.created_date)



class Customer(models.Model):
	name = models.CharField(max_length=50, blank=True)
	industry_name = models.CharField(max_length=50, default="Retail Customer")
	mobile_no = PhoneNumberField(unique=True)
	alter_mobile_no = PhoneNumberField(verbose_name="Alternate Mobile No", blank=True)
	goods_tax_id = models.CharField(max_length=15, blank=True, validators=[isGST], unique=True)
	pending_balance = models.IntegerField(default=0, blank=True)

	created_date = models.DateField(auto_now_add=True)
	created_time = models.TimeField(auto_now_add=True)
	
	def __str__(self):
		return self.industry_name

	@property
	def raw_mobile_no(self):
		national_code = [
			"+243","+682","+506","+225","+385","+53","+357","+420","+45","+253","+1767","+1849","+593","+503","+240","+678",
			"+856","+371","+961","+266","+231","+218","+423","+370","+352","+853","+389","+261","+265","+960","+223","+255",
			"+299","+1473","+590","+1671","+502","+44","+224","+245","+595","+509","+379","+504","+852","+36","+354","+673",
			"+356","+692","+596","+222","+230","+262","+52","+691","+373","+377","+976","+382","+1664","+212","+258","+263",
			"+264","+674","+977","+31","+599","+687","+681","+505","+227","+234","+683","+672","+1670","+250","+968","+680",
			"+93","+358","+355","+213","+1684","+376","+244","+1264","+672","+1268","+967","+374","+297","+61","+43","+994",
			"+66","+670","+228","+690","+676","+1868","+216","+90","+993","+1649","+688","+256","+380","+971","+260","+598",
			"+1869","+1758","+590","+508","+685","+378","+239","+966","+221","+381","+248","+232","+65","+421","+386","+49",
			"+359","+226","+257","+855","+237","+1","+238","+345","+236","+235","+56","+86","+61","+61","+57","+269","+242",
			"+98","+964","+353","+972","+39","+1876","+81","+44","+962","+77","+254","+686","+850","+82","+965","+996","+1",
			"+291","+372","+251","+500","+298","+679","+358","+33","+594","+689","+241","+220","+995","+1784","+233","+350",
			"+1242","+973","+880","+1246","+375","+32","+501","+229","+1441","+975","+591","+387","+267","+55","+246","+92",
			"+677","+252","+27","+211","+500","+34","+94","+249","+597","+47","+268","+46","+41","+963","+886","+992","+62",
			"+970","+507","+675","+595","+51","+63","+872","+48","+351","+1939","+974","+40","+7","+47","+262","+590","+44",
			"+998","+58","+84","+1284","+1340","+20","+64","+54","+44","+290","+30","+60","+91","+95"
		]

		test = re.compile('|'.join(map(re.escape, national_code))) 			# escape to handle metachars
		return test.sub('', str(self.mobile_no))

	@property
	def previous_bill_pending_amount(self):
		today_str = str(today.strftime(CUSTOM_DATE_FORMAT))
		date_list = []
		items = self.invoice_set.all()   #order_by('-created_date').first()
		
		for item in items:
			item_date = item.created_date.strftime(CUSTOM_DATE_FORMAT)
			date_list.append(str(item_date))
		
		date_list = list(set(date_list))
		data = [value for value in date_list if value != today_str]
		if data:
			return data[0]
		else:
			return "No purchase"

	@property
	def previous_balance(self):
		items = self.invoice_set.all()
		total_amount = 0
		for item in items:
			total_amount += item.pending_amount
		return total_amount

	def save(self, *args, **kwargs):
		super(Customer, self).save(*args, **kwargs)
		self.name = (self.name).capitalize()
		super(Customer, self).save(*args, **kwargs)


class Invoice(models.Model):
	customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)          # many - to - on relationship 
	invoice_id = models.CharField(max_length=20, default=get_invoiceid, editable=False) 
	bill_note = models.TextField(blank=True)
	cash_pay = models.DecimalField(verbose_name="Cash Amount", max_digits=20, decimal_places=2)
	upi_pay = models.DecimalField(verbose_name="Upi / Online Amount", max_digits=20, decimal_places=2)

	created_date = models.DateField(auto_now_add=True)
	created_time = models.TimeField(auto_now_add=True)
	updated_date = models.DateField(auto_now=True)
	updated_time = models.TimeField(auto_now=True)
	
	
	def is_updated_date(self):
		return self.created_date != self.updated_date
	
	@property
	def name(self):
		return self.customer_id.name

	@property
	def shop_name(self):
		return self.customer_id.industry_name

	@property
	def total_amount(self):
		items = self.invoiceitem_set.aggregate(Sum('item_subtotal'))
		return items["item_subtotal__sum"]

	@property
	def pending_amount(self):
		# return (getattr(self, "total_amount", 0))# - self.bill_paid_amount)
		return _getattr_or_zero(self, "cash_pay")
	
	@property
	def paid_amount(self):
		return _getattr_or_zero(self, "upi_pay") + _getattr_or_zero(self, "cash_pay")

	def get_absolute_url(self):
		return reverse_lazy('ViewInvoice', kwargs={'pk': self.pk})

	def __str__(self):
		return str(self.invoice_id)




class InvoiceItem(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)     # many - to - on relationship 
	item_name = models.CharField(max_length=100, verbose_name="Name")
	item_quantity = models.DecimalField(validators=[no_zero], verbose_name="Quantity", max_digits=20, decimal_places=2)
	item_price = models.DecimalField(validators=[no_zero], verbose_name="Price", max_digits=20, decimal_places=2)
	item_subtotal = models.DecimalField(default=0, verbose_name="Sub Total", max_digits=20, decimal_places=2)
	
	def save(self, *args, **kwargs):
		self.item_subtotal = self.item_quantity * self.item_price
		super(InvoiceItem, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.item_subtotal)


# class Payment(models.Model):
# 	customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)    # many - to - on relationship 
# 	bill_paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)

# 	created_date = models.DateField(auto_now_add=True)
# 	created_time = models.TimeField(auto_now_add=True)
# 	updated_date = models.DateField(auto_now=True)
# 	updated_time = models.TimeField(auto_now=True)