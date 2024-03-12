from rest_framework.routers import DefaultRouter

from .views import CartViewSet, CartItemViewSet

app_name = 'moto_cart'

router = DefaultRouter()
router.register(r'moto_carts', CartViewSet, basename='moto_cart')
router.register(r'moto_cart-items', CartItemViewSet, basename='moto_cart-items')

urlpatterns = router.urls
