# Generated by Django 3.1 on 2020-12-25 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_profileimg'),
        ('classroom', '0010_auto_20201225_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]