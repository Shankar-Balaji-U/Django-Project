from django.urls import path
from . import views



urlpatterns = [
	path('dashboard/', views.DashboardView , name='Dashboard'),
	# path('invoices/<str:name>_<int:pk>/all/', views.CustomerInvoiceListView.as_view(), name='CustomerInvoiceList'),
	
	# path('customer/all/', views.CustomerListView.as_view(), name='CustomerList'),
	path('customer/create/', views.CustomerCreateView.as_view(), name='AddCustomer'),
	# path('customer/edit/<int:pk>/', views.CustomerUpdateView.as_view(), name='EditCustomer'),
	# path('customer/view/<int:pk>/', views.CustomerDetailView.as_view(), name='ViewCustomer'),
	# path('customer/delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='DeleteCustomer'),
	
	path('invoices/all/', views.InvoiceListView.as_view(), name='InvoiceList'),
	path('invoice/create/', views.InvoiceCreateView.as_view(), name='AddInvoice'),
	path('invoice/edit/<int:pk>/', views.InvoiceUpdateView.as_view(), name='EditInvoice'),
	path('invoice/view/<int:pk>/', views.InvoiceDetailView.as_view(), name='ViewInvoice'),
	path('invoice/delete/<int:pk>/', views.InvoiceDeleteView.as_view(), name='DeleteInvoice'),
	# path('invoice/search/', views.InvoiceSearchView.as_view(), name='InvoiceSearch'),
	
	# path('instocks/all/', views.InstockListView.as_view(), name='InstockList'),
	# path('instocks/create/', views.InstockCreateView.as_view(), name='AddInstock'),
	# path('instocks/edit/<int:pk>/', views.InstockUpdateView.as_view(), name='EditInstock'),
	# path('instocks/view/<int:pk>/', views.InstockDetailView.as_view(), name='ViewInstock'),
	# path('instocks/delete/<int:pk>/', views.InstockDeleteView.as_view(), name='DeleteInstock'),


	path('get/customer/mobile_no/list/', views.CustomerMobileList.as_view(), name='CustomerMobileList'),
	path('get/customer/person/', views.CustomerData.as_view(), name='CustomerData'),
	path('myView/', views.CustomerData.as_view(), name='Sample'),
]