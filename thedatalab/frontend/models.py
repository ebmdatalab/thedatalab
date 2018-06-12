from django.conf import settings
from django.db import models
from tagulous.models import SingleTagField, TagField
from frontend import views
from django.urls import reverse


class InternalThing(models.Model):
    title = models.CharField(max_length=200)
    navigation_title = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)

    def get_absolute_url(self):
        return reverse('show_' + self.__class__.__name__.lower(), args=[self.pk])

    class Meta:
        abstract = True


class ExternalThing(InternalThing):
    doi = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=200, unique=True)
    class Meta:
        abstract = True


class Topic(InternalThing):
    tags = TagField()


class Blog(InternalThing):
    tags = TagField()


class Author(InternalThing):
    tags = TagField()


class Paper(ExternalThing):
    tags = TagField()


class Tool(ExternalThing):
    tags = TagField()


class Software(ExternalThing):
    tags = TagField()


class Dataset(ExternalThing):
    tags = TagField()
