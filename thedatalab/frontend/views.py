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
    thing = thing_type.objects.get(pk=slug)

    context = {
        'thing': thing,
        'klasses': {'Papers': Paper,
                    'Blogs': Blog,
                    'Tools': Tool,
                    'Software': Software,
                    'Dataset': Dataset,
        }
    }

    for var, klass in context['klasses'].items():
        context['klasses'][var] = klass.objects.filter(
            tags__slug__in=[x.slug for x in thing.tags.all()]
        )
    # drop empty klasses
    context['klasses'] = clean_klasses(context['klasses'], thing)
    return render(request, 'thing.html', context=context)
