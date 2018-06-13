from django.conf import settings
from django.db import models
from tagulous.models import SingleTagField, TagField
from frontend import views
from django.urls import reverse
from markdownx.models import MarkdownxField


class InternalThing(models.Model):
    title = models.CharField(max_length=200)
    navigation_title = models.CharField(max_length=30)
    description = MarkdownxField()
    image = models.ImageField()
    created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)

    def get_absolute_url(self):
        return reverse('show_' + self.__class__.__name__.lower(), args=[self.pk])

    def __str__(self):
        return "{} ({})".format(self.navigation_title, self.title)

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
    abstract = MarkdownxField()
    citation = models.CharField(max_length=200)


class Tool(ExternalThing):
    tags = TagField()


class Software(ExternalThing):
    tags = TagField()


class Dataset(ExternalThing):
    tags = TagField()
