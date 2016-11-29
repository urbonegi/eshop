from django.core.management import BaseCommand
from menu.models import Category, Product, CategoryHierarchy
from menu.utils import pretty
import time
import random

class Command(BaseCommand):
    help = "Test high load of eshop by adding 10 000 products to DB"

    def handle(self, *args, **options):
        self.stdout.write("Stress testing the Applcation!")
        
        print(u'Test create 5000 categories with 1-5 sub_categories and 1-5 product records per sub_category...')
        start = time.time()
        for i in range(5000):
            top_cat = Category.objects.create(active=True, name='Top Cat {}'.format(i))
            for j in range(random.randint(1, 5)):
                inner_cat = Category.objects.create(active=True, name='Inner Cat {} {}'.format(i, j))
                CategoryHierarchy.objects.create(parent_category=top_cat, child_category=inner_cat)
                for k in range(random.randint(1, 5)):
                    product = Product.objects.create(name=u'product {} {} {}'.format(i, j, k), active=True, price=6)
                    inner_cat.products.add(product)

        end_1 = time.time()
        print(u'Creating of new products/categories and adding them to the DB takes ths time in secs: ', end_1 - start)
        
        print(u'Getting records from DB')   
        product_dict = Product.objects.product_json()
        hierarchy_dict = CategoryHierarchy.objects.mapping_json()
        cat_dict, active_level_0 = Category.objects.category_json()
        final_list = pretty(active_level_0, cat_dict=cat_dict, product_dict=product_dict, hierarchy_dict=hierarchy_dict, indent=0, menu_list=[])
        end_2 = time.time()
        print(u'Getting {} number of records from DB takes this time in secs: {}'.format(len(final_list), end_2 - end_1))
 
        
        print(u'Deleting test data from DB')
        Category.objects.filter(name__contains="Top Cat").delete()
        Category.objects.filter(name__contains="Inner Cat").delete()
        Product.objects.filter(name__contains="product").delete()
        end_3 = time.time()
        print(u'Deleting data took this time in secs: {}'.format(end_3 - end_2))
