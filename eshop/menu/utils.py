

def count_active_products(cat_list, product_number=0):
    """
    Function to count number of active products
    in active categories for given category list
    """
    for c in cat_list:
        if c.sub_categories.exists():
            product_number = product_number + count_active_products(c.sub_categories.active(),
                                                                    product_number=len(c.active_products))
        else:
            product_number = product_number + len(c.active_products)
    return product_number

def count_all_products(cat_list, product_number=0):
    """
    Function to count all products in given category list
    and all its sub_directories
    """
    for c in cat_list:
        if c.sub_categories.all().exists():
            product_number = product_number + count_all_products(list(c.sub_categories.all()),
                                                                 product_number=c.products.count())
        else:
            product_number = product_number + c.products.count()
    return product_number


def count_categoriy_level(cat, level=0):
    """
    Function determine category level
    0 level category - has no parents
    1 level category has 1 parent etc.
    """
    if not cat.parent_categories.all():
        return level
    for parent in cat.parent_categories.all():
        level = count_categoriy_level(parent, level=(level+1))
    return level

def pretty(cat_list, cat_dict={}, product_dict={}, hierarchy_dict={}, indent=0, menu_list=[]):
    """
    Function create an output list with all active categories and products
    with indentation based on its level and extra info:
    price and product in category count
    """
    for cat_id in cat_list:
        if cat_dict[cat_id]["active"]:
            menu_list.append(u' ' * indent + u'-' + cat_dict[cat_id]["name"] + u'({})'.format(cat_dict[cat_id]["active_inner_products"]))
            for product_id in cat_dict[cat_id]["products"]:
                menu_list.append(u' ' * (indent + 1) + u'-' + product_dict[product_id]["name"] + u'\u20AC' + u'({})'.format(product_dict[product_id]["price"]))
            if hierarchy_dict.get(cat_id):
                menu_list = pretty(hierarchy_dict[cat_id], cat_dict=cat_dict, product_dict=product_dict, hierarchy_dict=hierarchy_dict, indent=indent+1, menu_list=menu_list)
    return menu_list


def update_cat_level(obj):
    """
    Funcion to determine and  update given obj
    category level and its sub_categories levels
    """
    obj.level = count_categoriy_level(obj, level=0)
    obj.save()
    for sub in obj.sub_categories.all():
        update_cat_level(sub)
