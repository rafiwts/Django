from django.urls import re_path
from . import views

app_name = 'blog'

urlpatterns = [
 re_path(r'^$', views.post_list, name='post_list'), # for all
 re_path('^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
      r'(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'), # for all posts
]