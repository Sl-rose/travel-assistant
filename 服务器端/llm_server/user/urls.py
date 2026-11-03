from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('update_profile/', views.update_user_profile, name='update_user_profile'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
]