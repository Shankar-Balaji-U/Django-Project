from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile


"""Checks a values validates as a GST Number.
    NOTE:
        A GST number is 15 digit alphanumeric.
        eg. 24 AAACB5343E 1 Z 7
        - First 2 digits are state code ranges 01-37
        - Next 10 digits is PAN Card number
            * First 3 are alphabets ranges from AAA-ZZZ
            * Next alphabet is either C,P,H,F,A,T,B,L,J,G,E
            * Next alphabet of Surname or Name
            * Next 4 digits range from 0001 to 9999
            * Next alphabetic check digit
        - 13th alphabets assigned based on the no. of reg. within a state
        - 14th alphabets will be Z by default
        - Last digit will be for check code. It may be an alphabet or a number.
"""
@deconstructible
class GSTINValidator:
	PAN_REGEX = r'^[A-Z]{3}[ABCEFGHJLPT]{1}[A-Z]{1}\d{4}[A-Z]{1}$'  # noqa
	GSTIN_REGEX = r'^(3[0-7]|[1-2][0-9]|0[1-9])%s\d[Z]{1}[A-Z\d]{1}$' % PAN_REGEX   # noqa
	message = _('Enter a valid value.')
	code = 'invalid'
	_regex = None
	
	def __init__(self, message=None, code=None):
		if message is not None: self.message = message
		if code is not None: self.code = code
		self._regex = _lazy_re_compile(self.GSTIN_REGEX)

	def __call__(self, value):
		"""
		Validate that the input contains a match for the regular expression.
		"""
		regex_matches = self._regex.search(self.clean(value))
		if regex_matches:
			raise ValidationError(self.message, code=self.code, params={'value': value})

	def clean(self, value):
		return str(value)



"""Checks a values validates as a PAN Number.
    NOTE:
        A PAN number is 10 digit alphanumeric.
        eg. AAA C B 5343 E
        - First 3 are alphabets ranges from AAA-ZZZ
        - Next alphabet is either C,P,H,F,A,T,B,L,J,G,E
        - Next alphabet of Surname or Name
        - Next 4 digits range from 0001 to 9999
        - Next alphabetic check digit
"""
@deconstructible
class PANValidator(GSTINValidator):

	def __init__(self, message=None, code=None):
		super().__init__(message, code)
		self._regex = _lazy_re_compile(self.PAN_REGEX)

	def __call__(self, value):
		regex_matches = self._regex.search(self.clean(value))
		if not regex_matches:
			raise ValidationError(self.message, code=self.code, params={'value': value})


p = PANValidator()

p("KAMPS9308R")