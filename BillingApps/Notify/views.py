# import datetime
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from Notify.models import Payment, Notification
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate ,login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from datetime import date
today = date.today()

import re

def getNotification(request):
	pass


class NotificationDetailView(DetailView):
	model = Notification
	template_name = 'notification/saved_notify.html'


# class NotificationListView(ListView):
# 	model = Invoice
# 	template_name = 'billingsite/invoice_list.html'
# 	paginate_by = 50

# 	def get_queryset(self):
# 		self.is_custom_query_set = dict()
# 		queryset = super().get_queryset()
# 		get_data = self.request.GET
# 		customer_mobile = get_data.get('by')
# 		created_date = get_data.get('on_date')

# 		if customer_mobile:
# 			self.is_custom_query_set['name'] = customer_mobile
# 			customer = Customer.objects.get(mobile_no=customer_mobile)
# 			queryset = queryset.filter(customer_id=customer)
		
# 		if created_date:
# 			self.is_custom_query_set['date'] = created_date
# 			queryset = queryset.filter(created_date=created_date)

# 		return queryset

# 	def get_context_data(self, **kwargs):
# 		context = super(InvoiceListView, self).get_context_data(**kwargs)
# 		context['total_invoices'] = self.model.objects.all().count()
# 		context['ordered_by'] = self.get_ordering()
# 		context['filtered_by'] = self.is_custom_query_set
# 		return context

# 	def get_ordering(self):
# 		order = self.request.GET.get('ordering', '-invoice_id')
# 		return order


# class NotificationDeleteView(LoginRequiredMixin, DeleteView):
# 	model = Invoice
# 	success_url = reverse_lazy('InvoiceList')

# 	def get(self, *args, **kwargs):
# 		return self.post(*args, **kwargs)



# created_on = instance.created_on.strftime('%Y, %m, %d, %H, %M, %S, %f')
# date = ','.join('"%s"'%i for i in created_on)