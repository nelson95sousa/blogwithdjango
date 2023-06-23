from django import template

register = template.Library()



# def cutcutcut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

# register.filter('cutcutcut', cutcutcut )

@register.filter
def comments_not_approved(things):
    return things.filter(approved_comment =False)