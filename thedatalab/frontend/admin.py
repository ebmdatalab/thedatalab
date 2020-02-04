from django.contrib import admin

from . import models

from markdownx.admin import MarkdownxModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

admin.site.register(models.Blog, MarkdownxModelAdmin)
admin.site.register(models.Paper, MarkdownxModelAdmin)
admin.site.register(models.Tool, MarkdownxModelAdmin)
admin.site.register(models.Software, MarkdownxModelAdmin)
admin.site.register(models.Dataset, MarkdownxModelAdmin)

@admin.register(models.Author)
class AuthorAdmin(MarkdownxModelAdmin):
    pass

@admin.register(models.TeamMember)
class TeamMemberAdmin(MarkdownxModelAdmin):
    list_display = ['name', 'position', 'is_alumni']

@admin.register(models.Page)
class PageAdmin(DjangoMpttAdmin, MarkdownxModelAdmin):
	pass

@admin.register(models.Project)
class ProjectAdmin(MarkdownxModelAdmin):
    pass

class SeriesThingInline(admin.TabularInline):
    model = models.SeriesThing
    fields = ['thing', 'ordering']
    extra = 1

@admin.register(models.Series)
class SeriesAdmin(MarkdownxModelAdmin):
    inlines = [
	SeriesThingInline
    ]
    pass

