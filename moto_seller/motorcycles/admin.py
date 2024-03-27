from django.contrib import admin

from .models import Motorcycle


class MotorcycleAdmin(admin.ModelAdmin):
    """
    Зарегистрированная модель мотоциклов в админ панели
    """
    list_display = ['id', "model_name", "moto_type", "date_of_issue", "status", 'creator']
    list_filter = ["moto_type", "date_of_issue", "status", 'creator']
    search_fields = ['creator__login']


admin.site.register(Motorcycle, MotorcycleAdmin)
