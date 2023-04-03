from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import ListView
from django.contrib.postgres.search import TrigramSimilarity
# from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.views.decorators.http import require_POST

# class PostListView(ListView): # this does the same what the function belows - it returns a list of posts
#     queryset = Post.published.all()
#     context_object_name = 'posts' # list of posts
#     paginate_by = 3 # the number of pages
#     template_name = 'blog/post/list.html' 


def post_list(request, tag_slug=None): # tag is optional
    object_list = Post.published.all() # we get all published posts
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag]) # tags for a given post

    paginator = Paginator(object_list, 3) # 3 posts on one side
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) # if not integer, return the first page
    except EmptyPage: # if the number is higher than the nubmer of pages, return the last page
        posts = paginator.page(paginator.num_pages)

    return render(request, # render - creates a list of posts on the basis of 'posts'
                  'blog/post/list.html', # html path
                  {'page': page,
                   'posts': posts,
                   'tag': tag}) # template


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    comments = post.comments.filter(active=True) # a list of active comments is displayed

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST) # a comment was published
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) # the object is created but not commited to the database, hence False
            new_comment.post = post # the object is assigned to a post 
            new_comment.save() # saving to our table in database
    else:
        comment_form = CommentForm()

    post_tags_id = post.tags.values_list('id', flat=True) # collecting all tags for a given post
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id) # we collect all posts with one of the tag except from the current one
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] # we sort it according to the amount of similar tags and the day of publishing - we return only 4 posts

    return render(request,
                    'blog/post/detail.html',
                    {'post': post,
                     'comments': comments,
                     'comment_form': comment_form,
                     'similar_posts': similar_posts})


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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, 
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    
    comment = None
    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),
                                              ).filter(similarity__gt=0.1).order_by('-similarity')
        
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                  'query': query,
                  'results': results})