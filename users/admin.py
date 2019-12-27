from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import CustomUser

# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username','email','is_admin', 'is_staff', 'is_active')
	list_filter = ('is_admin', 'is_staff', 'is_active')

	fieldsets = (
			(None, {'fields': ('username','email','password')}),
			('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')})
		)
	search_fields = ('username','email')
	ordering = ('username','email')

	filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)


admin.site.unregister(Group)