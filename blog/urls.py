from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('create/', views.create_post, name='create_post'),
    path('blogs/',views.blogs,name='blogs'),
    path('post/<id>/', views.post_detail, name='post'),
    path('update/<id>',views.update_post,name='update_post'),
    path('delete/<id>',views.delete_post,name='delete_post'),

    path('cat/<id>/',views.cat_detail,name='cat-detail'),
    path('tag/<id>/',views.tag_detail,name='tag-detail'),

    #search
    path('search/',views.search_function,name='search'),
 ]