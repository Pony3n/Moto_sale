from django.contrib import admin

from .models import Cart, CartItem


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["cart", 'get_model_name']

    def get_model_name(self, obj):
        return obj.get_model_name()

    get_model_name.short_description = 'Model Name'

class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__login']
    list_filter = ['user']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemsAdmin)
