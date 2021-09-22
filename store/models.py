from django.db import models

class Store(models.Model):
    """Store Model"""
    store_type = models.CharField(max_length=50)
    store_id = models.CharField(max_length=50)
    store_name = models.CharField(max_length=200)
    store_address = models.TextField()
    store_city = models.CharField(max_length=50)
    store_state = models.CharField(max_length=50)
    store_zip = models.CharField(max_length=20)
    store_phone = models.CharField(max_length=20)
    store_latitude = models.CharField(max_length=20, default=None)
    store_logitude = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.store_name