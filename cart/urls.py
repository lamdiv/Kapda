from django.urls import path,include
from rest_framework import routers
from .views import WishListViewSet,CartViewSet,CouponViewSet

router = routers.DefaultRouter()

router.register(r'wishlist', WishListViewSet, basename="wishlist")
router.register(r'order', CartViewSet, basename="order")
router.register(r'coupon', CouponViewSet, basename="coupon")

app_name = 'cart'

urlpatterns = [
    path('', include((router.urls, app_name))),
]
