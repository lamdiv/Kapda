from django.urls import path,include
from rest_framework import routers
from .views import WishListViewSet

router = routers.DefaultRouter()

router.register(r'wishlist', WishListViewSet, basename="wishlist")

app_name = 'cart'

urlpatterns = [
    path('', include((router.urls, app_name))),
]
