from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.
from mptt.models import MPTTModel,TreeForeignKey

from django.core.exceptions import ValidationError


class Image(models.Model):
    posts=models.ForeignKey('Post',on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField()

class Category(models.Model):
    name=models.CharField(max_length=10,default='Cat')

    def __str__(self):
        return self.name

    def get_absolute_cat_url(self):
        return reverse('cat-detail',kwargs={'id':self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=10, default='Tag')

    def __str__(self):
        return self.name

    def get_absolute_tag_url(self):
        return reverse('tag-detail',kwargs={'id':self.pk})


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=100,default='Title')
    content=models.TextField(default="The Content")
    date_posted = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,blank=True)
    cat=models.ManyToManyField(Category,blank=True)
    thumbnail = models.ImageField(upload_to='blog_images',blank=True,null=True)
    images=models.ManyToManyField(Image,blank=True)
    is_save=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_post_url(self):
        return reverse('post',kwargs={'id':self.id})

    def get_absolute_save_post_url(self):
        return reverse('save-post',kwargs={'id':self.id})


def validate_geeks_mail(value):
    if "@gmail.com" in value:
        return value
    else:
        raise ValidationError("This field accepts mail id of google only")

class Comment(MPTTModel):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    parent=TreeForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50, default='Samir Patil')
    email = models.EmailField(default="email@gmail.com",validators=[validate_geeks_mail])
    content = models.TextField(default="This is the comment")
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)



    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'comment on {self.post.title}'


class LikePost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title } like by {self.user}'


class DislikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.title} dislike by {self.user}'

