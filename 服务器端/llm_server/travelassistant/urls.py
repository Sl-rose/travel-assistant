from django.urls import path

from . import views
# 二级路由：子路由 食堂
urlpatterns = [
    path("ai/", views.assistant, name="assistant"),
    path("upload/", views.uploadfile, name="uploadfile"),
    path("history/", views.history, name="history"),
    path("detail/", views.detail, name="detail"),
    path("deltopic/", views.deltopic, name="deltopic"),
    
]