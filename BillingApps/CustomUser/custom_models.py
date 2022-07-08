import os
from django.db import models
from django.db.models.fields.files import ImageFieldFile, ImageField


class CustomImageFieldFile(ImageFieldFile):

	@property
	def filename(self):
		self._require_file()
		return os.path.basename(self.name)


class ImageField(ImageField):
	attr_class = CustomImageFieldFile