# Generated by Django 5.0.8 on 2024-10-02 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0010_examsubmission_exam_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examsubmission',
            name='exam_sub',
        ),
    ]
