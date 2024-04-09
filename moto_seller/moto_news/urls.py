from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moto_news.views import MotoNewsViewSet


app_name = 'moto_news'

router = DefaultRouter()
router.register(r'moto_news', MotoNewsViewSet, basename='moto_news')

urlpatterns = [
    # path('', MotoNewsPage.as_view(), name='news_page'),
    # path('<int:pk>', MotoNewsDetailPage.as_view(), name='news_detail'),
    path('api/', include(router.urls))
]