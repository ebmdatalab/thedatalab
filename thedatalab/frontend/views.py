from datetime import date
from collections import defaultdict
from django.shortcuts import render

def clean_klasses(klasses_dict, exclude_thing):
    cleaned_klasses = defaultdict(list)
    for klass, things in klasses_dict.items():
        things = [thing for thing in things if thing != exclude_thing]
        if things:
            cleaned_klasses[klass].extend(things)
    return cleaned_klasses



def show_thing(request, slug, thing_type=None):
    from .models import Paper
    from .models import Blog
    from .models import Tool
    from .models import Software
    from .models import Dataset
    from .models import Topic
    from .models import TopicTags

    thing = thing_type.objects.get(pk=slug)
    thing_name = thing.__class__.__name__.lower()
    index_url_name =  thing_name + '_index'
    thing_plural = thing.__class__.__name__.lower() + "s"
    klasses = {'Papers': Paper,
               'Blogs': Blog,
               'Tools': Tool,
               'Software': Software,
               'Datasets': Dataset}
    context = {
        'thing': thing,
        'index_url_name': index_url_name,
        'thing_plural': thing_plural,
        'klasses': {},
        'root_topics': TopicTags.objects.filter(level=1)
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
            context['other_things_of_same_type'] = other_things_of_same_type

        context['tags'] = thing.topics.weight()

    context['related_title'] = "Related resources"
    return render(request, 'thing.html', context=context)


def thing_index(request, thing_type=None):
    from .models import Author
    from .models import Paper
    from .models import Blog
    from .models import Tool
    from .models import Software
    from .models import Dataset
    from .models import Topic
    from .models import TopicTags
    context = {
        'title': "All {}s".format(thing_type.__name__),
        'root_topics': TopicTags.objects.filter(level=1)
    }
    context['topics'] = defaultdict(list)
    # If authors, we just want all of them
    if thing_type == Author:
        context['topics']['Authors'] = Author.objects.all()
    else:
        for topic in TopicTags.objects.all():
            klass_filter = {'topics': topic}
            context['topics'][topic].extend(thing_type.objects.filter(**klass_filter))
            # sort them, most recent first
            context['topics'][topic] = sorted(
                context['topics'][topic],
                key=lambda x: date.today() - (x.published_at or date.today()))
        context['topics'] = clean_klasses(context['topics'], None)
    context['topics'] = dict(context['topics'])
    context['related_title'] = ""
    return render(request, 'thing_index.html', context=context)
