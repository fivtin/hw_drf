# Generated by Django 4.2.2 on 2024-07-06 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='previews/lessons/', verbose_name='превью'),
        ),
    ]
