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




# def helper_text_profile():

# 	help_texts = [
# 		f'Your image size should be between {MIN_FILE_SIZE} - {MAX_FILE_SIZE}MB',
# 		'Please your a 2 x 2 image for between resolution.'
# 	]
	
# 	help_items = [f'<li>{help_text}</li>' for help_text in help_texts]
# 	return mark_safe('<ol>{}</ol>'.format(''.join(help_items)))




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
	



class CustomUser(AbstractUser):
	"""User model."""
	username = None
	profile_path = None
	email = models.EmailField(_('email Address'), unique=True)
	profile_image = custom_models.ImageField(blank=True, 
		default=PROFILE_PATH, 
		upload_to='User profile images', 
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








#   @property
# 	def thumbnail_tag_responsive(self):
# 		img_w, img_h = THUMB_SIZE
# 		SM_THUMB_SIZE = ((img_w / 100) * 25, (img_h / 100) * 25)
# 		MD_THUMB_SIZE = ((img_w / 100) * 50, (img_h / 100) * 50)
# 		LG_THUMB_SIZE = ((img_w / 100) * 75, (img_h / 100) * 75)

# 		image_og = Image.open(self.profile_image)
# 		image_sm = Image.open(self.profile_image)
# 		image_md = Image.open(self.profile_image)
# 		image_lg = Image.open(self.profile_image)

# 		image_og.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
# 		image_sm.thumbnail(SM_THUMB_SIZE, Image.ANTIALIAS)
# 		image_md.thumbnail(MD_THUMB_SIZE, Image.ANTIALIAS)
# 		image_lg.thumbnail(LG_THUMB_SIZE, Image.ANTIALIAS)

# 		thumb_name, thumb_extension = os.path.splitext(self.profile_image.name)
# 		thumb_extension = thumb_extension.lower()

# 		if thumb_extension in ['.jpg', '.jpeg']:
# 			FTYPE = 'JPEG'
# 		elif thumb_extension == '.gif':
# 			FTYPE = 'GIF'
# 		elif thumb_extension == '.png':
# 			FTYPE = 'PNG'
# 		else:
# 			return False    # Unrecognized file type

# 		# Save thumbnail to in-memory file as StringIO
# 		temp_thumb_og = BytesIO()
# 		temp_thumb_sm = BytesIO()
# 		temp_thumb_md = BytesIO()
# 		temp_thumb_lg = BytesIO()

# 		image_og.save(temp_thumb_og, FTYPE)
# 		image_sm.save(temp_thumb_sm, FTYPE)
# 		image_md.save(temp_thumb_md, FTYPE)
# 		image_lg.save(temp_thumb_lg, FTYPE)
# 		temp_thumb_og.seek(0)
# 		temp_thumb_sm.seek(0)
# 		temp_thumb_md.seek(0)
# 		temp_thumb_lg.seek(0)

# 		try:
# 			self.og_thumbnail = "data:image/jpg;base64,{}".format(base64.b64encode(temp_thumb_og.getvalue()).decode("utf-8"))
# 		except UnicodeDecodeError:
# 			self.og_thumbnail = None

# 		try:
# 			self.sm_thumbnail = "data:image/jpg;base64,{}".format(base64.b64encode(temp_thumb_sm.getvalue()).decode("utf-8"))
# 		except UnicodeDecodeError:
# 			self.sm_thumbnail = None

# 		try:
# 			self.md_thumbnail = "data:image/jpg;base64,{}".format(base64.b64encode(temp_thumb_md.getvalue()).decode("utf-8"))
# 		except UnicodeDecodeError:
# 			self.md_thumbnail = None

# 		try:
# 			self.lg_thumbnail = "data:image/jpg;base64,{}".format(base64.b64encode(temp_thumb_lg.getvalue()).decode("utf-8"))
# 		except UnicodeDecodeError:
# 			self.lg_thumbnail = None

# 		# set save=False, otherwise it will run in an infinite loop
# 		temp_thumb_og.close()
# 		temp_thumb_sm.close()
# 		temp_thumb_md.close()
# 		temp_thumb_lg.close()

# 		img_scale = 1
# 		# aspect = self.width / self.height
# 		json_raw = {
# 						"og": self.og_thumbnail,
# 						"sm": self.sm_thumbnail,
# 						"md": self.md_thumbnail,
# 						"lg": self.lg_thumbnail,
# 					}

# 		json_string = json.dumps(json_raw)

# 		img_tag = '<div class="profile_preview"><img src="%s" data-src="%s"></div>' % (self.og_thumbnail, escape(json_string))	
# 		return mark_safe(img_tag)























# 	# Present Address DataBase Fieldsets
# 	cur_zipcode = models.CharField(max_length=6, blank=True, null=True, validators=[ZipCodeValid])
# 	cur_door_no = models.IntegerField(blank=True, null=True)
# 	cur_street = models.CharField(max_length=50, verbose_name='Street', blank=True)
# 	cur_area = models.CharField(max_length=50, verbose_name='Area', blank=True)
# 	cur_district = models.CharField(max_length=50, verbose_name='District', blank=True)
# 	cur_state = models.CharField(max_length=50, verbose_name='State', blank=True)
# 	cur_country = models.CharField(max_length=50, verbose_name='Country', blank=True)

# 	# Pemanent Address DataBase Fieldsets
# 	per_zipcode = models.CharField(max_length=6, blank=True, null=True, validators=[ZipCodeValid])
# 	per_door_no = models.IntegerField(blank=True, null=True)
# 	per_street = models.CharField(max_length=50, verbose_name='Street', blank=True)
# 	per_area = models.CharField(max_length=50, verbose_name='Area', blank=True)
# 	per_district = models.CharField(max_length=50, verbose_name='District', blank=True)
# 	per_state = models.CharField(max_length=50, verbose_name='State', blank=True)
# 	per_country = models.CharField(max_length=50, verbose_name='Country', blank=True)

# 	nationality = models.CharField(max_length=50, blank=True)
# 	mobile_no = PhoneNumberField(null=True, blank=True, unique=True, help_text='Contact mobile number')
# 	mother_tongue = models.CharField(max_length=50, blank=True)
# 	blood_group = models.IntegerField(choices=BLOODGROUP_CHOICES, default=8)
# 	marital_status = models.IntegerField(choices=MARITAL_CHOICES, default=0)
# 	community = models.IntegerField(choices=COMMUNITY_CHOICES, default=5)
# 	differential_ability = models.CharField(max_length=50, blank=True)
# 	personalId1 = models.CharField(max_length=50, blank=True)
# 	personalId2 = models.CharField(max_length=50, blank=True)
# 	community_certificate = models.FileField(upload_to='Student/Community Certificate', null=True, blank=True)
# 	SSLC_certificate = models.FileField(upload_to='Student/SSLC Certificate', null=True, blank=True)
# 	HSC_certificate = models.FileField(upload_to='Student/HSC Certificate', null=True, blank=True)
# 	desired_college = models.CharField(max_length=50, blank=True)
# 	desired_course = models.CharField(max_length=50, blank=True)


# 	def __str__(self):
# 		return self.first_name + self.last_name

# 	def save(self, *args, **kwargs):
# 		super(StudentAdmissionData, self).save(*args, **kwargs)

# 	def image_tag(self):
# 		return mark_safe('<img src="%s" class="profile_preview" width="123.89" height="159.29">' % (self.image.url))      # width 413, height 531



# class AdmissionDateNTime(models.Model):
# 	degree = models.CharField(max_length=10, choices=DEGREE_CHOICES, null=True, blank=True, default='------', unique=True)
# 	start_date_time = models.DateTimeField(null=True, blank=True)
# 	end_date_time = models.DateTimeField(null=True, blank=True)

# 	def __str__(self):
# 		return self.degree


# class User(AbstractUser):
#     """User model."""

#     username = None
#     email = models.EmailField(blank=True, null=True)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone = models.CharField(_('phone number'), validators=[phone_regex], max_length=17, unique=True) # validators should be a list
#     is_partner = models.BooleanField(default=False)
#     is_client = models.BooleanField(default=False)


#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = ['email']
	
#     objects = UserManager()



















