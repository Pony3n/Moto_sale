from django.contrib import admin

from moto_news.models import MotoNewsItem


class MotoNewsItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_of_creation', 'date_of_publish', 'is_published']
    list_filter = ['date_of_creation', 'date_of_publish', 'is_published']
    search_fields = ['title']


admin.site.register(MotoNewsItem, MotoNewsItemAdmin)
