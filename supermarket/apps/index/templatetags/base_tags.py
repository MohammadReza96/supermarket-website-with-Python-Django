import datetime
from django import template
from apps.products.models import Product
#--------
register = template.Library()
#--------


#------------------------------------------- type 1 return a value
@register.simple_tag
def current_time():
    return datetime.datetime.now()


# {% current_time %}  add this tag in template
#------------------------------------------- type 2 return a html  (like include)
@register.inclusion_tag("link.html", takes_context=True)
def jump_link(context):
    return {
        "product": Product.objects.filter(),  # for example
        "title": context["home_title"],
    }
    
# {% jump_link %}  add this tag in template
