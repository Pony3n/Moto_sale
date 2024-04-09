from django.db import models


class MotoNewsItem(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = models.TextField()
    date_of_creation = models.DateField(auto_now_add=True)
    date_of_publish = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='moto_news/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
