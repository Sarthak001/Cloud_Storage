# Generated by Django 3.0.2 on 2020-01-21 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloudx', '0003_filedetails_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedetails',
            name='email',
        ),
    ]
