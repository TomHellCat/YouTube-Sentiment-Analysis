from django.db import models
from django.contrib.auth.models import User

class Project2(models.Model): 
    title = models.CharField(max_length=200)
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=30,default="")
    not_objects = models.BooleanField(default=False)

class VideoInfo2(models.Model):
    project = models.ForeignKey(Project2, null=True, blank=True, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    sentiment = models.BooleanField(default=True)
    date = models.CharField(max_length=10,null=True)
    tag = models.CharField(max_length=10,null=True)
    


    


