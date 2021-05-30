from rest_framework import serializers
from .models import Category,Type,Color,Material,Brand,Product,Size
from review.models import Question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class TypeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Type
        fields = ['id','name','category']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','name']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id','name']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id','name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','name']


class ProductSerializer(serializers.ModelSerializer):
    _type = TypeSerializer(read_only=True)
    color = ColorSerializer(many=True,read_only=True)
    material = MaterialSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    size = SizeSerializer(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['id','name','slug','category','_type','color',
                  'material','size','brand','image','description','price']

class FilterSerializer(serializers.Serializer):
    category = CategorySerializer(read_only=True,many=True)
    _type = TypeSerializer(read_only=True,many=True)
    color = ColorSerializer(read_only=True,many=True)
    size = SizeSerializer(read_only=True,many=True)
    material = MaterialSerializer(read_only=True,many=True)
    brand = BrandSerializer(read_only=True,many=True)
