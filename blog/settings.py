from django.conf import settings

#: App to use for comments.
COMMENTS_APP = getattr(settings, 'COMMENTS_APP', None)

#: Set to change the number of blogs per page. Set to None to disable (useful if using your own pagination implementation).
PAGINATION_PER_PAGE = getattr(settings, 'BLOG_PAGINATION_PER_PAGE', None)

#: Optionally set this to limit the author field choices based on this Django Group. Otherwise it defaults to check if user is_staff. Set to a tuple to allow multiple groups.
LIMIT_AUTHOR_CHOICES = getattr(settings, 'BLOG_LIMIT_AUTHOR_CHOICES_GROUP', None)

#: Set to true if limiting authors to multiple groups and want to add is_staff users as well.
LIMIT_AUTHOR_CHOICES_ADMIN = getattr(settings, 'BLOG_LIMIT_AUTHOR_CHOICES_ADMIN', False)

SWAPPING_DETECTED = False
for s in ['BLOG_BLOGINDEXPAGE_MODEL', 'BLOG_BLOGPAGE_MODEL', 'BLOG_BLOGPAGETAG_MODEL', 'BLOG_BLOGCATEGORY_MODEL', 'BLOG_BLOGCATEGORYBLOGPAGE_MODEL', 'BLOG_BLOGTAG_MODEL']:
    if getattr(settings, s, False):
        SWAPPING_DETECTED = True
        break
