from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MotoUser


class MotoUserAdmin(UserAdmin):
    """
    Кастомное отображение пользователей в админ панели, для более удобного чтения информации.
    """
    model = MotoUser
    list_display = ['id', 'login', 'get_full_name', 'date_of_birth', 'preferences', 'is_active']
    list_filter = ['date_of_birth', 'preferences', 'is_active']
    search_fields = ['login', 'email']
    ordering = ['login']

    fieldsets = (
        ('Базовая информация', {'fields': ('email', 'login', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name',
                                                'date_of_birth', 'preferences', 'phone_number')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        ('Информация пользователя', {
            'classes': ('wide',),
            'fields': ('login', 'email', 'avatar'),
        }),
        ('Персональная информация', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'preferences', 'phone_number'),
        }),
        ('Пароль', {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = 'Full Name'


admin.site.register(MotoUser, MotoUserAdmin)

