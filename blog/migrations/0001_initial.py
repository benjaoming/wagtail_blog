# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import django.db.models.deletion
import modelcluster.fields
import modelcluster.tags
import swapper


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('taggit', '0001_initial'),
        ('wagtailimages', '0005_make_filter_spec_unique'),
        swapper.dependency('blog', 'BlogPage'),
        swapper.dependency('blog', 'BlogIndexPage'),
        swapper.dependency('blog', 'BlogCategory'),
        swapper.dependency('blog', 'BlogTag'),
        swapper.dependency('blog', 'BlogPageTag'),
        swapper.dependency('blog', 'BlogCategoryBlogPage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='Category Name')),
                ('slug', models.SlugField(unique=True, max_length=80)),
            ],
            options={
                'ordering': ['name'],
                'swappable': swapper.swappable_setting('blog', 'BlogCategory'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategoryBlogPage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('category', models.ForeignKey(related_name='+', to=swapper.get_model_name('blog', 'BlogCategory'))),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
                'swappable': swapper.swappable_setting('blog', 'BlogCategoryBlogPage'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True)),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('blog', 'BlogIndexPage'),
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, to='wagtailcore.Page', primary_key=True, auto_created=True, parent_link=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
                ('header_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', blank=True)),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('blog', 'BlogPage'),
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='tagged_items', to=swapper.get_model_name('blog', 'BlogPage'))),
                ('tag', models.ForeignKey(related_name='blog_blogpagetag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('blog', 'BlogPageTag'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.tags.ClusterTaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag', blank=True, through=swapper.get_model_name('blog', 'BlogPageTag')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcategoryblogpage',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='categories', to=swapper.get_model_name('blog', 'BlogPage')),
            preserve_default=True,
        ),
    ]
