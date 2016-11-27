from django.db import models

class ActiveManager(models.Manager):
    """
    Active manager defines active queryset filter
    """
    def active(self):
        return self.filter(active=True)

