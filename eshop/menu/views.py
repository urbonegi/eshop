from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from menu.models import Category, Product, CategoryHierarchy
from menu.utils import pretty
from django.core import serializers
import json


def menu(request):
    """
    View creates read only page with
    Product and Category Menu
    """
    template = loader.get_template('index.html')
    product_dict = Product.objects.product_json()
    hierarchy_dict = CategoryHierarchy.objects.mapping_json()
    cat_dict, active_level_0 = Category.objects.category_json()

    final_list = pretty(active_level_0, cat_dict=cat_dict, product_dict=product_dict, hierarchy_dict=hierarchy_dict, indent=0, menu_list=[])

    context = {
        'menu': u'\n'.join(final_list),
    }
    return HttpResponse(template.render(context, request))

def new_menu(request):
    json_data = serializers.serialize("json", Category.objects.all())
    data = json.loads(json_data)
    return HttpResponse(data)
