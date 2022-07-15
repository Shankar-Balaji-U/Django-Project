from django import forms
from django.conf import settings
from django.forms import widgets
from .models import Customer, Invoice, InvoiceItem
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext, gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from djangocustom.forms.widgets import SearchInput

from django.core.exceptions import ValidationError

class ReadOnlyWidget(widgets.Widget):
	""" Some of these values are read only - just a bit of text... """
	def render(self, _, value, attrs=None):
		return value



class CustomerForm(forms.ModelForm):

	class Meta:
		model = Customer
		fields = ('__all__')

	def clean_alter_mobile_no(self):
		""" We are checking the mobile no. not to be same as alternative no.
			and the two are not already existing mobile numbers. 
			Only alt_mobile_no value is returned because we working inside a particular field. """
		mobile_no = self.cleaned_data.get('mobile_no')
		alt_mobile_no = self.cleaned_data.get('alter_mobile_no')

		try:
			customer = Customer.objects.get(mobile_no=alt_mobile_no)
			raise forms.ValidationError('Customer with this Alternate mobile no already exists as mobile no.')
		except Customer.DoesNotExist:
			pass

		if mobile_no == alt_mobile_no:
			raise forms.ValidationError('Alternative mobile no. is distinct from mobile no. field.')
		return alt_mobile_no

	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'



class InvoiceForm(forms.ModelForm):
	temp_search_bar = forms.CharField(widget=SearchInput(), required=False)
	temp_shop_name = forms.CharField(label=_('Shop name'), required=False)
	temp_name = forms.CharField(label=_('Customer name'), required=False)
	temp_gst_no = forms.CharField(label=_('GST no.'), required=False)
	temp_mobile_no = forms.CharField(label=_('Mobile no.'), required=False)
	temp_created = forms.CharField(label=_('Created date'), required=False)
	temp_pre_balance = forms.CharField(label=_('Previous balance'), required=False)

	class Meta:
		model = Invoice
		widgets = {'customer_id':forms.TextInput}
		temp_fields = ['temp_search_bar', 'temp_shop_name', 'temp_name', 'temp_gst_no', 'temp_mobile_no', 'temp_created', 'temp_pre_balance']
		fields = ['customer_id', 'bill_note', 'cash_pay', 'upi_pay'] + temp_fields

	def __init__(self, *args, **kwargs):
		super(InvoiceForm, self).__init__(*args, **kwargs)

		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
		placeholder = { 
			'temp_search_bar': 'Search customer', 
			'temp_shop_name': 'Shop Name',
			'temp_name': 'Customer Name',
			'temp_gst_no': 'Goods and Services Tax Identification Number',
			'temp_mobile_no': '+91-xxxxxxxxxx',
			'temp_created': 'DD MMM YYYY',
			'temp_pre_balance': 'Previous Balance'
		}
		self.fields['customer_id'].widget.attrs.update({'readonly': True})
		for name in self.Meta.temp_fields:
			try:
				self.fields[name].widget.attrs.update({'placeholder':placeholder[name]})
			except KeyError:
				pass
			if name == 'temp_search_bar':
				self.fields[name].widget.attrs.update({'onkeydown': 'return (event.keyCode!=13);'})
			else:
				self.fields[name].widget.attrs.update({'readonly': True})

	def clean_customer_id(self):
		""" We don't need to do: cleaned_data = super().clean()
			because there is no validation logic in the parent class. """
		customer_id = self.cleaned_data['customer_id']
		if not customer_id:
			self.fields['temp_search_bar'].widget.attrs.update({'class': 'form-control is-invalid'})
			self.fields['customer_id'].widget.attrs.update({'class': 'form-control is-invalid'})
			self.add_error('customer_id', 'Please select the customer id.') 
		return customer_id
	

class InvoiceItemForm(forms.ModelForm):
	item_name = forms.CharField(label=_('Product Name'))
	item_subtotal = forms.IntegerField(required=False, label=_('Sub Total'))

	class Meta:
		model = InvoiceItem
		fields = ['item_name', 'item_quantity', 'item_price', 'item_subtotal']
		exclude = ()

	def __init__(self, *args, **kwargs):
		super(InvoiceItemForm, self).__init__(*args, **kwargs)
		self.fields['item_name'].widget.attrs['placeholder'] = 'Enter the food name'
		self.fields['item_quantity'].widget.attrs.update({'placeholder':'Pieces', 'step': '0.25'})
		self.fields['item_price'].widget.attrs.update({'placeholder':'in ₹', 'step': '0.25'})
		self.fields['item_subtotal'].widget.attrs.update({'readonly': True, 'tabindex': -1})
		
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'



class InlineFormSet(forms.BaseInlineFormSet):
	
	def clean(self):
		delete_checked = 0
		total_forms = len(self.forms)
		try:
			for form in self.forms:
				if form.cleaned_data['DELETE']:
					delete_checked += 1

		except AttributeError:
			"""  Annoyingly, if a subform is invalid Django explicity 
					raises an AttributeError for cleaned_data """
			pass

		if (total_forms - delete_checked) < self.min_num:
			raise forms.ValidationError('Make sure atleast one row is required. Please uncheck a row before submit.')

	def __init__(self, *args, **kwargs):
		super(InlineFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False
			form.fields['DELETE'].widget.attrs.update({'class': 'form-check-input m-auto'})



InvoiceFormSet = forms.inlineformset_factory(
	Invoice, InvoiceItem, fields=('__all__'), 
	form=InvoiceItemForm, formset=InlineFormSet,
	extra=0, min_num=1, can_delete=True
)