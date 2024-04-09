from rest_framework import serializers

from moto_news.models import MotoNewsItem


class MotoNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotoNewsItem
        fields = [
            'id',
            'title',
            'content',
            'date_of_creation',
            'date_of_publish',
            'is_published'
        ]
