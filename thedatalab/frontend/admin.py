from django.contrib import admin

from . import models

from markdownx.admin import MarkdownxModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

admin.site.register(models.Blog, MarkdownxModelAdmin)
admin.site.register(models.Paper, MarkdownxModelAdmin)
admin.site.register(models.Tool, MarkdownxModelAdmin)
admin.site.register(models.Software, MarkdownxModelAdmin)
admin.site.register(models.Dataset, MarkdownxModelAdmin)
admin.site.register(models.Author, MarkdownxModelAdmin)

@admin.register(models.TeamMember)
class TeamMemberAdmin(MarkdownxModelAdmin):
	list_display = ['name', 'position', 'is_alumni']

@admin.register(models.Page)
class PageAdmin(DjangoMpttAdmin, MarkdownxModelAdmin):
	pass
