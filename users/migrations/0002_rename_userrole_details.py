# Generated by Django 3.2.8 on 2021-11-14 15:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserRole',
            new_name='Details',
        ),
    ]
