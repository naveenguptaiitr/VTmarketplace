# Generated by Django 3.2.8 on 2021-11-19 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_details_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='profile_pic',
            field=models.TextField(blank=True),
        ),
    ]