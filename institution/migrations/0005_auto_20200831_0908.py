# Generated by Django 3.1 on 2020-08-31 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_auto_20200828_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]
