# Generated by Django 3.1.4 on 2020-12-28 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20201228_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(default='1'),
            preserve_default=False,
        ),
    ]