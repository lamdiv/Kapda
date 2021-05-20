from django.urls import path,include
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
  path('',include('djoser.urls')),
  path('',include('djoser.urls.jwt')),
  path('', include(router.urls)),
]
