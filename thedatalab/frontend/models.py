from django.conf import settings
from django.db import models
from django.template.loader import select_template

import tagulous.models
from tagulous.models import SingleTagField, TagField
from django.urls import reverse
from markdownx.models import MarkdownxField

from . import views

class TopicTags(tagulous.models.TagTreeModel):
    def pathslug(self):
        return self.path.replace("/", "-")

    def topic(self):
        return self.topic_set.first()
        
    def get_absolute_url(self):
        return "asdf"

    class TagMeta:
        # Tag options
        force_lowercase = False
        space_delimiter = False
        # Run `python manage.py initial_tags` if you change:
        initial = ["Health/OpenPrescribing",
                   "Health/Variation",
                   "Health/Changing Behaviour",
                   "Health/RCTs",
                   "Health/Data Science",
                   "Health/Research",
                   "Health/Policy",
                   "Science/Trial Reporting",
                   "Science/TrialsTrackers",
                   "Science/Retractions",
                   "Science/Conflicts of Interest",
                   "Science/Policy",
                   "Science/RCTs"]


class BaseThing(models.Model):
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=30)
    description = MarkdownxField()
    long_text = MarkdownxField(blank=True, null=True)
    image = models.ImageField(default='default.png')
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
    def index_url_name(cls):
        return cls.model_name() + '_index'

    @classmethod
    def header_include_name(cls):
        return cls.include_name('header')

    @classmethod
    def body_include_name(cls):
        return cls.include_name('body')

    @classmethod
    def related_include_name(cls):
        return cls.include_name('related')

    @classmethod
    def related_item_include_name(cls):
        return cls.include_name('related_item')

    def long_text_has_images(self):
        return self.long_text and "![" in self.long_text

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


class ThingWithTopics(BaseThing):
    topics = TagField(blank=True, null=True, to=TopicTags)


class ExternalThing(ThingWithTopics):
    doi = models.CharField(max_length=200, unique=True, blank=True, null=True)
    url = models.URLField(max_length=200, unique=True)

    class Meta:
        abstract = True


class Topic(BaseThing):
    topic_tag = SingleTagField(to=TopicTags)

    def is_topic(self):
        return True


class Blog(ThingWithTopics):
    def show_date(self):
        return True


class Author(ThingWithTopics):
    def is_author(self):
        return True


class Paper(ExternalThing):
    citation = models.CharField(max_length=200)


class Tool(ExternalThing):
    pass


class Software(ExternalThing):
    pass


class Dataset(ExternalThing):
    pass
