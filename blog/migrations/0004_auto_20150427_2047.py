# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import django.db.models.deletion
import swapper


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150323_2116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogindexpage',
            options={
                'swappable': swapper.swappable_setting('blog', 'BlogIndexPage'),
            },
        ),
        migrations.AlterModelOptions(
            name='blogpage',
            options={
                'swappable': swapper.swappable_setting('blog', 'BlogPage'),
            },
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='description',
            field=models.CharField(max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, to=swapper.get_model_name('blog', 'BlogCategory'), help_text='Categories, unlike tags, can have a hierarchy. You might have a Jazz category, and under that have children categories for Bebop and Big Band. Totally optional.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategoryblogpage',
            name='category',
            field=models.ForeignKey(verbose_name='Category', related_name='+', to=swapper.get_model_name('blog', 'BlogCategory')),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name='body'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='header_image',
            field=models.ForeignKey(to='wagtailimages.Image', verbose_name='Header image', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+'),
            preserve_default=True,
        ),
    ]
