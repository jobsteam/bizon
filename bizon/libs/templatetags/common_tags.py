from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def current_host(context):
    """
    Возвращает имя хоста вместе со схемой.
    """
    request = context['request']
    return '{scheme}://{host}'.format(scheme=request.scheme,
                                      host=request.get_host())
