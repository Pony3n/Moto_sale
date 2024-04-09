from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from moto_news.models import MotoNewsItem


class MotoNewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return MotoNewsItem.objects.filter(
            date_of_publish__lte=timezone.now(),
            is_published=True).order_by('-date_of_publish')

    def lastmod(self, obj: MotoNewsItem):
        return obj.date_of_publish