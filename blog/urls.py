from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('create/', views.create_post, name='create_post'),
    path('blogs/',views.blogs,name='blogs'),
    path('post/<id>/', views.post_detail, name='post'),
    path('update/<id>',views.update_post,name='update_post'),
 ]