from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'username',
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )}),
        ('Личная информация', {
            'fields': (
                'first_name',
                'last_name',
                'email',
            )}),
        ('Разрешения', {
            'fields': (
                'is_staff',
                'is_active',
            )}),
        ('Другое', {
            'classes': (
                'collapse',
            ),
            'fields': (
                'last_login',
                'date_joined',
            )}),
    )
    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
    )
    ordering = ('email',)
    exclude = ('password',)


admin.site.unregister(Group)
