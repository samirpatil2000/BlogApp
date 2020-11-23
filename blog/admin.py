from django.contrib import admin
from .models import Post,Author,Tag,Category,Comment,LikePost,DislikePost,Image

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(DislikePost)

admin.site.register(Image)