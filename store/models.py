import datetime

from django.db import models


class StoreType(models.Model):
    """Store Type Model"""
    store_type = models.CharField(max_length=50)

    def __str__(self):
        return self.store_type

    class Meta:
        db_table = 'store_type'
        verbose_name = 'Store Type'
        verbose_name_plural = 'Store Types'


class Store(models.Model):
    """Store Model"""
    store_type = models.ForeignKey(StoreType, on_delete=models.CASCADE, default=-1)
    store_name = models.CharField(max_length=200)
    store_address = models.TextField(null=True)
    store_city = models.CharField(max_length=50, null=True)
    store_state = models.CharField(max_length=50, null=True)
    store_zip = models.CharField(max_length=20, null=True)
    store_phone = models.CharField(max_length=20, null=True)
    store_latitude = models.CharField(max_length=20, null=True)
    store_longitude = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = 'store'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
