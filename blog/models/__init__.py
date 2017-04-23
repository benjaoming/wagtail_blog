from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.wagtailadmin.edit_handlers import FieldPanel

import swapper

from . import base


class BlogPage(base.BlogPageBase):
    
    class Meta:
        swappable = swapper.swappable_setting('blog', 'BlogPage')


class BlogIndexPage(base.BlogIndexPageBase):

    class Meta:
        swappable = swapper.swappable_setting('blog', 'BlogIndexPage')


class BlogTag(base.BlogTagBase):

    class Meta:
        proxy = True
        swappable = swapper.swappable_setting('blog', 'BlogTag')


class BlogCategory(base.BlogCategoryBase):

    class Meta:
        swappable = swapper.swappable_setting('blog', 'BlogCategory')
        # Because django.db.migrations doesn't correctly read the Meta class
        # of the parent abstract model. No-op!
        ordering = ['name']


class BlogCategoryBlogPage(base.BlogCategoryBlogPageBase):

    class Meta:
        swappable = swapper.swappable_setting('blog', 'BlogCategoryBlogPage')


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(swapper.get_model_name('blog', 'BlogPage'), related_name='tagged_items')

    class Meta:
        swappable = swapper.swappable_setting('blog', 'BlogPageTag')
