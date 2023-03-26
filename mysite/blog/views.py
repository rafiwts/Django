from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all() # we get all published posts
    return render(request, # render - creates a list of posts on the basis of 'posts'
                  'blog/post/list.html', # path
                  {'posts': posts}) # template


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

# Create your views here.
