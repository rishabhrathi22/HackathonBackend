# Generated by Django 3.1 on 2020-12-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profileimg',
            field=models.ImageField(default='none', upload_to='student-images/'),
            preserve_default=False,
        ),
    ]