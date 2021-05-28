from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status

from .models import Category,Type,Color,Material,Brand,Product,Size
from .serializers import (CategorySerializer,ProductSerializer,FilterSerializer)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]



class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name")
    _type = filters.CharFilter(field_name="_type__name")
    color = filters.CharFilter(field_name="color__name")
    material = filters.CharFilter(field_name="material__name")
    brand = filters.CharFilter(field_name="brand__name")
    size = filters.CharFilter(field_name="size__name")
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category','_type','min_price','max_price','size','color','material','brand']


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(available=True)
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]



class FilterViewset(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        filters = {}

        cat = Category.objects.all()
        typ = Type.objects.all()
        col = Color.objects.all()
        mat = Material.objects.all()
        brnd = Brand.objects.all()
        size = Size.objects.all()

        category_params = self.request.query_params.get('category')
        _type = self.request.query_params.get('type')
        
        if category_params is not None:   
            category = get_object_or_404(Category,name=category_params)
            typ = category.types.all()

            products = category.products.filter(available=True).values_list('id',flat=True)

            col = col.filter(id__in=products)
            mat = mat.filter(id__in=products)
            size = size.filter(id__in=products)
            brnd = brnd.filter(id__in=products)
            
        filters['category'] = cat
        filters['_type'] = typ
        filters['color']= col
        filters['size'] = size
        filters['material'] = mat
        filters['brand'] = brnd
        
        serializer = FilterSerializer(filters)
        return Response (serializer.data, status=status.HTTP_200_OK)


