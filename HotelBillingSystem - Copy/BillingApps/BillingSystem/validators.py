from django.core.validators import RegexValidator, BaseValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


MOBILE_REGEX =  "(\+)?(91)?( )?[789]\d{9}"
isMobileNo = RegexValidator(regex=MOBILE_REGEX, message="Phone number must be entered in the format: '+91 9230248493'.Up to 14 digits allowed.")