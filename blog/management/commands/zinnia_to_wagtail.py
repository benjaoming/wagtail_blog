from __future__ import absolute_import, unicode_literals, print_function

import os

from blog import models as blog_models
from blog.models import BlogTag, BlogCategory, BlogCategoryBlogPage,\
    BlogPageTag
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from wagtail.wagtailimages.models import Image
from zinnia import models as zinnia_models
from zinnia.managers import PUBLISHED


class Command(BaseCommand):
    """
    Export Zinnia blog posts to wagtail-blog. Can be re-run and will
    overwrite already existing slugs
    
    Does not support comments.
    """

    def add_arguments(self, parser):
        """have to add this to use args in django 1.8"""
        parser.add_argument('blog_index',
                            help="Title of blog index page to attach blogs")

    def handle(self, *args, **options):
        try:
            self.blog_index = blog_models.BlogIndexPage.objects.get(
                title__icontains=options['blog_index'])
        except blog_models.BlogIndexPage.DoesNotExist:
            raise CommandError("Incorrect blog index title - have you created it?")
        self.create_blog_pages()

    def create_category(self, zinnia_category):
        if zinnia_category.parent:
            parent = self.create_category(zinnia_category.parent)
        else:
            parent = None
        new_category = BlogCategory.objects.get_or_create(
            name=zinnia_category.title,
            parent = parent
        )[0]
        new_category.slug = zinnia_category.slug
        new_category.save()
        return new_category

    def create_blog_pages(self):
        """create Blog post entries from wordpress data"""
        for entry in zinnia_models.Entry.objects.all().order_by('-creation_date'):
            slug = entry.slug
            title = entry.title
            body = entry.html_content
            for author in entry.authors.all():
                user = author
            if not entry.authors.all():
                user = get_user_model().objects.all()[0]
            date = entry.creation_date
            
            try:
                new_entry = blog_models.BlogPage.objects.get(slug=slug)
                new_entry.title = title
                new_entry.body = body
                new_entry.owner = user
                new_entry.save()
            except blog_models.BlogPage.DoesNotExist:
                new_entry = self.blog_index.add_child(
                    instance=blog_models.BlogPage(
                        title=title,
                        slug=slug,
                        search_description="description",
                        date=date,
                        body=body,
                        owner=user
                    )
                )

            if not entry.status == PUBLISHED:
                new_entry.unpublish()

            if entry.image:
                title = entry.image_caption
                header_image = Image(title=title)
                header_image.file.save(
                    entry.image.file.name, entry.image)
                header_image.save()
            else:
                header_image = None

            new_entry.header_image = header_image
            new_entry.save()
            
            # Categories
            for zinnia_category in entry.categories.all():
                category = self.create_category(zinnia_category)
                BlogCategoryBlogPage.objects.get_or_create(
                    category=category, page=new_entry)[0]

            # Tags
            for zinnia_tag in entry.tags_list:
                new_tag = BlogTag.objects.get_or_create(name=zinnia_tag)[0]
                BlogPageTag.objects.get_or_create(
                    tag=new_tag,
                    content_object=new_entry
                )
