from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Команда для создания супе-пользователя"""
    help = 'Create a superuser with required fields filled'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email='admin@example.com',
                login='admin',
                password='admin2362',
                first_name='Admin',
                last_name='User',
                date_of_birth='2000-01-01',
                preferences='КЛАС',
                phone_number='+71234567890',
            )

        self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
