# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
import swapper


from blog import settings as blog_settings


def default_author(apps, schema_editor):
    BlogPage = swapper.load_model('blog', 'BlogPage')
    for blog in BlogPage.objects.all():
        if not blog.author:
            blog.author = blog.owner
            blog.save()


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        swapper.dependency('blog', 'BlogPage'),
        ('blog', '0004_auto_20150427_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogTag',
            fields=[
            ],
            options={
                'proxy': True,
                'swappable': swapper.swappable_setting('blog', 'BlogTag'),
            },
            bases=('taggit.tag',),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='blog_categories',
            field=models.ManyToManyField(to=swapper.get_model_name('blog', 'BlogPage'), blank=True, through=swapper.get_model_name('blog', 'BlogCategoryBlogPage')),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.', null=True, on_delete=models.deletion.CASCADE, related_name='children', to=swapper.get_model_name('blog', 'BlogCategory')),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(default=datetime.datetime.today, help_text='This date may be displayed on the blog post. It is not used to schedule posts to go live at a later date.', verbose_name='Post date'),
        ),
    ]

    if not blog_settings.SWAPPING_DETECTED:
        operations.append(
            migrations.RunPython(default_author, reverse_code=migrations.RunPython.noop),
        )
