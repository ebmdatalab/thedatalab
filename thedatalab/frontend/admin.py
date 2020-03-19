from django.contrib import admin

from . import models

from markdownx.admin import MarkdownxModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

admin.site.register(models.Tool, MarkdownxModelAdmin)
admin.site.register(models.Software, MarkdownxModelAdmin)
admin.site.register(models.Dataset, MarkdownxModelAdmin)

def get_type_string(obj):
    return str(obj.type)
get_type_string.short_description = 'Type'

def get_topics_string(obj):
    return str(obj.topics)
get_topics_string.short_description = 'Topics'

@admin.register(models.Blog)
class BlogAdmin(MarkdownxModelAdmin):
    list_display = ['__str__', get_type_string, get_topics_string]

@admin.register(models.Paper)
class PaperAdmin(MarkdownxModelAdmin):
    list_display = ['__str__', get_topics_string]

@admin.register(models.Author)
class AuthorAdmin(MarkdownxModelAdmin):
    pass

@admin.register(models.TeamMember)
class TeamMemberAdmin(MarkdownxModelAdmin):
    list_display = ['name', 'position', 'is_alumni']

@admin.register(models.Page)
class PageAdmin(DjangoMpttAdmin, MarkdownxModelAdmin):
	pass

#@admin.register(models.Project)
#class ProjectAdmin(MarkdownxModelAdmin):
#    pass

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

