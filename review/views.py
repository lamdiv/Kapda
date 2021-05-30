from rest_framework import viewsets,mixins,permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Question,Answer
from .serializers import QuestionSerializer,AnswerSerailzer
from shop.models import Product

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

            