from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Project(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #customer = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    search_term = models.CharField(max_length=30,default="")
    total_views = models.IntegerField(default=0)
    fav_titles = models.IntegerField(default=0)
    unfav_titles = models.IntegerField(default=0)
    likes_fav = models.IntegerField(default=0)
    dislikes_fav = models.IntegerField(default=0)
    likes_unfav = models.IntegerField(default=0)
    dislikes_unfav = models.IntegerField(default=0)
    total_favourability = models.IntegerField(default=0)
    months = ArrayField(models.CharField(max_length=10,default=""), null=True, blank=True)
    y1 = ArrayField(models.IntegerField(default=0), null=True, blank=True)
    y2 = ArrayField(models.IntegerField(default=0), null=True, blank=True)

    def __str__(self):
        return self.project_name


