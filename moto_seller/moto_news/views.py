from django.shortcuts import render
from rest_framework import viewsets

from moto_news.serializers import MotoNewsSerializer
from moto_news.models import MotoNewsItem


class MotoNewsViewSet(viewsets.ModelViewSet):
    queryset = MotoNewsItem.objects.all()
    serializer_class = MotoNewsSerializer
