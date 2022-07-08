from django import forms
from django.conf import settings
from django.forms import widgets
from .models import Customer, Invoice, InvoiceItem
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext, gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

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

	class Meta:
		model = Invoice
		fields = ['customer_id', 'bill_note']

	def clean_customer_id(self):
		""" We don't need to do: cleaned_data = super().clean()
			because there is no validation logic in the parent class. """
		customer_id = self.cleaned_data['customer_id']

		if not customer_id and customer_id == 0:
			raise forms.ValidationError('Please select the customer id.')
		return customer_id



class InvoiceItemForm(forms.ModelForm):
	item_name = forms.CharField(label=_('Product Name'))
	item_subtotal = forms.IntegerField(required=False, label=_('Sub Total'))

	class Meta:
		model = InvoiceItem
		fields = ['item_name', 'item_quantity', 'item_price', 'item_subtotal']
		exclude = ()
		widgets = {
			"item_quantity": widgets.NumberInput(attrs={'step': '0.25'}),
			"item_price": widgets.NumberInput(attrs={'step': '0.25'})
		}


	def __init__(self, *args, **kwargs):
		super(InvoiceItemForm, self).__init__(*args, **kwargs)
		self.fields['item_name'].widget.attrs['placeholder'] = 'Enter the food name'
		self.fields['item_quantity'].widget.attrs['placeholder'] = 'Pieces'
		self.fields['item_price'].widget.attrs['placeholder'] = 'in ₹' 
		self.fields['item_subtotal'].widget.attrs['readonly'] = True
		self.fields['item_subtotal'].widget.attrs['tabindex'] = -1
		
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'




class InlineFormSet(forms.BaseInlineFormSet):
	
	def clean(self):
		delete_checked = 0
		total_forms = len(self.forms)
		MAX_INLINE_FORM = 1

		try:
			for form in self.forms:
				if form.cleaned_data['DELETE']:
					delete_checked += 1
		
		except AttributeError:
			"""  Annoyingly, if a subform is invalid Django explicity 
					raises an AttributeError for cleaned_data """
			pass

		if (total_forms - delete_checked) < MAX_INLINE_FORM:
			raise forms.ValidationError('Atleast one row is required. Please uncheck a row before submit.')
	

	def __init__(self, *args, **kwargs):
		super(InlineFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False



InvoiceFormSet = forms.inlineformset_factory(
	Invoice, InvoiceItem, fields=('__all__'), 
	form=InvoiceItemForm, formset = InlineFormSet,
	extra=0, min_num=1, can_delete=True
)