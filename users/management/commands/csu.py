import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(email=os.getenv('SUPERUSER_LOGIN'), first_name='admin')
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()

        user = User.objects.create(email='user@example.com', first_name='user')
        user.set_password('user1user')
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()

        user = User.objects.create(email='guest@example.com', first_name='guest')
        user.set_password('guest1guest')
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()

        user = User.objects.create(email='moderator@example.com', first_name='moderator')
        user.set_password('moder1moder')
        user.is_staff = True
        user.is_active = True
        user.is_superuser = False
        user.save()
