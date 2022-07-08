from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from Notify.models import Payment, Notification


@receiver(post_save, sender=Payment)
def payment_save(sender, created, instance, **kwargs):
	if created:
		temp = Notification.objects.create(
			title='We receiver a new payment', 
			message=f'Hey, We received a pending payment amount {instance.amount}rupees from {instance.from_ac}A/C to our {instance.to_ac}A/C by {instance.payment_method}. Transaction id {instance.transaction_id}', 
			created_on=instance.created_on)


@receiver(post_save, sender=Notification)
def notify_save(sender, created, instance, **kwargs):
	if created:
		datetime = instance.created_on.strftime('%a %b %d %Y %H:%M:%S %f')
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			"payment_notify", {
				"type": "user_notification",
				"event": "New Notification",
				"title": instance.title,
				"message": instance.message,
				"created_on": datetime
			}
		)


