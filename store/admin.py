from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from store.models import Store

class StoreAdmin(admin.ModelAdmin):
    """ Customized display of Store for Django Admin"""
    list_display = (
        'id', 'store_name', 'store_city', 'store_state', 'store_phone'
    )
    list_display_links = ('store_name', )
    search_fields = ('store_name', 'store_type', )


admin.site.register(Store, StoreAdmin)
