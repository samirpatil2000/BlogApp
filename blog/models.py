from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.


class Author(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100,default='Title')
    content=models.TextField(default="The Content")
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(Author, on_delete=models.CASCADE,blank=True,null=True)
    thumbnail = models.ImageField(upload_to='blog_images',blank=True,null=True)

    def __str__(self):
        return self.title


