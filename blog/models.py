from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=10,default='Cat')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10, default='Tag')

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100,default='Title')
    content=models.TextField(default="The Content")
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,blank=True,null=True)
    cat=models.ManyToManyField(Category,blank=True,null=True)
    thumbnail = models.ImageField(upload_to='blog_images',blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_post_url(self):
        return reverse('post',kwargs={'id':self.id})


