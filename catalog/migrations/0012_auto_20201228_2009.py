# Generated by Django 3.1.4 on 2020-12-28 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20201228_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='promo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.promo'),
        ),
    ]
