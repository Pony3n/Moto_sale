from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from moto_cart.urls import urlpatterns as moto_cart_urlpatterns
from moto_news.sitemap import MotoNewsSitemap

sitemaps = {
    'news': MotoNewsSitemap
}

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include("motorcycles.urls")),
    path('users/', include('moto_user.urls')),
    path('news/', include('moto_news.urls')),
    path('carts/', include(moto_cart_urlpatterns)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
