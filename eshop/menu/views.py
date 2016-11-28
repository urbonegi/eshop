from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from menu.models import Category
from menu.utils import pretty
from django.core import serializers
import json


def menu(request):
    """
    View creates read only page with
    Product and Category Menu
    """
    template = loader.get_template('index.html')
    cats = Category.objects.active().filter(level=0)
    cat_list = list(cats)
    final_list = pretty(cat_list, indent=0, menu_list=[])
    context = {
        'menu': u'\n'.join(final_list),
    }
    return HttpResponse(template.render(context, request))

def new_menu(request):
    json_data = serializers.serialize("json", Category.objects.all())
    data = json.loads(json_data)
    return HttpResponse(data)
