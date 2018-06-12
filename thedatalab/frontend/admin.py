from django.contrib import admin

from frontend.models import Topic
from frontend.models import Blog
from frontend.models import Paper
from frontend.models import Tool
from frontend.models import Software
from frontend.models import Dataset
from frontend.models import Author


admin.site.register(Topic)
admin.site.register(Blog)
admin.site.register(Paper)
admin.site.register(Tool)
admin.site.register(Software)
admin.site.register(Dataset)
admin.site.register(Author)
