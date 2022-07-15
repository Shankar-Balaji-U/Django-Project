import os, base64, json

from PIL import Image
from io import BytesIO
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.html import escape, mark_safe
from django.core.files.base import ContentFile
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager

from CustomUser import custom_models
from CustomUser.validators import min_max_size

THUMB_SIZE = settings.THUMB_SIZE

PROFILE_PATH = settings.DEFAULT_PROFILE_IMAGE_PATH
MIN_FILE_SIZE, MAX_FILE_SIZE = settings.PROFILE_IMAGE_SIZE



class CustomUserManager(BaseUserManager):
	"""Define a model manager for User model with no username field."""
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError('User must have an email Address')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password=None, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)


		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)
	

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	name, ext = os.path.splitext(filename)
	timeformat = '%d_%m_%Y_%H_%M_%S'
	now = timezone.now()	
	edited_date = now.strftime(timeformat)
	name = instance.email_name + "_" + edited_date
	filename = ''.join([name, ext])
	return 'User profile images/{0}'.format(filename)


class CustomUser(AbstractUser):
	""" User model."""
	username = None
	profile_path = None
	email = models.EmailField(_('email Address'), unique=True)
	profile_image = custom_models.ImageField(blank=True, 
		default=PROFILE_PATH, 
		upload_to=user_directory_path, 
		help_text=_(
			f'Your image size should be between {MIN_FILE_SIZE} - {MAX_FILE_SIZE}MB. <br>'
			'Please your a 2 x 2 image for between resolution.'
		),
		validators=[min_max_size] )
	date_joined = models.DateTimeField(auto_now_add=True, help_text="Joined date in our office.")
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	@property
	def full_name(self):
		if self.first_name and self.last_name:
			return ' '.join([self.first_name, self.last_name])
		else:
			return None

	@property
	def email_name(self):
		return str(self.email).split('@')[0]

	@property
	def thumbnail_tag(self):
		image = Image.open(self.profile_image)
		image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

		thumb_name, thumb_extension = os.path.splitext(self.profile_image.name)
		thumb_extension = thumb_extension.lower()

		if thumb_extension in ['.jpg', '.jpeg']:
			FTYPE = 'JPEG'
		elif thumb_extension == '.gif':
			FTYPE = 'GIF'
		elif thumb_extension == '.png':
			FTYPE = 'PNG'
		else:
			return False    # Unrecognized file type

		# Save thumbnail to in-memory file as StringIO
		temp_thumb = BytesIO()
		image.save(temp_thumb, FTYPE)
		temp_thumb.seek(0)

		try:
			self.thumbnail = "data:image/jpg;base64,{}".format(base64.b64encode(temp_thumb.getvalue()).decode("utf-8"))
		except UnicodeDecodeError:
			self.thumbnail = None

		# set save=False, otherwise it will run in an infinite loop
		temp_thumb.close()

		img_tag = '<img src="%s" class="profile_preview" alt="Profile thumbnail">' % (self.thumbnail)
			
		return mark_safe(img_tag)

	def __str__(self):
		return self.email


class ClientSettings(models.Model):
	THEME_LIST = (
		('Theme1', _('Theme1')),
		('Theme2', _('Theme2')),
		('Theme3', _('Theme3')),
		('Theme4', _('Theme4')),
		('Theme5', _('Theme5')),
	)
	# name = models.CharField(max_length=200, blank=True, null=True)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	address = models.CharField(max_length=200, blank=True, null=True)
	pincode = models.CharField(max_length=10, blank=True, null=True)
	mobile_no = models.CharField(max_length=100, blank=True, null=True)
	pan_no = models.CharField(max_length=100, blank=True, null=True)
	theme = models.CharField(choices=THEME_LIST, max_length=100, blank=True, null=True)

	def __str__(self):
		return self.user.full_name



# class AdmissionDateNTime(models.Model):
# 	degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, null=True, blank=True, default='------', unique=True)
# 	start_date_time = models.DateTimeField(null=True, blank=True)
# 	end_date_time = models.DateTimeField(null=True, blank=True)

# 	def __str__(self):
# 		return self.degree
