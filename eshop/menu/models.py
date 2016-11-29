from django.db import models
from menu.utils import count_all_products, count_categoriy_level, update_cat_level, count_active_products
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Prefetch


class CategoryManager(models.Manager):
    """
    Category object query manager
    """
    def active(self):
        product_query = Product.objects.filter(active=True).only('id')
        cat_query = Category.objects.filter(active=True)
        return self.prefetch_related(Prefetch('sub_categories',
                                              queryset=cat_query),
                                     Prefetch('products',
                                              queryset=product_query, to_attr='active_products')).filter(active=True)

    def all_prefetched(self):
        product_query = Product.objects.filter(active=True).only('id')
        return self.prefetch_related(Prefetch('products',
                                              queryset=product_query, to_attr='active_products'))

    def category_json(self):
        obj = self.all_prefetched()
        data_dict = dict()
        active_level_0 = []
        for cat in obj:
            data_dict[cat.id] = {"name": cat.name, "products": [x.id for x in cat.active_products], "active": cat.active, "level": cat.level, "active_inner_products": cat.active_inner_products}
            if cat.active and cat.level == 0:
                active_level_0.append(cat.id)
        return data_dict, active_level_0


class ProductManager(models.Manager):
    """
    Product object query manager
    """
    def active(self):
        return self.filter(active=True)

    def product_json(self):
        obj = self.filter(active=True).values("id", "name", "price")
        product_data_dict = dict()
        for product in obj:
            product_data_dict[product["id"]] = {"name": product["name"], "price": product["price"]}
        return product_data_dict

class CategoryHierarchyManager(models.Manager):
    """
    Category Hierarchy object query manager
    """
 
    def mapping_json(self):
        obj = self.values("parent_category", "child_category")
        data_dict = dict()
        for hier in obj:
            data_dict.setdefault(hier["parent_category"], []).append(hier["child_category"])
        return data_dict


class Product(models.Model):
    """
    Product class
    """
    name = models.CharField(max_length=100)
    active = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = ProductManager()

    class Meta:
        unique_together = (u'name', u'price')
 
    @property
    def price_display(self):
        return u'\u20AC{}'.format(self.price)

    def __str__(self):
        return u'{0}/{1}'.format(self.name, self.price_display)

    def __unicode__(self):
        return u'{0}/{1}'.format(self.name, self.price_display)
 
 
class Category(models.Model):
    """
    Product Category class
    products and sub_categories m2m fields for menu mappings
    """
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField()
    products = models.ManyToManyField(Product, blank=True)
    sub_categories = models.ManyToManyField('self', symmetrical=False, through='CategoryHierarchy', blank=True, through_fields=('parent_category', 'child_category'), related_name='parent_categories')
    level = models.IntegerField(editable=False, default=0, db_index=True)
    active_inner_products = models.IntegerField(editable=False, default=0)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def active_child_product_count(self):
        if not self.active:
            return 0
        products = count_active_products(list(self.sub_categories.active()), product_number=0)
        return self.products.active().count() + products

    @property
    def all_child_product_count(self):
        products = count_all_products(self.sub_categories.all(), product_number=0)
        return self.products.count() + products


class CategoryHierarchy(models.Model):
    """
    M2M Field through model allow to do validation
    post delete and on save signals
    """
    parent_category = models.ForeignKey(Category, related_name='parent_category')
    child_category = models.ForeignKey(Category, related_name='child_category')

    objects = CategoryHierarchyManager()
 
    def __str__(self):
        return self.child_category.name
 
    def __unicode__(self):
        return self.child_category.name
 
    def clean(self):
        self.validate_self_select()
        self.validate_one_parent()
        self.validate_added_once()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(CategoryHierarchy, self).save(*args, **kwargs)

    def validate_self_select(self):
        """
        Self assign a category as a sub category is forbidden
        """
        try:
            if self._parent_category_cache.name == self._child_category_cache.name:
                raise ValidationError(u'Category and subcategories cannot be the same.')
        except AttributeError:
            pass

    def validate_added_once(self):
        """
        It is forbidden to have same subcategory assigned multiple times
        """
        parent_cat = Category.objects.filter(id=self.parent_category_id)
        if parent_cat and self._child_category_cache.id in [x.id for x in parent_cat[0].sub_categories.all()] and not self.id:
            raise ValidationError(u'Category {0} is already assigned to this category'.format(self._child_category_cache.name))

    def validate_one_parent(self):
        """
        It is forbidden to have multiple parent categories
        """
        parent_cats = Category.objects.get(id=self.child_category_id).parent_categories.all()
        if any([x.id != self._parent_category_cache.id for x in parent_cats]):
            raise ValidationError(u'Category {0} is already assigned to '.format(self._child_category_cache.name) +
                                  u'parent category: {0}'.format(parent_cats[0].name))


def update_child_product_count(obj):
    """
    Funcion to determine and update given obj
    and parent cats inner product count
    """
    Category.objects.filter(id=obj.id).update(active_inner_products=obj.active_child_product_count)
    for parent in obj.parent_categories.all():
        update_child_product_count(parent)


@receiver(post_save, sender=CategoryHierarchy)
@receiver(post_delete, sender=CategoryHierarchy)
def on_manipulate_signal_hierachy(sender, instance, **kwargs):
    update_cat_level(Category.objects.get(id=instance.child_category_id))
    update_child_product_count(Category.objects.get(id=instance.parent_category_id))


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def on_manipulate_signal_product(sender, instance, **kwargs):
    for cat in instance.category_set.all():
        update_child_product_count(cat)


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def on_manipulate_signal_category(sender, instance, **kwargs):
    update_child_product_count(instance)

