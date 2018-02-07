"""
Use the configuration with swappable models by running:

python manage.py --settings=demo.settings_swappable
"""
from .settings import *  # noqa

INSTALLED_APPS += [
    "demo.example_swapped"
]


WAGTAIL_BLOG_SWAPPED_APP = 'example_swapped'

BLOG_BLOGINDEXPAGE_MODEL = "{}.BlogIndex".format(WAGTAIL_BLOG_SWAPPED_APP)
BLOG_BLOGPAGE_MODEL = "{}.BlogPage".format(WAGTAIL_BLOG_SWAPPED_APP)
BLOG_BLOGPAGETAG_MODEL = "{}.BlogPageTag".format(WAGTAIL_BLOG_SWAPPED_APP)
BLOG_BLOGCATEGORY_MODEL = "{}.BlogCategory".format(WAGTAIL_BLOG_SWAPPED_APP)
BLOG_BLOGCATEGORYBLOGPAGE_MODEL = "{}.BlogCategoryBlogPage".format(WAGTAIL_BLOG_SWAPPED_APP)
BLOG_BLOGTAG_MODEL = "{}.BlogTag".format(WAGTAIL_BLOG_SWAPPED_APP)
