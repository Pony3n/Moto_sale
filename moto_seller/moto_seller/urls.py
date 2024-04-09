from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from moto_cart.urls import urlpatterns as moto_cart_urlpatterns
from moto_news.sitemap import MotoNewsSitemap

sitemaps = {
    'news': MotoNewsSitemap
}

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include("motorcycles.urls")),
    path('user/', include('moto_user.urls')),
    path('news/', include('moto_news.urls')),
    path('cart/', include(moto_cart_urlpatterns)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
