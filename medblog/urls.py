from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('posts/', views.posts, name='posts'),
    path('search/', views.search_blogs, name='search_blogs'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]

