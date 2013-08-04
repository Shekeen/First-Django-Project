from django.utils import timezone
from django.views import generic
from Blog.models import BlogPost


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'Blog/index.html'
    context_object_name = 'recent_blog_posts'

    def get_queryset(self):
        """ Return 10 most recent blog posts """
        return BlogPost.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:10]


class BlogPostView(generic.DetailView):
    model = BlogPost
    template_name = 'Blog/post.html'
    context_object_name = 'blog_post'

    def get_queryset(self):
        return BlogPost.objects.filter(pub_date__lte=timezone.now())
