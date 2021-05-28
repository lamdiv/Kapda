from rest_framework import serializers
from .models import WishList,Cart,CartItem
from shop.models import Product,Size,Color
from shop.serializers import ProductSerializer,ColorSerializer,SizeSerializer


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


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id','product','color','size','price','quantity']
        read_only_fields = ['id','price','quantity']

class CartCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=Color.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all(),required=False)

    class Meta:
        model = CartItem
        fields = ['id','product','color','size','quantity']

