import os
import django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.conf import settings


class Command(BaseCommand):
    help = '''Given a model name, generate stub templates for displaying it'''

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='+', type=str)

    def handle(self, *args, **options):
        templates = [
            "_{}_header.html",
            "_{}_body.html",
            "_{}_related.html",
            ]
        for model_name in options['models']:
            klass = apps.get_app_config('frontend').get_model(model_name)
            for template in templates:
                default = template.format('default')
                template = template.format(klass.model_name())
                path = os.path.join(
                    settings.PROJECT_ROOT, '..', 'frontend', 'templates', template)
                if os.path.exists(path):
                    raise CommandError("{} already exists!".format(path))
                with open(path, "w") as f:
                    f.write("{{% include '{}' %}}".format(default))
