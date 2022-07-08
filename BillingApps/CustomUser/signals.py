from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from CustomUser.models import CustomUser
import os

@receiver(pre_save, sender=CustomUser)
def pass_old_profile_path_to_post_save(sender, instance, **kwargs):
	"""
		Note: The ModelState object has two attributes: 
			adding: A flag which is True if the model has not been saved to the database yet, and 
			db: A string referring to the database alias the instance was loaded from or saved to.
	"""
	if instance._state.adding and not instance.pk:
		return False
	
	try:
		old_instance = sender.objects.get(pk=instance.pk)
	except sender.DoesNotExist:
		return False
	
	# Comparing the new file with the old one
	old_pic = old_instance.profile_image
	new_pic = instance.profile_image
	if old_pic != new_pic and os.path.isfile(old_pic.path) and old_pic.filename != 'default.png':
		instance.profile_path = old_file.profile_image.path
	else:
		instance.profile_path = None


@receiver(post_save, sender=CustomUser)
def delete_old_profile(sender, instance, **kwargs):
	if instance.profile_path:
		os.remove(instance.profile_path)
