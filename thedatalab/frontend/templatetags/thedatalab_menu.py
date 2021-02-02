from django import template
import json

from ..models import Page

register = template.Library()

@register.inclusion_tag("_top_menu.html", takes_context=True)
def render_menu(context):
    root = Page.objects.filter(url='', level=0).first()
    if not root: return []
    
    def generate_tree(queryset):
        ret = []
        cur = None
        for child in queryset:
            cur = None
            if len(ret) and child.url.startswith(ret[-1]['url']):
                cur = ret[-1]
                while len(cur['children']) and child.url.startswith(cur['children'][-1]['url']):
                    cur = cur['children'][-1]

            (cur['children'] if cur else ret).append({
                #'node':child,
                'title':child.menu_title,
                'url':child.url,
                'colour_scheme':child.colour_scheme,
                'children':[]
            })
        return ret
        
    return {
        'home_menu_items':generate_tree(root.get_descendants(include_self=False).filter(show_in_home_menu=True)),
        'primary_menu_items':generate_tree(root.get_descendants(include_self=False).filter(show_in_primary_menu=True)),
        'secondary_menu_items':generate_tree(root.get_descendants(include_self=False).filter(show_in_secondary_menu=True)),
            }

@register.inclusion_tag("_footer_menu.html", takes_context=True)
def render_footer_menu(context):
    root = Page.objects.filter(url='', level=0).first()
    if not root: return []
    
    #print(root.get_descendants(include_self=True).filter(show_in_footer_menu=True))
    
    return {
        'footer_menu_items':[
            {
                'title':i.menu_title,
                'url':i.url
            } for i in root.get_descendants(include_self=True).filter(show_in_footer_menu=True)
            ]
    }


@register.inclusion_tag("_breadcrumbs.html")
def page_breadcrumbs(page, skip_parent=False):
    if not page or not hasattr(page, 'get_ancestors'): return {}
    
    ret = []

    if skip_parent:
        page = page.parent
    
    for item in page.get_ancestors():
        ret.append({
            'title':item.menu_title,
            'url':item.url
        })
    
    return {'breadcrumb_items':ret}
