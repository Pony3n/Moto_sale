from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        call_command('loaddata', 'moto_user/fixtures/moto_user.json')
        call_command('loaddata', 'motorcycles/fixtures/motorcycles.json')
        call_command('loaddata', 'moto_news/fixtures/moto_news.json')

        self.stdout.write(self.style.SUCCESS('Successfully loaded fixtures'))
