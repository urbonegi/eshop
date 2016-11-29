from django.test import TestCase
from menu.models import Category, Product, CategoryHierarchy
from django.core.exceptions import ValidationError
from menu.utils import pretty


class CategoryTestCase(TestCase):
    """Main Application data model tests"""
    
    fixtures = ['test_menu_data.json']

    def setUp(self):
        print(u'Testing Category DB model validations, signals and couters')
        # Assert init state
        products = Product.objects.active()
        cats = Category.objects.active()
        self.assertEqual(len(products), 3)
        self.assertEqual(len(cats), 11)
        
    def test_category_no_self_assign(self):
        """Self assign as a sub category is forbidden by validation"""
        print(u'test no self category assign')
        test_cat = Category.objects.get(name='food')
        with self.assertRaises(ValidationError):
            CategoryHierarchy.objects.create(parent_category=test_cat, child_category=test_cat)

    def test_category_added_once(self):
        """Assign the same sub category to the same parent category is forbidden by validation"""
        print(u'test no multiple same category assign')
        test_cat = Category.objects.get(name='Pigu eshop')
        parent_cat = Category.objects.create(name='parent', active=True)
        CategoryHierarchy.objects.create(parent_category=parent_cat, child_category=test_cat)
        with self.assertRaises(ValidationError):
            CategoryHierarchy.objects.create(parent_category=parent_cat, child_category=test_cat)

    def test_category_no_multiple_parents(self):
        """It is forbidden to have multiple parent categories"""
        print(u'test no multiple parents')
        test_sub_cat = Category.objects.get(name='fruit')
        test_cat = Category.objects.get(name='food')
        self.assertNotEqual(test_sub_cat.child_category.all()[0].parent_category.name, test_cat.name)
        with self.assertRaises(ValidationError):
            CategoryHierarchy.objects.create(parent_category=test_cat, child_category=test_sub_cat)
        self.assertNotIn(test_cat.name, [x.parent_category.name for x in test_sub_cat.child_category.all()])

    def test_save_signal(self):
        """On CategoryHierachy object save as sub_categories levels are recalculated"""
        print(u'on_save_signal test')
        eshop_cat = Category.objects.get(name='Pigu eshop')
        self.assertEqual(Category.objects.get(name='fruit').level, 5)
        self.assertEqual(Category.objects.get(name='food').level, 3)
        self.assertEqual(eshop_cat.level, 0)
        new_cat = Category.objects.create(name='new_one', active=True)
        self.assertEqual(new_cat.level, 0)
        CategoryHierarchy.objects.create(parent_category=new_cat, child_category=eshop_cat)
        self.assertEqual(Category.objects.get(name='fruit').level, 6)
        self.assertEqual(Category.objects.get(name='food').level, 4)
        self.assertEqual(Category.objects.get(name='Pigu eshop').level, 1)

    def test_delete_signal_category(self):
        """On Category delete category levels of children are recalculated"""
        print(u'on_delete_signal test category')
        eshop_cat = Category.objects.get(name='Pigu eshop')
        child_cat = Category.objects.get(name='Pigu.lt')
        self.assertEqual(Category.objects.get(name='fruit').level, 5)
        self.assertEqual(Category.objects.get(name='food').level, 3)
        self.assertEqual(eshop_cat.level, 0)
        self.assertEqual(child_cat.level, 1)
        eshop_cat.delete()
        self.assertEqual(Category.objects.get(name='fruit').level, 4)
        self.assertEqual(Category.objects.get(name='food').level, 2)

    def test_delete_signal_cat_hierarchy(self):
        """On Category Hierarchy object delete levels of children are recalculated"""
        print(u'on_delete signal test hierarchy obj')
        eshop_cat = Category.objects.get(name='Pigu eshop')
        child_cat = Category.objects.get(name='Pigu.lt')
        self.assertEqual(Category.objects.get(name='fruit').level, 5)
        self.assertEqual(Category.objects.get(name='food').level, 3)
        self.assertEqual(eshop_cat.level, 0)
        self.assertEqual(child_cat.level, 1)
        mapping_obj = CategoryHierarchy.objects.get(child_category=child_cat)
        mapping_obj.delete()
        self.assertEqual(Category.objects.get(name='fruit').level, 4)
        self.assertEqual(Category.objects.get(name='food').level, 2)
        self.assertEqual(Category.objects.get(name='Pigu.lt').level, 0)

    def test_product_count_sinals(self):
        """On Product, Category and CategoryHierarchy data delete/save update inner_product_count"""
        

    def test_correct_count_of_products(self):
        """Testing active product count"""
        print(u'test correct product count')
        parent_cat = Category.objects.get(name='Pigu eshop')
        self.assertEqual(parent_cat.level, 0)
        self.assertTrue(parent_cat.active)
        self.assertEqual(parent_cat.active_child_product_count, 2)
        self.assertEqual(parent_cat.all_child_product_count, 4)
        parent_cat.active = False
        parent_cat.save()
        parent_cat = Category.objects.get(name='Pigu eshop')
        self.assertEqual(parent_cat.active_child_product_count, 0)
        self.assertEqual(parent_cat.all_child_product_count, 4)
        parent_cat.active = True
        parent_cat.save()
        tomato = Product.objects.get(name='tomato')
        tomato.active = True
        tomato.save()
        parent_cat = Category.objects.get(name='Pigu eshop')
        self.assertEqual(parent_cat.active_child_product_count, 4)
        self.assertEqual(parent_cat.all_child_product_count, 4)

    def test_correct_final_product_list(self):
        """Testing all product count"""
        print(u'Test menu list for menu tree view')
        product_dict = Product.objects.product_json()
        hierarchy_dict = CategoryHierarchy.objects.mapping_json()
        cat_dict, active_level_0 = Category.objects.category_json()

        final_list = pretty(active_level_0, cat_dict=cat_dict, product_dict=product_dict, hierarchy_dict=hierarchy_dict, indent=0, menu_list=[])
        self.assertEqual((len(final_list)), 13)
        parent_cat = Category.objects.get(name='Pigu eshop')
        parent_cat.active = False
        parent_cat.save()
        cats = Category.objects.active().filter(level=0)
        final_list = pretty(cats, indent=0, menu_list=[])
        self.assertEqual((len(final_list)), 0)

        


