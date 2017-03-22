from django.conf import settings

#: App to use for comments.
COMMENTS_APP = getattr(settings, 'COMMENTS_APP', None)

#: Set to change the number of blogs per page. Set to None to disable (useful if using your own pagination implementation).
PAGINATION_PER_PAGE = getattr(settings, 'BLOG_PAGINATION_PER_PAGE', None)

#: Optionally set this to limit the author field choices based on this Django Group. Otherwise it defaults to check if user is_staff. Set to a tuple to allow multiple groups.
LIMIT_AUTHOR_CHOICES = getattr(settings, 'BLOG_LIMIT_AUTHOR_CHOICES_GROUP', None)

#: Set to true if limiting authors to multiple groups and want to add is_staff users as well.
LIMIT_AUTHOR_CHOICES_ADMIN = getattr(settings, 'BLOG_LIMIT_AUTHOR_CHOICES_ADMIN', False)

#: Model path: 'app.ModelName'
MODEL_PAGE = getattr(settings, 'BLOG_BLOGPAGE_MODEL', None)

#: Model path: 'app.ModelName'
MODEL_INDEX = getattr(settings, 'BLOG_BLOGINDEXPAGE_MODEL', None)

#: Model path: 'app.ModelName'
MODEL_CATEGORY = getattr(settings, 'BLOG_BLOGCATEGORY_MODEL', None)

#: Model path: 'app.ModelName'
MODEL_TAG = getattr(settings, 'BLOG_BLOGTAG_MODEL', None)
