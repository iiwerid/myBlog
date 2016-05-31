from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink


class Blogpost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)

    def __unicode__(self):
        return "%s"%self.title

    @permalink
    def get_absolute_url(self):
        #from django.core.urlresolvers import reverse
        #return reverse('view_blog_post', args=[str(self.slug)])
        return ('view_blog_post', None, {'slug':self.slug})
