from django import template
from markdownx.utils import markdownify

from imagefit.templatetags.imagefit import resize

register = template.Library()

@register.simple_tag
def page_title(page, suffix=""):
    if page in [None, '']:
        return suffix

    if not page.parent_id:
        # Just use whole meta title for homepage
        return page.meta_title

    #if page.meta_title:
    #    return page.meta_title

    bits = list(page.get_ancestors(include_self=True))[::-1][:-1]

    bits = [(p.meta_title or p.menu_title) for p in bits] + [suffix]

    return " | ".join(i for i in bits if i)

@register.simple_tag
def page_colour_scheme(page):
    if page.colour_scheme:
        return page.colour_scheme

    for p in page.get_ancestors():
        if p.colour_scheme:
            return p.colour_scheme

    return ''

@register.filter
def show_markdown(text):
    return markdownify(text)

@register.filter
def twitter_url(url):
    if url.startswith("@"):
        return "https://www.twitter.com/" + url[1:]

@register.filter
def tdl_resize(img, size):
    ret = resize(img, size)
    if ret.startswith("/"):
        return "https://www.thedatalab.org" + ret
    return ret