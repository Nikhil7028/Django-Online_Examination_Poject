# Generated by Django 5.0.8 on 2024-09-19 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacultyLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ZPRN', models.CharField(max_length=10, unique=True)),
                ('Name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=7)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobNo', models.CharField(max_length=14)),
            ],
        ),
    ]
