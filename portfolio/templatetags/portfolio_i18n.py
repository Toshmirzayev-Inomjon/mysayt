from django import template

from portfolio.ui_i18n import t

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, key):
    request = context.get('request')
    language = context.get('current_language', '')
    return t(key, request=request, language=language)
