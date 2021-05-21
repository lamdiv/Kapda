from django.urls import path,include
from rest_framework import routers
from .views import CategoryViewset,ProductViewset,FilterViewset

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewset, basename="categories")
router.register(r'products', ProductViewset, basename="products")
router.register(r'filters', FilterViewset, basename="filters")

app_name = 'shop'

urlpatterns = [
    path('', include((router.urls, app_name))),
]
