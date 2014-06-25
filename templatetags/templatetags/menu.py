from django import template

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page

@register.assignment_tag(takes_context=True)
def get_year(context):
    return context['request'].get_full_path().split('/')[1]

@register.inclusion_tag('generic/navbar.html', takes_context=True)
def top_menu(context, parent, top, calling_page=None):
    if top.isalnum():
        menuitems = parent.get_children().get(slug=top).get_children().filter(
            live=True,
            show_in_menus=True
        )

        return {
            'year': top,
            'calling_page': calling_page,
            'menuitems': menuitems,
            # required by the pageurl tag that we want to use within this template
            'request': context['request'],
        }
    else:
        return None
