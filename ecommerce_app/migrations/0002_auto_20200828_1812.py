# Generated by Django 2.2.4 on 2020-08-28 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='store_count',
            field=models.IntegerField(default=0),
        ),
    ]