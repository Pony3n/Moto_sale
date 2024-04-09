from django.db import models
from django.urls import reverse


class MotoNewsItem(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст новости')
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания новости')
    date_of_publish = models.DateField(null=True, blank=True, verbose_name='Дата публикации новости')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='moto_news/', null=True, blank=True, verbose_name='Картинка новости')

    def get_absolute_url(self):
        return reverse('moto_news:news_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
