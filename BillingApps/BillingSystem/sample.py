from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse



class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
	model = Invoice
	template_name = 'billingsite/edit_invoice.html'
	fields =  ['customer_id', 'bill_note']

	def get_context_data(self, **kwargs):
		context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = InvoiceFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = InvoiceFormSet(instance=self.object)
		return context

    def form_valid(self, form):
        context = self.get_context_data()

        invoice_formset = context['formset']
        if invoice_formset.is_valid():
        	self.object = form.save()
        	invoice_formset.instance = self.object
        	invoice_formset.save()

        return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self, pk):
		return reverse_lazy('ViewInvoice', kwargs={'pk': pk})