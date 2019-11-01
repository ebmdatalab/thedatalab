from django import template
import json

from ..models import Page

register = template.Library()


@register.inclusion_tag("_top_menu.html", takes_context=True)
def render_menu(context):
    root = Page.objects.filter(url='', level=0).first()
    if not root: return []
    
    ret = []
    cur = None
    
    for child in root.get_descendants(include_self=False).filter(show_in_menu=True):
        cur = None
        if len(ret) and child.url.startswith(ret[-1]['url']):
            cur = ret[-1]
            while len(cur['children']) and child.url.startswith(cur['children'][-1]['url']):
                cur = cur['children'][-1]

        (cur['children'] if cur else ret).append({
            #'node':child,
            'title':child.menu_title,
            'url':child.url,
            'children':[]
        })
    
    return {'menu_items':ret}

@register.inclusion_tag("_breadcrumbs.html")
def page_breadcrumbs(page):
    if not page or not hasattr(page, 'get_ancestors'): return {}
    
    ret = []
    
    for item in page.get_ancestors():
        ret.append({
            'title':item.menu_title,
            'url':item.url
        })
    
    return {'breadcrumb_items':ret}
