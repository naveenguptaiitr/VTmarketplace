# Generated by Django 3.2.8 on 2021-11-18 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0026_createcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='createcomment',
            name='role',
            field=models.TextField(default='regular', max_length=50),
            preserve_default=False,
        ),
    ]
