# Generated by Django 3.2.8 on 2021-11-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0018_alter_marketplaceitemobject_prod_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaceitemobject',
            name='prod_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
