# Generated by Django 2.2.6 on 2021-01-28 14:59

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_auto_20200319_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='software',
            name='description',
        ),
        migrations.AddField(
            model_name='software',
            name='body',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
    ]
