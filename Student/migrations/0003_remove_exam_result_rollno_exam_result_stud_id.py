# Generated by Django 5.0.8 on 2024-10-08 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_exam_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam_result',
            name='rollno',
        ),
        migrations.AddField(
            model_name='exam_result',
            name='stud_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='Student.studinfo'),
            preserve_default=False,
        ),
    ]
