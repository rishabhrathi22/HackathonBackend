# Generated by Django 3.1 on 2020-12-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_auto_20201121_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.CharField(default='16-12-2020', max_length=10),
        ),
    ]
