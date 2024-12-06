from django.contrib.auth.views import LogoutView
from django.urls import path
from users import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('update/',views.update,name='update'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]
