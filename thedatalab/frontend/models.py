from django.conf import settings
from django.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.template.loader import select_template

import tagulous.models
from tagulous.models import SingleTagField, TagField
from django.urls import reverse
from markdownx.models import MarkdownxField
from mptt.models import MPTTModel, TreeForeignKey

from . import views

class TopicTags(tagulous.models.TagTreeModel):
    def pathslug(self):
        return self.path.replace("/", "-")

    def topic(self):
        return self.topic_set.first()
        
    def get_absolute_url(self):
        return "/topics/%s/"%self.pathslug()

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

class Types(tagulous.models.TagModel):
    class TagMeta:
        # Tag options
        initial = "blog-post, podcast"
        force_lowercase = True

class BaseThing(models.Model):
    title = models.CharField(max_length=200)
    #short_title = models.CharField(max_length=30)
    #description = MarkdownxField()
    #long_text = MarkdownxField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    published_at = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True)

    @classmethod
    def model_name(cls):
        return cls.__name__.lower()
        
    @classmethod
    def plural_name(cls):
        if cls.__name__ in ["Blog", "Software"]:
            return cls.__name__
        return cls.__name__ + 's'

    @classmethod
    def include_name(cls, part):
        """Look up fragments for displaying individual thing.

        If a thing-specific fragment exists in a templates
        subdirectory, return that; otherwise return a default.

        """
        template_name = "_{}.html".format(part)
        print("{}/{}".format(cls.model_name(), template_name),
             "defaults/{}".format(template_name))
        return select_template(
            ["{}/{}".format(cls.model_name(), template_name),
             "defaults/{}".format(template_name)])

    @classmethod
    def index_url_name(cls):
        return cls.model_name() + '_index'

    @classmethod
    def index_url(cls):
        return '/%s/'%cls.plural_name().lower()

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
        return self.title
        #return "{} ({})".format(self.short_title, self.title)
        
    class Meta:
        abstract = True
        ordering = ('-published_at',)


#class Thing(BaseThing):
#    related = models.ManyToManyField('self', blank=True)

class ThingWithTopics(BaseThing):
    class Meta:
        ordering = ['title']

    related = models.ManyToManyField('self', blank=True)
    topics = TagField(blank=True, to=TopicTags, related_name="things")
    
    def get_attachments(self):
        ret = []
        for rel in self.related.all():
            if rel.dataset:
                ret.append(rel)
        return ret

class ExternalThing(models.Model):
    doi = models.CharField(max_length=200, unique=True, blank=True, null=True)
    url = models.URLField(max_length=200, unique=True)

    class Meta:
        abstract = True
        
    def get_url_domain(self):
        return ".".join(self.url.split('//', 1)[-1].split('/')[0].rsplit(".", 2)[-2:])


class Topic(BaseThing):
    topic_tag = SingleTagField(to=TopicTags)

    def is_topic(self):
        return True


class Blog(ThingWithTopics):
    body = MarkdownxField(blank=True)
    type = TagField(blank=False, to=Types, help_text="eg: blog-post, podcast")
    
    #topics = TagField(blank=True, to=TopicTags)
    
    def get_authors(self):
        names = [a.name for a in self.authors.all()]
        return ", ".join(names)
        
    def get_preview(self):
        ret = ""
        
        truncated = False
        
        for bit in self.body.replace('\r', '').split('\n\n'):
            if len(ret)>400:
                truncated = True
                break
            ret += '\n\n' + bit
            
        if truncated:
            ret += '\n\n[Read more...](%s)'%self.get_absolute_url()
            
        return ret
        
    def get_absolute_url(self):
        return '/blog/%d/%s/'%(self.pk, slugify(self.title))
        

class Author(models.Model):
    class Meta:
        ordering = ['name']
    
    name = models.CharField(max_length=50, blank=True)
    slug = models.CharField(max_length=50, blank=True, editable=False)
    institution = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True, null=True)
    url = models.URLField(max_length=200, blank=True)
    topics = TagField(blank=True, to=TopicTags)
    
    def get_absolute_url(self):
        return '/authors/%s/'%self.slug
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Author, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Paper(ThingWithTopics, ExternalThing):
    description = models.CharField(max_length=250, blank=True, help_text="20 words max.")
    abstract = MarkdownxField(blank=True)
    #topics = TagField(blank=True, to=TopicTags)
    
    citation = models.CharField(max_length=2000)

    def get_colour_scheme(self):
        if hasattr(self, 'colour_scheme'):
            return self.colour_scheme
        return self.topics.all().aggregate(colour_scheme=Max('pages__project__colour_scheme'))['colour_scheme']

class Tool(ThingWithTopics, ExternalThing):
    description = models.CharField(max_length=250, blank=True, help_text="20 words max.")

class Software(ThingWithTopics, ExternalThing):
    body = MarkdownxField(blank=True)


class Dataset(ThingWithTopics, ExternalThing):
    description = models.CharField(max_length=250, blank=True, help_text="20 words max.")

class Page(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=100, blank=True)
    url = models.CharField(max_length=100, blank=True, editable=False)
    redirect_to = models.CharField(max_length=250, blank=True)
    
    menu_title = models.CharField(max_length=150, blank=True)
    show_in_home_menu = models.BooleanField(default=False)
    show_in_primary_menu = models.BooleanField(default=False)
    show_in_secondary_menu = models.BooleanField(default=False)
    show_in_footer_menu = models.BooleanField(default=False)

    meta_title = models.CharField(max_length=150, blank=True)
    
    image = models.ImageField(blank=True, null=True)
    overlay_text = models.CharField(max_length=150, blank=True)
    overlay_url = models.URLField(max_length=200, blank=True)
    introduction = MarkdownxField(blank=True)
    
    page_type = models.CharField(max_length=150, blank=True, choices=[['', 'Static page'], ['papers', 'Papers'], ['blog', 'Blog'], ['softwares', 'Software'], ['topic', 'Topic']])
    
    body = MarkdownxField(blank=True, null=True)
    colour_scheme = models.CharField(max_length=150, blank=True, choices=[['', ''], ['green', 'Green'], ['orange', 'Orange'], ['blue', 'Blue'], ['red', 'Red']])

    topics = TagField(blank=True, to=TopicTags, related_name="pages")
    types = TagField(blank=True, to=Types)

    def save(self, *args, **kwargs):
        if self.parent is None:
            self.url = ''
        else:
            self.url = self.parent.url + '/' + self.slug
        
        return super(Page, self).save(*args, **kwargs)

    def __str__(self):
        if not self.parent:
            return self.menu_title or "Home"
        return "[%s] %s"%(self.url, self.menu_title)

class Project(Page):
    pass
    #image = models.ImageField(blank=True, null=True)
    #overlay_text = models.CharField(max_length=150, blank=True)
    #overlay_url = models.URLField(max_length=200, blank=True)
    #introduction = MarkdownxField(blank=True)

class TeamMember(models.Model):
    class Meta:
        ordering = ['ordering']
    
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True, editable=False)
    position = models.CharField(max_length=250, blank=True)
    biography = MarkdownxField(blank=True)
    image = models.ImageField(blank=True, null=True)
    
    website_url = models.CharField(max_length=150, blank=True)
    twitter_handle = models.CharField(max_length=150, blank=True)
    author = models.ForeignKey(Author, blank=True, null=True, on_delete=models.SET_NULL, related_name="team_member")
    
    is_alumni = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    ordering = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(TeamMember, self).save(*args, **kwargs)

class Series(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class SeriesThing(models.Model):
    class Meta:
        ordering = ['ordering']
    
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name="things")
    thing = models.ForeignKey(ThingWithTopics, on_delete=models.CASCADE, related_name="serieses")
    
    ordering = models.IntegerField(default=0)
    
    def get_position(self):
        ids = list(self.series.things.values_list('id', flat=True))

        pos = {
            'index':ids.index(self.id)+1,
            'count':len(ids),
        }
        
        if pos['index']>1:
            pos['prev'] = SeriesThing.objects.get(pk=ids[pos['index']-2]).thing
            
            
            
        if pos['index']<len(ids):
            pos['next'] = SeriesThing.objects.get(pk=ids[pos['index']]).thing
            
        return pos
