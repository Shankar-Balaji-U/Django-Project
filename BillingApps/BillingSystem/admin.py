from django import forms
from django.contrib import admin
from .forms import InlineFormSet
from .models import Customer, Invoice, InvoiceItem, BillCounter
from django.utils.translation import gettext, gettext_lazy as _


class InvoiceItemAdmin(admin.TabularInline):
	model = InvoiceItem
	formset = InlineFormSet
	readonly_fields = ('item_subtotal',)
	extra=0
	min_num=1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	fieldsets = (
			(None, {'fields': ('invoice_id', 'customer_id', 'name', 'shop_name',  'bill_note', 'total_amount', 'cash_pay', 'upi_pay', 'paid_amount', 'pending_amount')}),
			(_('Important dates'), {'fields': ('created_date', 'created_time', 'updated_date', 'updated_time', 'is_updated_date')}),
		)

	search_fields = ('customer_id', 'created_date')
	ordering = ('-created_date',)
	readonly_fields = ['invoice_id', 'total_amount', 'name', 'shop_name', 'pending_amount', 'paid_amount', 'created_date', 'is_updated_date', 'created_time', 'updated_date', 'updated_time']
	list_display = ('__str__', 'customer_id', 'name', 'pending_amount', 'created_date', 'created_time')
	inlines = [InvoiceItemAdmin]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	fieldsets = (
			(None, {'fields': ('mobile_no', 'name', 'industry_name', 'goods_tax_id', 'previous_balance')}),
			(_('Important date & time'), {'fields': ('created_date', 'created_time')}),
		)

	search_fields = ('mobile_no', 'created_date')
	ordering = ('-created_date',)
	readonly_fields = ['previous_balance', 'created_date', 'created_time']
	list_display = ('__str__', 'mobile_no', 'previous_balance', 'created_date')


admin.site.register(InvoiceItem)
admin.site.register(BillCounter)
