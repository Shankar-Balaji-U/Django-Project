from django.contrib import admin
from . models import Payment, Notification
from django.utils.translation import gettext, gettext_lazy as _



# Register your models here.
admin.site.register(Payment)

@admin.register(Notification)
class NotifyAdmin(admin.ModelAdmin):
	fieldsets = (
			(None, {'fields': ('title', 'message', 'status')}),
			(_('Important date & time'), {'fields': ('created_on', 'duration')}),
		)

	search_fields = ('title', 'created_on')
	ordering = ('-created_on',)
	readonly_fields = ['created_on', 'duration',]
	list_display = ('__str__', 'status', 'duration')