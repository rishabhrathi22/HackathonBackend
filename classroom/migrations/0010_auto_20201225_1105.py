# Generated by Django 3.1 on 2020-12-25 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_auto_20201225_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='messages',
            field=models.JSONField(),
        ),
    ]