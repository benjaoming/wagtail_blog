# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import swapper


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150226_2305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategoryblogpage',
            options={
                'abstract': False,
                'ordering': ['sort_order'],
                'swappable': swapper.swappable_setting('blog', 'BlogCategoryBlogPage'),
            },
        ),
        migrations.RemoveField(
            model_name='blogcategoryblogpage',
            name='sort_order',
        ),
    ]
