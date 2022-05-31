from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Follow(models.Model):
    #the follower
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="isFollowing")
    #the user followed
    userFollowed= models.ForeignKey(User, on_delete=models.CASCADE, related_name="isFollowed")
class Post(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='author')
    date = models.DateTimeField(default=datetime.now())
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    @property
    def likes_count(self):
        return self.liked.all().count()


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)