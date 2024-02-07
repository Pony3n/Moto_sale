from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import show_main, show_about, show_contact, MotorcycleDetailView

urlpatterns = [
    path('', show_main, name="show_main"),
    path('about/', show_about, name="show_about"),
    path('contact/', show_contact, name="show_contact"),
    path('<int:pk>/', MotorcycleDetailView.as_view(), name="motorcycle_detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)