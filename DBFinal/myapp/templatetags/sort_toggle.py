from urllib.parse import urlencode
from django import template


register = template.Library()

@register.simple_tag
def sort_toggle(request, field):
    dict_ = request.GET.copy()
    if field in dict_:
        if dict_[field] == 'asc':
            dict_[field] = 'desc'
        else:
            dict_[field] = 'asc'
    else:
        dict_[field] = 'asc'
    return dict_.urlencode()
