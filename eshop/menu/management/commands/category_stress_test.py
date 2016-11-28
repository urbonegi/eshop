from django.core.management import BaseCommand
from menu.models import Category, Product, CategoryHierarchy
from menu.utils import pretty
import time
import random

class Command(BaseCommand):
    help = "Test high load of eshop by adding 10 000 products to DB"

    def handle(self, *args, **options):
        self.stdout.write("Stress testing the Applcation!")
        
        print(u'Test create 5000 categories with 1 subcategory and 1 to 5 product records per subcategory...')
        start = time.time()
        for i in range(5000):
            top_cat = Category.objects.create(active=True, name='Top Cat {}'.format(i))
            for j in range(random.randint(1, 2)):
                inner_cat = Category.objects.create(active=True, name='Inner Cat {} {}'.format(i, j))
                CategoryHierarchy.objects.create(parent_category=top_cat, child_category=inner_cat)
                for k in range(random.randint(1, 5)):
                    product = Product.objects.create(name=u'product {} {} {}'.format(i, j, k), active=True, price=4)
                    inner_cat.products.add(product)

        end_1 = time.time()
        print(u'Creating of new products/categories and adding them to the DB takes ths time in secs: ', end_1 - start)
        
        print(u'Getting records from DB')   
        cats = Category.objects.active().filter(level=0)
        cats_list = list(cats)
        final_list = pretty(cats_list, indent=0, menu_list=[]) 
        end_2 = time.time()

        print(u'Getting the records takes this time in secs: ', end_2 - end_1)

