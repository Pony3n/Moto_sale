from django.contrib import admin

from .models import Motorcycle


class MotorcycleAdmin(admin.ModelAdmin):
    """
    Зарегистрированная модель мотоциклов в админ панели
    """
    list_display = ["model_name", "moto_type", "date_of_issue", "status"]
    list_filter = ["moto_type", "date_of_issue", "status"]


admin.site.register(Motorcycle, MotorcycleAdmin)
