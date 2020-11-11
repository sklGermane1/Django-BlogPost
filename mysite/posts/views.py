from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post,Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView
)
# Create your views here.
class PostListView(LoginRequiredMixin,ListView):
    model = Post 
    context_object_name = "posts"
    template_name = "posts/home.html"
    ordering = ["-created_at"]
    paginate_by = 5

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ["title","content"]
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post 
    fields = ["title","content"]

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False 

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False

@login_required
def about(request):
    context = {}
    return render(request,"posts/about.html",context)


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_create.html"


    def form_valid(self,form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    success_url = "/"