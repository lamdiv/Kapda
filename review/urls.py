from django.urls import path,include
from rest_framework import routers
from .views import QuestionViewset,AnswerViewset,RatingViewset

router = routers.DefaultRouter()

router.register(r'question',QuestionViewset,basename='question')
router.register(r'answer',AnswerViewset,basename='answer')
router.register(r'rating',RatingViewset,basename='rating')

app_name = 'review'

urlpatterns = [
    path('', include((router.urls, app_name))),
]