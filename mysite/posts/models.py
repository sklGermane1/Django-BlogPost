from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    likes = models.ManyToManyField(User, related_name="blog_posts")
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank=True,null=True)
   
    created_at = models.DateTimeField(default=timezone.now)



    def __str__(self):
        return f"Comment({self.post.title}, {self.user.username})"