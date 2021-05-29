from django.contrib import admin
from .models import WishList,OrderItem,Order,Coupon

admin.site.register(WishList)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)

