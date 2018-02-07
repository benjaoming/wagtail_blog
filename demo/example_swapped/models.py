from __future__ import unicode_literals

import swapper
from blog.models.base import (BlogCategoryBase, BlogCategoryBlogPageBase,
                              BlogIndexPageBase, BlogPageBase)
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from wagtail.wagtailsnippets.models import register_snippet

 
class BlogIndex(BlogIndexPageBase):
    pass
 
 
class BlogPage(BlogPageBase):
    pass
 
 
class BlogCategory(BlogCategoryBase):
    pass
 
 
class BlogPageTag(TaggedItemBase):
 
    content_object = ParentalKey(
        swapper.get_model_name('blog', 'BlogPage'), related_name='tagged_items')
 
 
class BlogCategoryBlogPage(BlogCategoryBlogPageBase):
    pass
 
 
@register_snippet
class BlogTag(Tag):
 
    class Meta:
        proxy = True


# from django.db import models
# 
# class BlogIndex(models.Model):
#     pass
# 
# 
# class BlogPage(models.Model):
#     pass
# 
# 
# class BlogCategory(models.Model):
#     pass
# 
# 
# class BlogPageTag(models.Model):
#     pass
# 
# 
# class BlogCategoryBlogPage(models.Model):
#     pass
# 
# 
# @register_snippet
# class BlogTag(Tag):
# 
#     class Meta:
#         proxy = True
