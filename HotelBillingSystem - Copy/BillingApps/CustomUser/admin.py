from django.contrib import admin
from CustomUser.models import CustomUser, ClientSettings
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from CustomUser.forms import CustomUserAdminForm




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	"""Define admin model for custom CustomUser model with no email field."""
	# form = CustomUserAdminForm
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_image', 'thumbnail_tag')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2'),
			}),
		)
	list_display = ('email', 'full_name', 'is_active', 'is_staff', 'is_superuser')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)
	readonly_fields = ['thumbnail_tag', 'date_joined']
	
	filter_horizontal = ()
	list_filter = ()

	class Media:
		css = {'all': ('css/admin/user.css',)}
		js = ('javascript/admin/dynamic-src.js',)




admin.site.register(ClientSettings)
