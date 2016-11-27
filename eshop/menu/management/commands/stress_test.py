from django.core.management import BaseCommand
from menu.models import Category, Product
from menu.utils import pretty
import time

class Command(BaseCommand):
    help = "Test high load of eshop by adding 10 000 products to DB"

    def handle(self, *args, **options):
        self.stdout.write("Stress testing the Applcation!")
        
        print(u'Test create 10 000 product records and category...')
        start = time.time()
        new_category, created = Category.objects.get_or_create(active=True, name='test_cat')
        for num in range(10000):
            new_product = Product.objects.create(active=True, name=u'test_product-{}'.format(num), price=1.12)
            new_category.products.add(new_product)
        end_1 = time.time()
        print(u'Creating of 10000 new products and adding them to the DB takes ths time in secs: ', end_1 - start)
        
        print(u'Test getting all products from DB for menu view...')
        cats = Category.objects.filter(level=0).filter(active=True)
        final_list = pretty(cats, indent=0, menu_list=[])
        end_2 = time.time()
        print(u'Getting ordered menu structure from DB takes this time in secs: ', end_2 - end_1)

        print(u'Test deleting all test products and category...')
        for product in Product.objects.filter(name__contains='test_product'):
            product.delete()
        new_category.delete()
        end_3 = time.time()
        print(u'Deleting 10 000 products and category from DB takes this time in secs: ', end_3 - end_2)
