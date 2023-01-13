from django import template

register = template.Library()

@register.simple_tag
def inc(val):
    n = val+1
    return n

@register.filter(name="isinstance")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))
