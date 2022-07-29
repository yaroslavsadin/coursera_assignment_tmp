from django import template


register = template.Library()


@register.filter
def inc(value, incby):
    return int(value) + int(incby)


@register.simple_tag
def division(divident, divisor, to_int=False):
    left = int(divident)
    right = int(divisor)
    res = left / right
    return int(res) if to_int else res
