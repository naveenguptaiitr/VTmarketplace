# Generated by Django 3.2.8 on 2021-11-03 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0013_alter_marketplaceitemobject_prod_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketplaceitemobject',
            name='prod_comment',
        ),
    ]
