from django.core.exceptions import ValidationError
from .functions import filesize

from django.conf import settings



def min_max_size(image):
    # This is in MegaByte MB
    MIN_FILE_SIZE, MAX_FILE_SIZE = settings.PROFILE_IMAGE_SIZE

    SIZE_IN_BY = image.size
    SIZE_IN_KB = round(SIZE_IN_BY / 1024, 2)
    SIZE_IN_MB = round(SIZE_IN_KB / 1024, 2)

    if image:
        """
        filename is a attribute of my custom models.ImageField().
        Code is in custom_models.py
        """
        img_name = (image.filename).split('.')[0]

        if not (SIZE_IN_MB > MIN_FILE_SIZE) and img_name != 'default':
            raise ValidationError(f"The minimum file size that can be uploaded is {MIN_FILE_SIZE}MB")

        elif not (SIZE_IN_MB < MAX_FILE_SIZE) and img_name != 'default':
            raise ValidationError(f"The maximum file size that can be uploaded is {MAX_FILE_SIZE}MB")
    
        else:
            pass

        return image




# def path_and_rename(instance, filename):
#     upload_to = 'photos'
#     ext = filename.split('.')[-1]
#     # get filename
#     if instance.pk:
#         filename = '{}.{}'.format(instance.pk, ext)
#     else:
#         # set filename as random string
#         filename = '{}.{}'.format(uuid4().hex, ext)
#     # return the whole path to the file
#     return os.path.join(upload_to, filename)


# class CardInfo(models.Model):
#     id_number = models.CharField(max_length=6, primary_key=True)
#     name = models.CharField(max_length=255)
#     photo = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)