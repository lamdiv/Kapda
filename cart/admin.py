from django.contrib import admin
from .models import WishList,CartItem,Cart

admin.site.register(WishList)
admin.site.register(Cart)
admin.site.register(CartItem)

