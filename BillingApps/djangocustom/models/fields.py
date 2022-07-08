# Django imports
from django.db.models import Field
from django.utils.translation import ugettext_lazy as _

# Project imports
from djangocustom.forms import fields
from djangocustom.models.validators import isGSTIN, isPAN




GSTIN_MAX_LENGTH = 15
PAN_MAX_LENGTH = 10


class GSTField(Field):
    default_validators = [isGSTIN]
    description = _("Goods and Services Tax")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = GSTIN_MAX_LENGTH
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.GSTField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class PANField(Field):
    default_validators = [isPAN]
    description = _("Permanent account number")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = PAN_MAX_LENGTH
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.PANField}
        defaults.update(kwargs)
        return super().formfield(**defaults)