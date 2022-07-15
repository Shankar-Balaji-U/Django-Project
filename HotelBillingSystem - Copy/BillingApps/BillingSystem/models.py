from datetime import datetime   
from datetime import date
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse_lazy
from djangocustom.models.validators import NonZeroValidator
from djangocustom.models.fields import GSTField, PANField

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
	goods_tax_id = GSTField(blank=True, null=True, unique=True)
	pending_balance = models.IntegerField(default=0, blank=True)

	created_date = models.DateField(auto_now_add=True)
	created_time = models.TimeField(auto_now_add=True)
	
	def __str__(self):
		return self.industry_name

	@property
	def raw_mobile_no(self):
		national_code = [
			'+237', '+94', '+81', '+506', '+850', '+674', '+266', '+1869', '+691', '+679', '+675', '+352', '+974', '+676', '+687', '+86', '+977', '+377', '+681', '+855', '+972', '+382', '+1242', '+378', '+1849', '+886', '+1671', '+27', '+34', '+992', '+258', '+239', '+1441', '+98', '+229', '+297', '+1649', '+66', '+385', '+58', '+598', '+249', '+20', '+503', '+51', '+55', '+1876', '+872', '+670', '+359', '+213', '+252', '+60', '+509', '+599', '+963', '+381', '+1246', '+501', '+965', '+596', '+995', '+690', '+298', '+91', '+265', '+420', '+93', '+232', '+212', '+689', '+372', '+211', '+356', '+61', '+1767', '+673', '+240', '+421', '+290', '+357', '+244', '+39', '+500', '+591', '+53', '+355', '+256', '+423', '+1268', '+376', '+220', '+269', '+370', '+253', '+1758', '+260', '+672', '+245', '+268', '+95', '+998', '+227', '+65', '+257', '+967', '+238', '+32', '+374', '+685', '+263', '+56', '+594', '+49', '+1784', '+221', '+1684', '+1284', '+686', '+508', '+57', '+1670', '+597', '+48', '+250', '+971', '+54', '+236', '+677', '+973', '+248', '+1868', '+218', '+235', '+1340', '+230', '+966', '+386', '+345', '+853', '+595', '+62', '+1', '+261', '+291', '+968', '+387', '+350', '+77', '+255', '+1264', '+251', '+389', '+682', '+960', '+590', '+41', '+962', '+351', '+224', '+379', '+856', '+44', '+852', '+683', '+222', '+507', '+43', '+961', '+1939', '+233', '+996', '+92', '+375', '+267', '+242', '+63', '+354', '+678', '+505', '+45', '+7', '+358', '+82', '+373', '+225', '+216', '+64', '+970', '+993', '+234', '+692', '+226', '+254', '+246', '+84','+228', '+353', '+52', '+47', '+30', '+964', '+880', '+31', '+33', '+976', '+264', '+975', '+262', '+36', '+502', '+241', '+371', '+593', '+1473', '+994', '+40', '+380', '+90', '+231', '+504', '+1664', '+680', '+299', '+46', '+243', '+223', '+688'
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
	customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, verbose_name="Customer ID")          # many - to - on relationship 
	invoice_id = models.CharField(verbose_name="Invoice ID", max_length=20, default=get_invoiceid, editable=False) 
	bill_note = models.TextField(blank=True)
	cash_pay = models.DecimalField(verbose_name="Cash Amount", default=0, max_digits=20, decimal_places=2)
	upi_pay = models.DecimalField(verbose_name="Upi / Online Amount", default=0, max_digits=20, decimal_places=2)

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
	item_quantity = models.DecimalField(validators=[NonZeroValidator()], verbose_name="Quantity", max_digits=20, decimal_places=2)
	item_price = models.DecimalField(validators=[NonZeroValidator()], verbose_name="Price", max_digits=20, decimal_places=2)
	item_subtotal = models.DecimalField(default=0, verbose_name="Sub Total", max_digits=20, decimal_places=2)
	
	def save(self, *args, **kwargs):
		self.item_subtotal = self.item_quantity * self.item_price
		super(InvoiceItem, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.item_subtotal)


# class Payment(models.Model):
# 	customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)			# many - to - on relationship 
# 	bill_paid_amount = models.DecimalField(default=0, max_digits=20, decimal_places=2)

# 	created_date = models.DateField(auto_now_add=True)
# 	created_time = models.TimeField(auto_now_add=True)
# 	updated_date = models.DateField(auto_now=True)
# 	updated_time = models.TimeField(auto_now=True)

