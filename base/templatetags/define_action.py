from django import template
register = template.Library()

@register.simple_tag
def add(a, b):
    return a+b

@register.simple_tag
def percentage(a, b):
 	return round(a/(a+b)*100) 