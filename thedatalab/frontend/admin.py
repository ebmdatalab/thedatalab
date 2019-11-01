from django.contrib import admin

from .models import Topic
from .models import Blog
from .models import Paper
from .models import Tool
from .models import Software
from .models import Dataset
from .models import Author
from .models import Page
from .models import TeamMember

from markdownx.admin import MarkdownxModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

admin.site.register(Topic, MarkdownxModelAdmin)
admin.site.register(Blog, MarkdownxModelAdmin)
admin.site.register(Paper, MarkdownxModelAdmin)
admin.site.register(Tool, MarkdownxModelAdmin)
admin.site.register(Software, MarkdownxModelAdmin)
admin.site.register(Dataset, MarkdownxModelAdmin)
admin.site.register(Author, MarkdownxModelAdmin)

@admin.register(TeamMember)
class TeamMemberAdmin(MarkdownxModelAdmin):
	list_display = ['name', 'position', 'is_alumni']

@admin.register(Page)
class PageAdmin(DjangoMpttAdmin, MarkdownxModelAdmin):
	pass
