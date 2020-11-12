from django.urls import path 
from . import views 
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    LikeView
    )

urlpatterns = [
    path("about/",views.about,name="about"),
    path("",PostListView.as_view(),name="posts-home"),
    path("post/<int:pk>/",PostDetailView.as_view(),name="post-detail"),
    path("post/new/",PostCreateView.as_view(),name="post-create"),
    path("post/<int:pk>/update",PostUpdateView.as_view(),name="post-update"),
    path("post/<int:pk>/delete",PostDeleteView.as_view(),name="post-delete"),
    path("post/<int:pk>/comment",CommentCreateView.as_view(),name="comment-create"),
    path("like/<int:pk>",LikeView,name="like_post")
]


