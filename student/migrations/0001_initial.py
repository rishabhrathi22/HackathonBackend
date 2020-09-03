# Generated by Django 3.1 on 2020-09-03 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institution.institute')),
            ],
        ),
    ]