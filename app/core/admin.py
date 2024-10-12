"""
Django admin cutomization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users"""

    ordering = ['id']
    list_display = ['email', 'name']

    # fields to show for users page on django admin
    fieldsets = (
        # Give a title
        (None, {'fields': ('email', 'password')}),
        # Create a section with title permission
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                ),
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                )
            }
        ),
    )

    readonly_fields = ['last_login']

    # Creates a page for adding a user
    add_fieldsets = (
        # Create heading for a section
        (None,
         {
             # (classes) Custom css class in django to make page look prettier
             'classes': ('wide',),
             'fields': (
                 'email',
                 'password1',
                 'password2',
                 'name',
                 'is_active',
                 'is_staff',
                 'is_superuser',
             )
         }
         ),
    )


admin.site.register(models.User, UserAdmin)
