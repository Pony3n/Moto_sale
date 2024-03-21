from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CartViewSet, CartItemViewSet, MotoUserCartView

app_name = 'moto_cart'

router = DefaultRouter()
router.register(r'moto_carts', CartViewSet, basename='moto_carts')
router.register(r'moto_cart_items', CartItemViewSet, basename='moto_cart_items')

urlpatterns = [
    path('', MotoUserCartView.as_view(), name='moto_user_cart'),
    path('api/', include(router.urls)),
]
