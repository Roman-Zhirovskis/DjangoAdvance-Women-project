# from django import template
# from django.db.models import *
# from my_app.models import *
#
#
# register = template.Library()
#
#
# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)
#
#
# @register.inclusion_tag('my_app/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     cats = Category.objects.annotate(total=Count('women')).filter(total__gt=0).order_by(sort)
#
#     # cats = Category.objects.filter().order_by(sort)
#     # if not sort:
#     #     cats = Category.objects.filter()
#     # else:
#     #     cats = Category.objects.order_by(sort)
#
#     return {'cats': cats, 'cat_selected': cat_selected}
