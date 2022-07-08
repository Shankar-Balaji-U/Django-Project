from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from CustomUser.views import UserCreateView, UserLoginView, UserDetailView, ChangeProfileSettingsView

urlpatterns = [
	path('user/signup/', UserCreateView.as_view(), name='SignUp'),
	path('user/login/', UserLoginView.as_view(), name='Login'),
	path('user/profile/<str:pk>/', UserDetailView.as_view(), name='Profile'),
	path('user/profile/<str:pk>/change/', ChangeProfileSettingsView.as_view(), name='ChangeProfile'),
	path('user/logout/', LogoutView.as_view(), name='Logout'),
	# path('admission/form', views.admissionForm, name='AdmissionForm'),
	# path('admissions/applied/<int:pk>/detail/', ApplicationDetailView.as_view(), name='AppliedForm'),
	# path('admission/applied/list', ApplicationListView.as_view(), name='Login'),
	# path('admission/form/test', Form.as_view(), name='AdmissionFormCreate'),
	# path('admission/form/<int:pk>/update', AdmissionUpdateView.as_view(), name='AdmissionFormUpdate'),
]



