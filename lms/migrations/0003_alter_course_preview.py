# Generated by Django 4.2.2 on 2024-07-07 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_lesson_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='previews/courses/', verbose_name='превью'),
        ),
    ]
