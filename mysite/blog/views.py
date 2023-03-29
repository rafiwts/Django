from django.shortcuts import render, get_object_or_404
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


class PostListView(ListView): # this does the same what the function belows - it returns a list of posts
    queryset = Post.published.all()
    context_object_name = 'posts' # list of posts
    paginate_by = 3 # the number of pages
    template_name = 'blog/post/list.html' 


# def post_list(request):
#     object_list = Post.published.all() # we get all published posts
#     paginator = Paginator(object_list, 3) # 3 posts on one side
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1) # if not integer, return the first page
#     except EmptyPage: # if the number is higher than the nubmer of pages, return the last page
#         posts = paginator.page(paginator.num_pages)

#     return render(request, # render - creates a list of posts on the basis of 'posts'
#                   'blog/post/list.html', # path
#                   { 'page': page,
#                     'posts': posts}) # template


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published') # get the post by id
    sent = False
 
    if request.method == 'POST': # an user fills out a formula and sends it -> request.POST
        form = EmailPostForm(request.POST) # the formula has been sent and the new formula is created on the basis of given data
        if form.is_valid(): # validating data
            cd = form.cleaned_data # if data is validated, it is generated to the attribute with fields and values
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} {cd["email"]} encourages you to read {post.title}'
            message = f'Read the post {post.title} on page {post_url}\n\nComment added by {cd["name"]} {cd["comments"]}'
            send_mail(subject, message, 'admin@myblod.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})