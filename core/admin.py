from django.contrib import admin
from django.contrib.auth.models import Group

from core.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {'fields': ('email', 'first_name', 'last_name')}),
        ('Допуски', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


# class PersonAdmin(CustomUserAdmin):
#     readonly_fields = ('last_login', 'data_joined')


admin.site.unregister(Group)