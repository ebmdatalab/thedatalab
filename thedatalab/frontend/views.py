from django.shortcuts import render


def show_thing(request, slug, thing_type=None):
    from frontend.models import Paper
    from frontend.models import Blog
    from frontend.models import Tool
    from frontend.models import Software
    from frontend.models import Dataset
    thing = thing_type.objects.get(pk=slug)

    context = {
        'thing': thing,
        'klasses': {'related_papers': Paper,
                    'related_blogs': Blog}
    }

    for var, klass in context['klasses'].items():
        context['klasses'][var] = klass.objects.filter(
            tags__slug__in=[x.slug for x in thing.tags.all()]
        )

    return render(request, 'thing.html', context=context)
