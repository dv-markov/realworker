from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Role, CustomUser, UserProfile, Country, City, Category, Specialization, Qualification, GeoData


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
admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(Specialization)
admin.site.register(Qualification)
admin.site.register(GeoData)
