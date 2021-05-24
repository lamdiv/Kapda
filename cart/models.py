from django.db import models
from django.conf import settings
from shop.models import Product

class WishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='wishlist')

    def __str__(self):
        return self.user.email + ' wishlist'