from django.db import models
from django.utils.translation import gettext_lazy as _
from BillingSystem.models import Customer

PAYMENT_TYPE_CHOICES = (
	('UPI', _('UPI')),
	('Cash', _('Cash')),
	('Check', _('Check')),
	('Debit cards', _('Debit cards')),
	('Credit cards', _('Credit cards')),
	('Internet Banking', _('Internet Banking')),
)

class Payment(models.Model):
	from_account = models.CharField(max_length=18, editable=False, blank=True)
	to_account = models.CharField(max_length=18, editable=False, blank=True)
	transaction_id = models.CharField(max_length=30, blank=True)
	sender = models.CharField(max_length=264, null=True, blank=True)
	payment_method = models.CharField(max_length=264, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
	amount = models.IntegerField(editable=False)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender