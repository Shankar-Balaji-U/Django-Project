# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.forms.fields import Field
from django.utils.translation import ugettext_lazy as _

# Project imports
from djangocustom.models.validators import isGSTIN, isPAN


class GSTField(Field):
    default_error_messages = {"invalid": _("Enter a valid GST number.")}
    default_validators = [isGSTIN]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)


class PANField(Field):
    default_error_messages = {"invalid": _("Enter a valid PAN number.")}
    default_validators = [isPAN]

    def __init__(self, **kwargs):
        super().__init__(strip=True, **kwargs)