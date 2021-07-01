from rest_framework import viewsets,mixins,permissions,status
from rest_framework.response import Response
from .models import Question,Answer,Rating
from .serializers import QuestionSerializer,AnswerSerailzer,RatingSerializer
from shop.models import Product
from django.shortcuts import get_object_or_404

class QuestionViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuestionSerializer
    
    def create(self,request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(id=serializer.data['product'])
            Question.objects.create(user=self.request.user,
                                    question=serializer.data['question'],
                                    product=product)
            return Response({'status':'added question'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
           
class AnswerViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AnswerSerailzer
    
    def create(self,request):
        serializer = AnswerSerailzer(data=request.data)
        if serializer.is_valid():
            question = Question.objects.get(id=serializer.data['question'])
            Answer.objects.create(user=self.request.user,
                                      answer=serializer.data['answer'],
                                        question=question)
            return Response({'status':'added answer'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class RatingViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RatingSerializer
    
    def create(self,request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.get(id=serializer.data['product'])
            rating = get_object_or_404(Rating,product=product,user=self.request.user)
            
            if rating:
                rating.stars = serializer.data['stars']
                rating.review = serializer.data['review']
                
                rating.save()
            
                return Response({'status':'Rating done'})
            return Response({'status':'You haven\'t bought this product yet'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            Product.objects.get(id=serializer.data['product'])