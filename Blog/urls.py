from django.conf.urls import patterns, url
from Blog import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>\d+)/$', views.BlogPostView.as_view(), name='blog_post'),
)
