from django.contrib import admin
from .models import WishList,OrderItem,Order

admin.site.register(WishList)
admin.site.register(Order)
admin.site.register(OrderItem)

