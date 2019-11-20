from datetime import date
from collections import defaultdict
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from . import models
from .utils import page_resolve

def clean_klasses(klasses_dict, exclude_thing):
    cleaned_klasses = defaultdict(list)
    for klass, things in klasses_dict.items():
        things = [thing for thing in things if thing != exclude_thing]
        if things:
            cleaned_klasses[klass].extend(things)
    return cleaned_klasses



def show_thing(request, slug, thing_type=None):
    thing = thing_type.objects.get(pk=slug)
    thing_name = thing.__class__.__name__.lower()
    index_url_name =  thing_name + '_index'
    thing_plural = thing.__class__.__name__.lower() + "s"
    klasses = {'Papers': models.Paper,
               'Blogs': models.Blog,
               'Tools': models.Tool,
               'Software': models.Software,
               'Datasets': models.Dataset}
    context = {
        'thing': thing,
        'index_url_name': index_url_name,
        'thing_plural': thing_plural,
        'klasses': {},
        'root_topics': models.TopicTags.objects.filter(level=1)
    }
    if thing.__class__.__name__ == 'Author':
        klass_filter = {'authors': thing}
    elif thing.__class__.__name__ == 'Topic':
        klass_filter = {'topics': thing.topic_tag}
    else:
        klass_filter = {'topics__in': [x for x in thing.topics.all()]}
    for var, klass in klasses.items():
        context['klasses'][var] = klass.objects.filter(**klass_filter)
    # drop empty klasses
    context['klasses'] = dict(clean_klasses(context['klasses'], thing))

    # Create links to related topics
    if thing.__class__.__name__ != 'Topic':
        context['topics'] = defaultdict(list)
        for topic in thing.topics.all():
            for var, klass in klasses.items():
                klass_filter = {'topics': topic}
                context['topics'][topic].extend(klass.objects.filter(**klass_filter))
            # sort them, most recent first
            context['topics'][topic] = sorted(
                context['topics'][topic],
                key=lambda x: date.today() - (x.published_at or date.today()))[:3]
        context['topics'] = clean_klasses(context['topics'], thing)
        context['topics'] = dict(context['topics'])
        other_things_of_same_type = thing_type.objects.exclude(pk=slug)
        if other_things_of_same_type.count():
            context['other_things_of_same_type'] = list(other_things_of_same_type)*10

        context['tags'] = thing.topics.weight()

    context['related_title'] = "Related resources"
    return render(request, 'thing.html', context=context)

@page_resolve(strict=False)
def thing_index(request, thing_type=None):
    context = {
        'title': "All {}s".format(thing_type.__name__),
        'root_topics': models.TopicTags.objects.filter(level=1)
    }
    context['topics'] = defaultdict(list)
    # If authors, we just want all of them
    if thing_type == models.Author:
        context['topics']['Authors'] = models.Author.objects.all()
    else:
        for topic in models.TopicTags.objects.all():
            klass_filter = {'topics': topic}
            context['topics'][topic].extend(thing_type.objects.filter(**klass_filter))
            # sort them, most recent first
            context['topics'][topic] = sorted(
                context['topics'][topic],
                key=lambda x: date.today() - (x.published_at or date.today()))
        context['topics'] = clean_klasses(context['topics'], None)
    context['topics'] = dict(context['topics'])
    context['related_title'] = ""
    
    context['spotlight_items'] = models.Paper.objects.all()
    
    return render(request, 'thing_index.html', context=context)

@page_resolve(strict=True)
def home_view(request):
    return render(request, "home.html", {})

@page_resolve(strict=True)
def page_index(request, path):
    return render(request, "page.html", {})

@page_resolve(strict=True)
def team_index(request):
	team_members = models.TeamMember.objects.filter(visible=True, is_alumni=False)
	
	return render(request, "team.html", {'team_members':team_members})

@page_resolve(strict=False)
def author_view(request, slug):
    author = get_object_or_404(models.Author.objects, slug=slug)
    team_member = author.team_member.first()
    papers = models.Paper.objects.filter(authors=author)
    return render(request, "author.html", {'author':author, 'team_member':team_member, 'papers':papers})
    
@page_resolve(strict=True)
def blog_index(request):
	posts = models.Blog.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')
	
	return render(request, "blog.html", {'blog_posts':posts})

@page_resolve(strict=False)
def blog_post_view(request, year, month, pk, slug):
    print(year, month)
    post = get_object_or_404(models.Blog.objects, published_at__year=year, published_at__month=month, pk=pk)
    return render(request, "thing.html", {'thing':post})

@page_resolve(strict=True)
def project_view(request, slug):
    blog_posts = models.Blog.objects.filter(published_at__lte=timezone.now()).order_by('-published_at')[:4]
    
    papers = models.Paper.objects.all()[:4]
    project = request.page.project
    
    return render(request, "project.html", {'blog_posts':blog_posts, 'papers':papers, 'project':project})
