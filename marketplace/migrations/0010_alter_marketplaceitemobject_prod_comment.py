# Generated by Django 3.2.8 on 2021-11-01 20:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0009_marketplaceitemobject_prod_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaceitemobject',
            name='prod_comment',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None),
        ),
    ]