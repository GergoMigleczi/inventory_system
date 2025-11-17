from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def getattr_dynamic(obj, attr):
    return getattr(obj, attr)

@register.simple_tag
def build_url(builder, row, url_kwargs):
    """
    builder: UrlBuilder
    row: current table row
    url_kwargs: request.resolver_match.kwargs
    """

    resolved = builder.resolve(row, url_kwargs)

    # Old behaviour: only args returned
    if isinstance(resolved, (list, tuple)) and len(resolved) == 1:
        args = resolved
        query = {}
    else:
        args, query = resolved

    url = reverse(builder.url_name, args=args)

    # append ?query if present
    if query:
        from urllib.parse import urlencode
        return f"{url}?{urlencode(query)}"

    return url


