# Generated by Django 3.2.8 on 2021-10-28 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketPlaceItemObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=200)),
                ('prod_price', models.PositiveIntegerField(default=0)),
                ('prod_description', models.TextField(blank=True)),
                ('prod_type', models.CharField(choices=[('electronics', 'Electronics'), ('furnitures', 'Furnitures'), ('collectible_arts', 'Collectible Arts'), ('home_and_kitchen', 'Home & Kitchen'), ('miscellaneous', 'Miscellaneous')], default='electronics', max_length=50)),
                ('prod_seller', models.CharField(max_length=200)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('img_path_1', models.TextField(blank=True)),
                ('img_path_2', models.TextField(blank=True)),
                ('img_path_3', models.TextField(blank=True)),
                ('img_path_4', models.TextField(blank=True)),
            ],
        ),
    ]
