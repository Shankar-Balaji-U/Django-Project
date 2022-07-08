from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# from datetime import datetime
# now = datetime.now()
from django.utils import timezone



PAYMENT_TYPE_CHOICES = (
	('UPI', _('UPI')),
	('Cash', _('Cash')),
	('Check', _('Check')),
	('Debit cards', _('Debit cards')),
	('Credit cards', _('Credit cards')),
	('Internet Banking', _('Internet Banking')),
)
 
class Payment(models.Model):
	from_ac = models.CharField(max_length=25, blank=True)
	to_ac = models.CharField(max_length=25, blank=True)
	transaction_id = models.CharField(max_length=255, blank=True)
	sender = models.CharField(max_length=264, null=True, blank=True)
	payment_method = models.CharField(max_length=264, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
	amount = models.IntegerField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender


class Notification(models.Model):
	status = models.BooleanField(default=False)
	title = models.CharField(max_length=264, null=True, blank=True)
	message = models.TextField()
	created_on = models.DateTimeField(null=True)

	def __str__(self):
		return self.title

	@property
	def duration(self):
		if self.created_on:
			now = timezone.now()
			return str(now - self.created_on)
		return None