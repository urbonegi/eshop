from django.db import models

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def active(self):
        return self.filter(active=True)

