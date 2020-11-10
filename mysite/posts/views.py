from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    context = {}
    return render(request,"posts/home.html",context) 

@login_required
def about(request):
    context = {}
    return render(request,"posts/about.html",context)