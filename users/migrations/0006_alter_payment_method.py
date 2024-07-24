# Generated by Django 4.2.2 on 2024-07-24 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_payment_link_payment_session_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.PositiveSmallIntegerField(choices=[(2, 'account'), (1, 'cash')], default=1, verbose_name='способ оплаты'),
        ),
    ]
