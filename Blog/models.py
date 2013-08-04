import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('Publish date')

    def __str__(self):
        return self.title

    def was_recently_published(self):
        now = timezone.now()
        return now > self.pub_date >= now - datetime.timedelta(days=2)

    was_recently_published.admin_order_field = 'pub_date'
    was_recently_published.boolean = True
    was_recently_published.short_description = 'Published recently?'

    def text_snippet(self):
        return self.text.split('\r\n\r\n', 1)[0].strip()

    text_snippet.short_description = 'Text cut'
