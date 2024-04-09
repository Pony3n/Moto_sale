from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from moto_cart.urls import urlpatterns as moto_cart_urlpatterns

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include("motorcycles.urls")),
    path('user/', include('moto_user.urls')),
    path('news/', include('moto_news.urls')),
    path('cart/', include(moto_cart_urlpatterns))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
