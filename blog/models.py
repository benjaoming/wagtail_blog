"""
Customized models.

Credits for this pattern go to django-blog-zinnia and Fantomas42
"""
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured

from . import settings


def load_model_class(model_path):
    """
    Load by import a class by a string path like:
    'module.models.MyModel'.
    This mechanism allows extension and customization of
    the Entry model class.
    """
    dot = model_path.rindex('.')
    module_name = model_path[:dot]
    class_name = model_path[dot + 1:]
    try:
        _class = getattr(import_module(module_name), class_name)
        return _class
    except (ImportError, AttributeError):
        raise ImproperlyConfigured('%s cannot be imported' % model_path)


class BlogPage(load_model_class(settings.MODEL_PAGE[0])):
    pass


class BlogIndexPage(load_model_class(settings.MODEL_INDEX[0])):
    pass


class BlogTag(load_model_class(settings.MODEL_TAG[0])):
    class Meta:
        proxy = True


class BlogCategory(load_model_class(settings.MODEL_CATEGORY[0])):
    pass


from .default_models import BlogCategoryBlogPage, BlogPageTag  # NOQA @UnusedImport
