from django.db import models
from django.conf import settings
from shop.models import Product,Size,Color

class WishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='wishlist')

    def __str__(self):
        return self.user.email + ' wishlist'

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email + ' cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.quantity*self.product.price
