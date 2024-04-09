from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from rest_framework import viewsets
from django.views import View
from django.utils import timezone

from moto_news.serializers import MotoNewsSerializer
from moto_news.models import MotoNewsItem


class MotoNewsViewSet(viewsets.ModelViewSet):
    queryset = MotoNewsItem.objects.all()
    serializer_class = MotoNewsSerializer


class MotoNewsPage(View):
    items_per_page = 6
    template_name = 'moto_news/news_page.html'

    def get(self, request, *args, **kwargs):
        news = MotoNewsItem.objects.filter(
            date_of_publish__lte=timezone.now(),
            is_published=True).order_by('-date_of_publish')
        page = request.GET.get('page', 1)

        paginator = Paginator(news, self.items_per_page)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'news': news})


class MotoNewsDetailPage(View):
    template_name = 'moto_news/news_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            news = MotoNewsItem.objects.get(pk=self.kwargs['pk'])
        except MotoNewsItem.DoesNotExist:
            return HttpResponseRedirect(reverse('moto_news:news_page'))

        return render(request, self.template_name, {'news': news})