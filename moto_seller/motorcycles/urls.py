from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import show_main

urlpatterns = [
    path('', show_main, name="show_main"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)