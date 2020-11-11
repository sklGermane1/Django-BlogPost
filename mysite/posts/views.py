from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post

from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView
)
# Create your views here.
class PostListView(ListView):
    model = Post 
    context_object_name = "posts"
    template_name = "posts/home.html"
    ordering = ["-created_at"]


@login_required
def about(request):
    context = {}
    return render(request,"posts/about.html",context)