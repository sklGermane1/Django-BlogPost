from django.urls import path 
from . import views 
from .views import PostListView
urlpatterns = [
    path("about/",views.about,name="about"),
    path("",PostListView.as_view(),name="posts-home")
]
