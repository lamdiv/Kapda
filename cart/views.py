from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import WishListSerializer,UpdateWishListSerializer
from .models import WishList
from shop.models import Product

from rest_framework import mixins

class WishListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishListSerializer

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

    