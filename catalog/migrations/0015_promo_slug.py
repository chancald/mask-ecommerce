# Generated by Django 3.1.4 on 2020-12-28 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20201228_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='slug',
            field=models.SlugField(default='test'),
            preserve_default=False,
        ),
    ]
