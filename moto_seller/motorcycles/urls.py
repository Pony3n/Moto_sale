from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import moto_show_about, moto_show_contact, MotoDetailView, MotoSearch, MotoMainView

app_name = 'motorcycles'

urlpatterns = [
    path('', MotoMainView.as_view(), name="show_main"),
    path('about/', moto_show_about, name="show_about"),
    path('contact/', moto_show_contact, name="show_contact"),
    path('<int:pk>/', MotoDetailView.as_view(), name="motorcycle_detail"),
    path('search/', MotoSearch.as_view(), name="motorcycle_search"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
