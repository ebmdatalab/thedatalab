from django.shortcuts import render

def clean_klasses(klasses_dict, exclude_thing):
    cleaned_klasses = {}
    for klass, things in klasses_dict.items():
        things = [thing for thing in things if thing != exclude_thing]
        if things:
            cleaned_klasses[klass] = things
    return cleaned_klasses



def show_thing(request, slug, thing_type=None):
    from frontend.models import Paper
    from frontend.models import Blog
    from frontend.models import Tool
    from frontend.models import Software
    from frontend.models import Dataset
    from frontend.models import Topic
    thing = thing_type.objects.get(pk=slug)
    thing_name = thing.__class__.__name__.lower()
    index_url_name =  thing_name + '_index'
    thing_plural = thing.__class__.__name__.lower() + "s"
    context = {
        'thing': thing,
        'index_url_name': index_url_name,
        'thing_plural': thing_plural,
        'klasses': {'Papers': Paper,
                    'Blogs': Blog,
                    'Tools': Tool,
                    'Software': Software,
                    'Datasets': Dataset}
    }
    if thing.__class__.__name__ == 'Author':
        klass_filter = {'authors': thing}
    else:
        klass_filter = {'tags__slug__in': [x.slug for x in thing.tags.all()]}
    for var, klass in context['klasses'].items():
        context['klasses'][var] = klass.objects.filter(**klass_filter)
    # drop empty klasses
    context['klasses'] = clean_klasses(context['klasses'], thing)

    # Create links to related topics
    topic_tags = [x for x in thing.tags.all() if '-' in str(x)]
    context['topics'] = Topic.objects.filter(
        tags__slug__in=topic_tags
    )
    return render(request, 'thing.html', context=context)


def thing_index(request, thing_type=None):
    from frontend.models import Paper
    from frontend.models import Blog
    from frontend.models import Tool
    from frontend.models import Software
    from frontend.models import Dataset
    from frontend.models import Topic
    things = thing_type.objects.all()

    context = {
        'things': things,
        'title': "All {}s".format(thing_type.__name__)
    }
    return render(request, 'thing_index.html', context=context)
