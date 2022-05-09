from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import (WishListSerializer,UpdateWishListSerializer,CartItemSerializer,CartCreateSerializer,
                        CouponSerializer,CouponApplySerializer)
from .models import WishList,OrderItem,Order,Coupon
from shop.models import Product,Color,Size
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
        return OrderItem.objects.filter(order__user=self.request.user,order__is_complete=False)

    def create(self,request):
        serializer = CartCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order,create = Order.objects.get_or_create(user=self.request.user,is_complete=False)
                product = Product.objects.get(id=serializer.data['product'],available=True)
                
                size = product.size.all()
                color = product.color.all()

                if size:
                    size = size.get(id=serializer.data['size'])
                else:
                    size = None


                if color:
                    color = color.get(id=serializer.data['color'])
                else:
                    color = None

                quantity = serializer.data['quantity']
                
                item,created = OrderItem.objects.get_or_create(order=order,
                                               product=product,
                                               size=size,
                                               color=color,
                                               price = product.price                                            
                                               )
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
                    size = size.get(id=serializer.data['size'])
                else:
                    size = None

                if color:
                    color = color.get(id=serializer.data['color'])
                else:
                    color = None

                item = get_object_or_404(OrderItem,pk=pk,order__user=self.request.user,order__is_complete=False)
                quantity = serializer.data['quantity']
                print(quantity)
                item.quantity = quantity
                item.color = color
                item.save()

                return Response({'status':'done'})
            except:
                return Response({'status':'error'})

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk):
        item = get_object_or_404(OrderItem,pk=pk,order__user=self.request.user,order__is_complete=False)
        item.delete()
        return Response({'status':'successfully deleted'})

    def get_serializer_class(self):
        if self.action in ["post","put"]:
            return CartCreateSerializer
        else:
            return CartItemSerializer


class CouponViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CouponApplySerializer

    def create(self,request):
        serializer = CouponApplySerializer(data=request.data)
        if serializer.is_valid():
            try:    
                code = serializer.data['code']
                now = timezone.now()
                coupon = Coupon.objects.get(code__iexact=code,
                                            valid_from__lte=now,
                                            valid_to__gte=now,
                                            active=True)
                serializer = CouponSerializer(coupon)
                return Response(serializer.data)
            except Coupon.DoesNotExist:
                return Response({'status':'coupon isn\'t valid'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  