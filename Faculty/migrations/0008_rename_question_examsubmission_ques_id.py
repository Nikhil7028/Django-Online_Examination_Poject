# Generated by Django 5.0.8 on 2024-10-02 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0007_examsubmission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examsubmission',
            old_name='question',
            new_name='ques_id',
        ),
    ]
