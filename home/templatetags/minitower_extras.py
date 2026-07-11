from django import template

register = template.Library()

UP_VALUES = {"connected", "up", "active"}


@register.filter
def status_badge_class(value):
    if str(value).strip().lower() in UP_VALUES:
        return "status-badge--up"
    return "status-badge--down"
