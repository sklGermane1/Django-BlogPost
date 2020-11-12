from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post,Comment 
from django.contrib.auth.models import User
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponseRedirect
from  django.urls import reverse_lazy,reverse

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

class PostDetailView(DetailView):
    model = Post 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        
        total_likes = stuff.total_likes()
        liked = False 
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["liked"] = liked
        context["total_likes"] = total_likes 
        return context
    

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

class UserPostListView(ListView):
    model = Post 
    template_name = "posts/user_posts.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-created_at")


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_create.html"


    def form_valid(self,form):
        form.instance.post_id = self.kwargs["pk"]
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    success_url = "/"


def LikeView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    liked = False 
    if post.likes.filter(id= request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:

        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("post-detail",args=[str(pk)]))