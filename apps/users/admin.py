from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CustomUser

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'name', 'username', 'email', 'city', 'role')
    list_display_links = ('id', 'name', 'username')
    ordering = ('id',)
    search_fields = ('name', 'username', 'email')
    filter_horizontal = ()
    fieldsets = None
    fields = ('name',
              'username',
              'email',
              'city',
              'role',
              'date_joined',
              'last_login')
    readonly_fields = ('date_joined',
                       'last_login')


admin.site.register(CustomUser, CustomUserAdmin)
