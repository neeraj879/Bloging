from django.db import models
from Blog.models import Post
from django.contrib.auth.models import User

# Create your models here.
class Likes(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post