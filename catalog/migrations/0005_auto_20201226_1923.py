# Generated by Django 3.1.4 on 2020-12-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='address',
            name='save_info',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='address',
            name='use_default',
            field=models.BooleanField(default=False),
        ),
    ]
