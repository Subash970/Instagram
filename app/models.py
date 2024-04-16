from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class UserBio(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=False)
    username = models.CharField(max_length=15 , blank=True)
    bio = models.TextField(max_length=50 , blank=True)
    img = models.ImageField(upload_to='picture' , blank=True)

class UserFriends(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=False)
    followers = models.ManyToManyField(User, blank=True , related_name='followers')
    following = models.ManyToManyField(User , blank=True , related_name='following')
    

class Post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank=False)
    img = models.ImageField(upload_to='picture' , blank=False)
    likes = models.ManyToManyField(User , blank=True , related_name='likes')
    caption = models.TextField(max_length=200 , blank=True)
    upload_at = models.DateTimeField(default=datetime.now, blank=False)

class UserTable(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=False)
    liked = models.ManyToManyField(Post , related_name='liked' , blank=True)
    saved = models.ManyToManyField(Post , related_name='saved' , blank=True)

class Comments(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , blank=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank=False)
    comment = models.CharField(max_length=100 , blank=False)
    commented_on = models.DateTimeField(default=datetime.now , blank=False)