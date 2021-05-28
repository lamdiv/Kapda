from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import WishListSerializer,UpdateWishListSerializer,CartItemSerializer,CartCreateSerializer
from .models import WishList,CartItem,Cart
from shop.models import Product,Color,Size
from django.shortcuts import get_object_or_404

from rest_framework import mixins

class WishListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            wishlist = WishList.objects.filter(user=self.request.user)
            # print(wishlist)
        except:
            wishlist = []
        return wishlist

    def get_serializer_class(self):
        if self.action in ["post"]:
            return UpdateWishListSerializer
        else:
            return WishListSerializer
   
    def create(self,request):
        serializer = UpdateWishListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                wishlist,create = WishList.objects.get_or_create(user=self.request.user)
   
                product = Product.objects.get(id=serializer.data['product'])
               
                if serializer.data['action'] == "add":
                    wishlist.product.add(product)
                    
                if serializer.data['action'] == "remove":
                    wishlist.product.remove(product)

                serializer = WishListSerializer(wishlist)
                return Response(serializer.data)
            except:
                return Response({'status':'Some Error Occured'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def create(self,request):
        serializer = CartCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                cart,create = Cart.objects.get_or_create(user=self.request.user)
                product = Product.objects.get(id=serializer.data['product'],available=True)
                
                size = product.size.all()
                color = product.color.all()

                if size:
                    size = size.get(id=serializer.data['color'])
                else:
                    size = None


                if color:
                    color = color.get(id=serializer.data['color'])
                else:
                    color = None

                quantity = serializer.data['quantity']
                
                price = product.price

                item,created = CartItem.objects.get_or_create(cart=cart,
                                               product=product,
                                               size=size,
                                               color=color,
                                               price=price)
                if created:
                    item.quantity = quantity
                else:
                    item.quantity += quantity

                item.save()


                return Response({'status':'done'})
            except:
                return Response({'status':'error'})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk):
        serializer = CartCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = Product.objects.get(id=serializer.data['product'],available=True)
                
                size = product.size.all()
                color = product.color.all()

                if size:
                    size = size.get(id=serializer.data['color'])
                else:
                    size = None

                if color:
                    color = color.get(id=serializer.data['color'])
                else:
                    color = None

                item = get_object_or_404(CartItem,pk=pk,cart__user=self.request.user)

                quantity = serializer.data['quantity']

                item.quantity = quantity
                item.size = size
                item.color = color
                item.save()

                return Response({'status':'done'})
            except:
                return Response({'status':'error'})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        item = get_object_or_404(CartItem,pk=pk,cart__user=self.request.user)
        item.delete()
        return Response({'status':'successfully deleted'})

    def get_serializer_class(self):
        if self.action in ["post","put"]:
            return CartCreateSerializer
        else:
            return CartItemSerializer
