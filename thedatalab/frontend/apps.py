from django.apps import AppConfig

class FrontendConfig(AppConfig):
    name = 'thedatalab.frontend'

    def ready(self):
        from . import signals
