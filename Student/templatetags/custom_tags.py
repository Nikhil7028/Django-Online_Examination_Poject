from django import template

register = template.Library()

# List of colors
cscolor = ['#ff0000', '#3cb371', '#0000ff', '#ffa500', '#ee82ee', '#6a5acd', '#0100ff']

@register.simple_tag
def get_color(counter):
    return cscolor[counter % len(cscolor)]
