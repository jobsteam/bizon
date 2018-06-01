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


@register.inclusion_tag('paginator.html', takes_context=True)
def paginator(context, adjacent_pages=2):
    page_obj = context['page_obj']
    paginator = context['paginator']
    page_num = page_obj.number
    total = paginator.num_pages

    startPage = max(page_num - adjacent_pages, 1)
    if startPage <= adjacent_pages:
        startPage = 1
    endPage = page_num + adjacent_pages + 1
    if endPage >= total - 1:
        endPage = total + 1
    page_numbers = [n for n in range(startPage, endPage)
                    if n > 0 and n <= total]
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'results_per_page': paginator.per_page,
        'page': page_num,
        'pages': total,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': total not in page_numbers,
        'queries': context.get('queries'),
    }
