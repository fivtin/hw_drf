# Generated by Django 4.2.2 on 2024-07-21 00:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms', '0005_courssubscriber'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoursSubscriber',
            new_name='CourseSubscriber',
        ),
    ]
