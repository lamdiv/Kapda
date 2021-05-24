from rest_framework import serializers
from .models import WishList
from shop.models import Product
from shop.serializers import ProductSerializer


class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = WishList
        fields = ['id','product']  
        depth = 1


class UpdateWishListSerializer(serializers.Serializer):
    Choices = (
        ('add','add'),
        ('remove','remove')
    )
    action = serializers.ChoiceField(choices=Choices)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())