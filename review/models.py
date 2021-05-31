from django.db import models
from django.conf import settings
from shop.models import Product
from django.core.validators import MaxValueValidator,MinValueValidator

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name="question",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    question = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
    question = models.OneToOneField(Question,related_name='reply',on_delete=models.CASCADE)
    answer = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer

class Rating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    review = models.TextField(null=True)

    class Meta:
        unique_together = (('user','product'),)
        index_together = (('user','product'),)

    def __str__(self):
        return str(self.stars)
