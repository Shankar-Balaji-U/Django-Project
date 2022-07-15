from datetime import date
from django.dispatch import receiver
from . models import Customer, Invoice, BillCounter
from django.db.models.signals import post_save, pre_init

today = date.today()



@receiver(pre_init, sender=Invoice)
def check_bill_count(sender, **kwargs):
	last_bill = BillCounter.objects.last()
	if last_bill != None:
		if last_bill.created_date != today:
			BillCounter.objects.all().delete()
			BillCounter.objects.create()

	else:
		BillCounter.objects.create()



@receiver(post_save, sender=Invoice)
def bill_count_add(sender, created, instance, **kwargs):
	if created:
		last_bill = BillCounter.objects.last()

		if last_bill.created_date == today:
			BillCounter.objects.filter(pk=last_bill.pk).update(billno=last_bill.billno + 1)



@receiver(post_save, sender=Customer)
def pending_set_zero_on_create_customer(sender, created, instance, **kwargs):
	if created:
		Customer.objects.filter(pk=instance.pk).update(pending_balance=0)