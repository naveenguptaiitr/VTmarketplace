# Generated by Django 3.2.8 on 2021-11-14 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0022_rename_prod_seller_marketplaceitemobject_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplaceitemobject',
            name='prod_seller',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]