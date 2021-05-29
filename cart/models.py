from django.db import models
from django.conf import settings
from shop.models import Product,Size,Color
from django.core.validators import MinValueValidator,MaxValueValidator

class WishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='wishlist')

    def __str__(self):
        return self.user.email + ' wishlist'

class Coupon(models.Model):
    code = models.CharField(max_length=54,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Order(models.Model):

    Choices = (
            ('Cash On Delivery','COD'),
            ('Esewa','esewa'),
            ('Khalti','khalti'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=54,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    paymentMethod = models.CharField(choices=Choices,default='COD',max_length=54)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)

    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0),
                               MaxValueValidator(100)])

    def __str__(self):
        return self.user.email + ' order'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))



class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.quantity*self.product.price
