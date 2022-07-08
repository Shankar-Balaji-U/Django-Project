from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


MOBILE_REGEX =  "(\+)?(91)?( )?[789]\d{9}"
PAN_REGEX = "[A-Z]{3}[ABCEFGHJLPT]{1}[A-Z]{1}\d{4}[A-Z]{1}"
GSTIN_REGEX = "(3[0-7]|[1-2][0-9]|0[1-9])%s\d[Z]{1}[A-Z\d]{1}" % PAN_REGEX

isMobileNo = RegexValidator(regex=MOBILE_REGEX, message="Phone number must be entered in the format: '+91 9230248493'.Up to 14 digits allowed.")
isGST = RegexValidator(regex=GSTIN_REGEX, message="GST must be entered in the format: '22 AAAAA0000A 1 Z 5'.Up to 15 digits allowed.")





def no_zero(value):
	if value <= 0:
		raise ValidationError(_('Zero is not valid'), params={'value': value})




