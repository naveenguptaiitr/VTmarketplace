from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField


# Model class for storing data.
class MarketPlaceItemObject(models.Model):

    PROD_TYPE = [
        ('electronics', 'Electronics'),
        ('furnitures', 'Furnitures'),
        ('collectible_arts', 'Collectible Arts'),
        ('home_and_kitchen', 'Home & Kitchen'),
        ('miscellaneous', 'Miscellaneous')
    ]

    prod_name = models.CharField(max_length=200)
    prod_price = models.CharField(max_length=5, default='$0')
    prod_description = models.TextField(blank=True)
    prod_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_seller = models.CharField(max_length=200, default='admin')
    prod_type = models.CharField(max_length=50, choices=PROD_TYPE, default='electronics')
    date_posted = models.DateTimeField(auto_now_add=True)
    img_path_1 = models.TextField(blank=True)
    img_path_2 = models.TextField(blank=True)
    img_path_3 = models.TextField(blank=True)
    img_path_4 = models.TextField(blank=True)

    def __str__(self):
        return self.prod_name

    def get_absolute_url(self):
        return reverse("marketplace:marketplace_detail_item", args=[self.id])


# Model class for storing data.
class CreateComment(models.Model):
    item = models.ForeignKey(MarketPlaceItemObject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=800)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if(self.comment):
            return self.comment[:20]
        else:
            self.user

    def get_absolute_url(self):

        if(self.id):
            return reverse("marketplace:marketplace_detail_item", args=[self.item_id])
        else:
            return reverse("users:profile", args=[self.user.username])



# credentials for regular and admin user
regular_user = {"username": "john", "password": "regular"}
admin_user = {"username": "admin", "password": "admin"}



