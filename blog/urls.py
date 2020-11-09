from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('blogs/',views.blogs,name='blogs'),
    path('post/',views.post,name='post'),
 ]