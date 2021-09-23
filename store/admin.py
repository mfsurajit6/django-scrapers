from django.contrib import admin

from store.models import Store, StoreType


class StoreAdmin(admin.ModelAdmin):
    """ Customized display of Store for Django Admin"""
    list_display = (
         'store_name', 'store_city', 'store_state', 'store_phone', 'store_type',
    )
    list_display_links = ('store_name', )
    search_fields = ('store_name', 'store_type', )
    list_filter = ('store_type', )


class StoreTypeAdmin(admin.ModelAdmin):
    """Customized Display of Store Type in Django Admin"""
    list_display = ('id', 'store_type', )
    list_display_links = ('store_type', )


admin.site.register(Store, StoreAdmin)
admin.site.register(StoreType, StoreTypeAdmin)
