from .models import Question,Answer,Rating
from rest_framework import serializers
from users.serializers import UserNameSerializer

class AnswerSerailzer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)
    class Meta:
        model = Answer
        fields = ['id','user','question','answer']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','product','question']

class QuestionReSerializer(serializers.ModelSerializer):
    reply = AnswerSerailzer(read_only=True)
    user = UserNameSerializer(read_only=True)
    class Meta:
        model = Question
        fields = ['id','user','product','created','question','reply']


class RatingSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ['id','user','product','created','stars','review']

