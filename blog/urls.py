from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('blogs/',views.blogs,name='blogs'),
    path('post/<id>/',views.post,name='post'),
    path('create/',views.create_post,name='create_post'),
 ]