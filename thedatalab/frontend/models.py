from django.conf import settings
from django.db import models
from django.template.loader import select_template

from tagulous.models import SingleTagField, TagField
from frontend import views
from django.urls import reverse
from markdownx.models import MarkdownxField


class InternalThing(models.Model):
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=30)
    description = MarkdownxField()
    long_text = MarkdownxField(blank=True, null=True)
    image = models.ImageField()
    created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)

    @classmethod
    def model_name(cls):
        return cls.__name__.lower()

    @classmethod
    def include_name(cls, part):
        """Look up fragments for displaying individual thing.

        If a thing-specific fragment exists in a templates
        subdirectory, return that; otherwise return a default.

        """
        template_name = "_{}.html".format(part)
        return select_template(
            ["{}/{}".format(cls.model_name(), template_name),
             "defaults/{}".format(template_name)])

    @classmethod
    def header_include_name(cls):
        return cls.include_name('header')

    @classmethod
    def body_include_name(cls):
        return cls.include_name('body')

    @classmethod
    def related_include_name(cls):
        return cls.include_name('related')

    def get_class(self):
        """For use in templates
        """
        return self.__class__

    def get_absolute_url(self):
        return reverse('show_' + self.__class__.model_name(), args=[self.pk])

    def __str__(self):
        return "{} ({})".format(self.short_title, self.title)

    class Meta:
        abstract = True
        ordering = ('-published_at',)


class ExternalThing(InternalThing):
    doi = models.CharField(max_length=200, unique=True, blank=True, null=True)
    url = models.URLField(max_length=200, unique=True)

    class Meta:
        abstract = True


class Topic(InternalThing):
    tags = TagField(blank=True, null=True)

    def is_topic(self):
        return True


class Blog(InternalThing):
    tags = TagField()

    def show_date(self):
        return True


class Author(InternalThing):
    tags = TagField(blank=True, null=True)

    def is_author(self):
        return True


class Paper(ExternalThing):
    tags = TagField()
    citation = models.CharField(max_length=200)


class Tool(ExternalThing):
    tags = TagField()


class Software(ExternalThing):
    tags = TagField()


class Dataset(ExternalThing):
    tags = TagField()
