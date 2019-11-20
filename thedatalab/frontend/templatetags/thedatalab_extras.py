from django import template
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def show_markdown(text):
    return markdownify(text)

@register.filter
def twitter_url(url):
    if url.startswith("@"):
        return "https://www.twitter.com/" + url[1:]
