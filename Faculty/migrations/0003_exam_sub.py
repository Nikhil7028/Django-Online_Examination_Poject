# Generated by Django 5.0.8 on 2024-09-21 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0002_rename_name_facultylogin_fullname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam_sub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subject', models.CharField(max_length=10, unique=True)),
                ('exam_time_min', models.IntegerField()),
            ],
        ),
    ]
