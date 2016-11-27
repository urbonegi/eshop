from django.contrib import admin
from menu.models import Product, Category, CategoryHierarchy
 
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'active')
 
class CategoryHierarchyInline(admin.StackedInline):
    model = CategoryHierarchy
    fk_name = 'parent_category'
 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    inlines = [CategoryHierarchyInline]

    def child_cat(self, obj):
        return [x.name for x in obj.sub_categories.all()]

    def parent_cat(self, obj):
        return [x.name for x in obj.parent_categories.all()]

    def product_list(self, obj):
        return [x.name for x in obj.products.all()]

    list_display = ('name', 'category_level', 'level', 'all_child_product_count', 'active_child_product_count', 'child_cat', 'parent_cat', 'product_list', 'active')
