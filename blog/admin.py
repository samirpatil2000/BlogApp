from django.contrib import admin
from .models import Post,Author,Tag,Category,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)