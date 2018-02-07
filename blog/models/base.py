import datetime

from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel)
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

import swapper

from .. import settings
from django.contrib.contenttypes.models import ContentType


def get_blog_context(context):
    """ Get context data useful on all blog related pages """
    from . import BlogCategory
    BlogPage = swapper.load_model("blog", "BlogPage")
    context['authors'] = get_user_model().objects.filter(
        owned_pages__live=True,
        owned_pages__content_type__model=ContentType.get_all_objects_for_this_type(BlogPage).model
    ).annotate(Count('owned_pages')).order_by('-owned_pages__count')
    context['all_categories'] = BlogCategory.objects.all()
    context['root_categories'] = BlogCategory.objects.filter(
        parent=None,
    ).prefetch_related(
        'children',
    ).annotate(
        blog_count=Count('blogpage'),
    )
    return context


class BlogIndexPageBase(Page):
    @property
    def blogs(self):
        # Get list of blog pages that are descendants of this page
        BlogPage = swapper.load_module("blog", "BlogPage")
        blogs = BlogPage.objects.descendant_of(self).live()
        blogs = blogs.order_by(
            '-date'
        ).select_related('owner').prefetch_related(
            'tagged_items__tag',
            'categories',
            'categories__category',
        )
        return blogs

    def get_context(self, request, tag=None, category=None, author=None, *args,
                    **kwargs):
        context = super(BlogIndexPageBase, self).get_context(
            request, *args, **kwargs)
        blogs = self.blogs

        from . import BlogCategory
        
        if tag is None:
            tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__slug=tag)
        if category is None:  # Not coming from category_view in views.py
            if request.GET.get('category'):
                category = get_object_or_404(
                    BlogCategory, slug=request.GET.get('category'))
        if category:
            if not request.GET.get('category'):
                category = get_object_or_404(BlogCategory, slug=category)
            blogs = blogs.filter(categories__category__name=category)
        if author:
            if isinstance(author, str) and not author.isdigit():
                blogs = blogs.filter(author__username=author)
            else:
                blogs = blogs.filter(author_id=author)

        # Pagination
        page = request.GET.get('page')
        page_size = 10
        if settings.PAGINATION_PER_PAGE is not None:
            page_size = settings.PAGINATION_PER_PAGE

        if page_size is not None:
            paginator = Paginator(blogs, page_size)  # Show 10 blogs per page
            try:
                blogs = paginator.page(page)
            except PageNotAnInteger:
                blogs = paginator.page(1)
            except EmptyPage:
                blogs = paginator.page(paginator.num_pages)

        context['blogs'] = blogs
        context['category'] = category
        context['tag'] = tag
        context['author'] = author
        context['COMMENTS_APP'] = settings.COMMENTS_APP
        context = get_blog_context(context)

        return context

    class Meta:
        abstract = True
        verbose_name = _('Blog index')
    subpage_types = [swapper.get_model_name("blog", "BlogPage")]


@register_snippet
class BlogCategoryBase(models.Model):
    name = models.CharField(
        max_length=80, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Jazz category, and under that have children categories for Bebop'
            ' and Big Band. Totally optional.')
    )
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        from . import BlogCategory
        if not self.slug:
            slug = slugify(self.name)
            count = BlogCategory.objects.filter(slug=slug).count()
            if count > 0:
                slug = '{}-{}'.format(slug, count)
            self.slug = slug
        return super(BlogCategoryBase, self).save(*args, **kwargs)


@register_snippet
class BlogTagBase(Tag):
    class Meta:
        proxy = True


def limit_author_choices():
    """ Limit choices in blog author field based on config settings """

    if settings.LIMIT_AUTHOR_CHOICES:
        if isinstance(settings.LIMIT_AUTHOR_CHOICES, str):
            limit = Q(groups__name=settings.LIMIT_AUTHOR_CHOICES)
        else:
            limit = Q()
            for s in settings.LIMIT_AUTHOR_CHOICES:
                limit = limit | Q(groups__name=s)
        if settings.LIMIT_AUTHOR_CHOICES_ADMIN:
            limit = limit | Q(is_staff=True)
    else:
        limit = {'is_staff': True}
    return limit


class BlogPageBase(Page):
    body = RichTextField(verbose_name=_('body'), blank=True)
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    date = models.DateField(
        _("Post date"), default=datetime.datetime.today,
        help_text=_("This date may be displayed on the blog post. It is not "
                    "used to schedule posts to go live at a later date.")
    )
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Header image')
    )
    author = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        blank=True, null=True,
        limit_choices_to=limit_author_choices,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]
    blog_categories = models.ManyToManyField(
        swapper.get_model_name('blog', 'BlogCategory'), through='blog.BlogCategoryBlogPage', blank=True)

    settings_panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('go_live_at'),
                FieldPanel('expire_at'),
            ], classname="label-above"),
        ], 'Scheduled publishing', classname="publishing"),
        FieldPanel('date'),
        FieldPanel('author'),
    ]
# 
#     content_panels = [
#         FieldPanel('title', classname="full title"),
#         MultiFieldPanel([
#             FieldPanel('tags'),
#             InlinePanel('categories', label=_("Categories")),
#         ], heading="Tags and Categories"),
#         ImageChooserPanel('header_image'),
#         FieldPanel('body', classname="full"),
#     ]

    def save_revision(self, *args, **kwargs):
        if not self.author:
            self.author = self.owner
        return super(BlogPageBase, self).save_revision(*args, **kwargs)

    def get_absolute_url(self):
        return self.url

    def get_blog_index(self):
        # Find closest ancestor which is a blog index
        IndexType = swapper.load_model("blog", "BlogIndexPage")
        return self.get_ancestors().type(IndexType).last()

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPageBase, self).get_context(request, *args, **kwargs)
        context['blogs'] = self.get_blog_index().blogindexpage.blogs
        context = get_blog_context(context)
        context['COMMENTS_APP'] = settings.COMMENTS_APP
        return context

    class Meta:
        abstract = True
        verbose_name = _('Blog page')
        verbose_name_plural = _('Blog pages')

    parent_page_types = [swapper.get_model_name("blog", "BlogIndexPage")]
