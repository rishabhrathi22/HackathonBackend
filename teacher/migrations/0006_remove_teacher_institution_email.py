# Generated by Django 3.1 on 2020-09-03 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_delete_studentteacherclassmapping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='institution_email',
        ),
    ]
