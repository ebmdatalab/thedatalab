from django.contrib import admin

from frontend.models import Topic
from frontend.models import Blog
from frontend.models import Paper
from frontend.models import Tool
from frontend.models import Software
from frontend.models import Dataset
from frontend.models import Author

from markdownx.admin import MarkdownxModelAdmin


admin.site.register(Topic, MarkdownxModelAdmin)
admin.site.register(Blog, MarkdownxModelAdmin)
admin.site.register(Paper, MarkdownxModelAdmin)
admin.site.register(Tool, MarkdownxModelAdmin)
admin.site.register(Software, MarkdownxModelAdmin)
admin.site.register(Dataset, MarkdownxModelAdmin)
admin.site.register(Author, MarkdownxModelAdmin)
