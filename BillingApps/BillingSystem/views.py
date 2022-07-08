# import datetime
from . models import CUSTOM_DATE_FORMAT
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from . forms import CustomerForm, InvoiceForm, InvoiceItemForm, InvoiceFormSet
from . models import Customer, Invoice, InvoiceItem, BillCounter
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin


from datetime import date
today = date.today()
import re


class CustomerMobileList(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		data = dict()
		if request.user.is_authenticated:
			customers = Customer.objects.all()
			data['mobile_no'] = [ customer.raw_mobile_no for customer in customers]

		else:
			data['message'] = "Authentication failed. You may not have permission \
						to access the site. You have to sign in to the site \
						and get back soon."

		return JsonResponse(data)


class CustomerData(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		data = dict()
		value = request.GET.get('mobile_no')
		if value:
			customer = Customer.objects.get(mobile_no=value)
			data = {
				'id':customer.pk, 'customer_name':customer.name, 
				'mobile_no':str(customer.mobile_no), 'gst_id':customer.goods_tax_id,
				'creater_date':customer.created_date.strftime(CUSTOM_DATE_FORMAT), 
				'pending':customer.pending_balance, 'industryname':customer.industry_name
			}
		else:
			data['error'] = "Please provide a mobile number."
		return JsonResponse(data, json_dumps_params={'indent': 4})


def DashboardView(request):
	social = ["facebook", "messenger", "twitter", "linkedin", "skype", "dropbox", "wordpress", "vimeo", "slideshare", "vk", "tumblr", "yahoo", "pinterest", "youtube", "reddit", "quora", "yelp", "weibo", "producthunt", "hackernews", "soundcloud", "blogger", "snapchat", "whatsapp", "wechat", "line", "medium", "vine", "slack", "instagram", "dribbble", "flickr", "foursquare", "tiktok", "behance"]

	return render(request, "billingsite/dashboard.html", {"social": social})







# ================================= Customer CRUD views ================================

class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Customer
	form_class = CustomerForm
	template_name = 'users/create_customer.html'
	success_url = reverse_lazy('AddInvoice')
	success_message = "%(name)s was created successfully"

	def get_context_data(self, **kwargs):
		context = super(CustomerCreateView, self).get_context_data(**kwargs)
		context['custom_title'] = "Create Customer"
		return context


class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Customer
	form_class = CustomerForm
	template_name = 'users/create_customer.html'
	success_url = reverse_lazy('AddInvoice')
	success_message = "%(name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(CustomerUpdateView, self).get_context_data(**kwargs)
		context['custom_title'] = "Create Customer"
		return context


class CustomerDetailView(LoginRequiredMixin, DetailView):
	model = Customer
	form_class = CustomerForm
	template_name = 'users/create_customer.html'
	success_url = reverse_lazy('AddInvoice')
	success_message = "%(name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(CustomerDetailView, self).get_context_data(**kwargs)
		context['custom_title'] = "Create Customer"
		return context


class CustomerListView(LoginRequiredMixin, ListView):
	model = Customer
	form_class = CustomerForm
	template_name = 'users/create_customer.html'
	success_url = reverse_lazy('AddInvoice')
	success_message = "%(name)s was updated successfully"

	def get_context_data(self, **kwargs):
		context = super(CustomerListView, self).get_context_data(**kwargs)
		context['custom_title'] = "Create Customer"
		return context







# ================================= Invoice CRUD views ================================

class InvoiceCreateView(LoginRequiredMixin, CreateView):
	model = Invoice
	form_class = InvoiceForm
	template_name = 'billingsite/create_invoice.html' 

	def get_context_data(self, **kwargs):
		context = super(InvoiceCreateView, self).get_context_data(**kwargs)
		context['custom_title'] = "New Invoice"
		temp = dict()	
		temp['customer_id'] = 0
		
		if self.request.POST:
			customer_id = int(self.request.POST.get('customer_id')) or False   # custom clean method.
			
			if customer_id:
				customer_object = Customer.objects.get(pk=customer_id)
				invoice_object = Invoice.objects.filter(customer_id=customer_object).order_by('-created_time').first()
				temp = {
					"customer_id": customer_id, "mobile_no": customer_object.mobile_no,
					"searched_mobile_no": customer_object.raw_mobile_no,
					"customer_name": customer_object.name, "gst_no": customer_object.goods_tax_id,
					"pre_bal": customer_object.pending_balance, "purchased_date": "No Bills",
					"created_date": customer_object.created_date.strftime(CUSTOM_DATE_FORMAT)
					}

			context['formset'] = InvoiceFormSet(self.request.POST)

		else:
			context['formset'] = InvoiceFormSet()

		context['temp'] = temp
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		context = self.get_context_data()
		customer_id = int(self.request.POST.get('customer_id'))   # custom clean method.

		if customer_id and customer_id != 0:
			customer_object = Customer.objects.get(pk=customer_id)
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			formsets = context['formset']

			with transaction.atomic():
				form.instance.customer_id = customer_object
				form.save(commit=False)

				if form.is_valid() and formsets.is_valid():
					self.object = form.save()
					messages.success(self.request, f'Invoice is Submitted.')
					return self.form_valid(form, formsets)
				else:
					return self.form_invalid(form, formsets)
			return reverse_lazy('InvoiceList')
		
		return self.render_to_response(context)

	def form_valid(self, form, formsets):
		formsets = formsets.save(commit=False)
		for formset in formsets:
			formset.invoice = self.object
			formset.save()
		return HttpResponseRedirect(self.get_success_url(self.object.pk))

	def form_invalid(self, form, formsets):
		return self.render_to_response(
			self.get_context_data(form=form, formset=formsets))

	def get_success_url(self, pk):
		return reverse_lazy('ViewInvoice', kwargs={'pk': pk})



class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
	model = Invoice
	template_name = 'billingsite/edit_invoice.html'
	fields =  ['customer_id', 'bill_note']

	def get_context_data(self, **kwargs):
		context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
		context['custom_title'] = "Edit Invoice"

		if self.request.POST:
			context['formset'] = InvoiceFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = InvoiceFormSet(instance=self.object)
		return context

	def form_valid(self, form):
		context = self.get_context_data(form=form)
		formset = context['formset']
		if formset.is_valid():
			formset.instance = self.object
			form.save()
			formset.save()
			messages.success(self.request, f'Invoice bill {self.object.customer_id} is updated successfully.')
			return HttpResponseRedirect(self.get_success_url(self.object.pk))
		else:
			return super().form_invalid(form)

	def get_success_url(self, pk):
		return reverse_lazy('ViewInvoice', kwargs={'pk': pk})



class InvoiceDetailView(DetailView):
	model = Invoice
	template_name = 'billingsite/saved_invoice.html'

	def get_context_data(self, **kwargs):
		context = super(InvoiceDetailView, self).get_context_data(**kwargs)
		context['custom_title'] = f"Invoice {self.get_object()}"
		return context


class InvoiceListView(ListView):
	model = Invoice
	template_name = 'billingsite/invoice_list.html'
	paginate_by = 50

	def get_queryset(self):
		self.searched_query = ''
		self.is_custom_query_set = dict()
		queryset = super().get_queryset()
		get_data = self.request.GET
		
		search = get_data.get('search')
		customer_mobile = get_data.get('by')
		created_date = get_data.get('on_date')

		if search and not (customer_mobile or created_date):
			self.searched_query = search
			queryset = queryset.filter(customer_id__name__icontains=search)

		if customer_mobile:
			self.is_custom_query_set['name'] = customer_mobile
			queryset = queryset.filter(customer_id__mobile_no=customer_mobile)
		
		if created_date:
			self.is_custom_query_set['date'] = created_date
			queryset = queryset.filter(created_date=created_date)

		return queryset

	def get_context_data(self, **kwargs):
		context = super(InvoiceListView, self).get_context_data(**kwargs)
		context['total_invoices'] = self.model.objects.all().count()
		context['ordered_by'] = self.get_ordering()
		context['filtered_by'] = self.is_custom_query_set
		context['search_query'] = self.searched_query
		if 'name' in self.is_custom_query_set:
			context['custom_title'] = f"Invoice list by {self.is_custom_query_set['name']}"
		elif 'date' in self.is_custom_query_set:
			context['custom_title'] = f"Invoice list on {self.is_custom_query_set['date']}"
		else:
			context['custom_title'] = f"All Invoice"
		return context

	def get_ordering(self):
		order = self.request.GET.get('ordering', '-invoice_id')
		return order


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
	model = Invoice
	success_url = reverse_lazy('InvoiceList')

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)


class InvoiceDeleteAllView(LoginRequiredMixin, DeleteView):
	model = Invoice
	success_url = reverse_lazy('InvoiceList')

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)









def create_customer():						# to create a sample customer data
	import os, json
	from django.conf import settings
	STORAGE_PATH = os.path.join(settings.MEDIA_ROOT, "")

	file_path = os.path.join(STORAGE_PATH, 'sampledata.json')

	with open(file_path, "r") as cfile:
		data = json.load(cfile)

		for i in range(len(data["gst number"])):
			name = data["gst number"][i]["name"]
			gst = data["gst number"][i]["value"]
			mobile_no = data["gst number"][i]["mobile_no"]

			Customer.objects.get_or_create(mobile_no=mobile_no, name=name, goods_tax_id=gst)













# from django.views.decorators.csrf import csrf_exempt
# a = csrf_exempt
# print(a)

# 	# To filter in date range
# 	if start_date and end_date:
# 		queryset = queryset.filter(created_date__range=(start_date, end_date))





# from faker import Faker
# fake = Faker()

# def fakedata(request):
# 	for i in range(100):
# 		pass
# 	return JsonResponse({'status':200})


# from django.shortcuts import get_object_or_404
# c = get_object_or_404(Customer, pk=None)
