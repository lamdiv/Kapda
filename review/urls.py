from django.urls import path,include
from rest_framework import routers
from .views import QuestionViewset,AnswerViewset

router = routers.DefaultRouter()

router.register(r'question',QuestionViewset,basename='question')
router.register(r'answer',AnswerViewset,basename='answer')

app_name = 'review'

urlpatterns = [
    path('', include((router.urls, app_name))),
]