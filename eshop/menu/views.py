from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from menu.models import Category
from menu.utils import pretty


def menu(request):
    template = loader.get_template('index.html')
    cats = Category.objects.active().filter(level=0)
    final_list = pretty(cats, indent=0, menu_list=[])
    context = {
        'menu': u'\n'.join(final_list),
    }
    return HttpResponse(template.render(context, request))
