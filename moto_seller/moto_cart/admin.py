from django.contrib import admin

from .models import Cart, CartItem


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["cart"]


class CartAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemsAdmin)
