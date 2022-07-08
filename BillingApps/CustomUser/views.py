# from django.contrib import messages
# from django.http import JsonResponse
from django.urls import reverse_lazy
from django.conf import settings
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.forms import modelformset_factory
# from django.core.exceptions import ValidationError
# from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView, DeleteView
# from django.contrib.messages.views import SuccessMessageMixin
from CustomUser.models import CustomUser
from CustomUser.forms import CustomUserForm, CustomUserLoginForm
from datetime import date


today = date.today()
import re




class UserCreateView(CreateView):
	model = CustomUser
	form_class = CustomUserForm
	template_name = 'users/signup.html'
	success_url = reverse_lazy(settings.SIGNUP_SUCCESS_REDIRECT_URL)
	success_message = "%(email)s was created successfully"

	def get_context_data(self, **kwargs):
		context = super(UserCreateView, self).get_context_data(**kwargs)
		context['custom_title'] = "Signup"
		return context


class UserLoginView(LoginView):
	template_name = 'users/login.html'
	form_class = CustomUserLoginForm

	def post(self, request, *args, **kwargs):
		remember_me = request.POST.get('remember_me') == 'on'
		if remember_me:
			request.session.set_expiry(settings.KEEP_ME_LOGGED_IN_DURATION)
		else:
			request.session.set_expiry(0)

			# If value is 0, the user’s session cookie will expire when the user’s web browser is closed.
			# If value is an integer, the session will expire after that many seconds of inactivity. 
			    # For example, request.session.set_expiry(300) would make the session expire in 5 minutes.
		return super(UserLoginView, self).post(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect(settings.LOGIN_REDIRECT_URL)
		else:
			return super(UserLoginView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UserLoginView, self).get_context_data(**kwargs)
		context['custom_title'] = "Login"
		return context

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
	model = CustomUser
	template_name = "users/profile.html"


	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)
		context['custom_title'] = ''.join(['Profile (', self.request.user.full_name, ')'])
		return context

	def test_func(self):					# UserPassesTestMixin to test the object is only requested by the creator.
		obj = self.get_object()	# or else it returns a 403 Forbidden Page
		return self.request.user.pk == obj.pk			# if this valid returns True or else False


class ChangeProfileSettingsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = CustomUser
	template_name = "users/confirm_change.html"

	def get(self, request, *args, **kwargs):
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

	def get_context_data(self, **kwargs):
		context = super(ChangeProfileSettingsView, self).get_context_data(**kwargs)
		context['custom_title'] = "Create Customer"
		return context

	def test_func(self):
		obj = self.get_object()
		return self.request.user.pk == obj.pk



    # def form_valid(self, form):
    #     form.instance.status = 'completed'
    #     return super().form_valid(form),

