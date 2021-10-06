import csv
import logging
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings

from webscraper.scrper import BurgerKing, PizzaHut, StarBucks, Verizon
from store.models import Store, StoreType


class AdminIndexView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Index Page for user with superuser permission"""
    login_url = 'login'

    def test_func(self):
        """Check if the user has super user permission or not """
        return self.request.user.is_superuser

    def get(self, request):
        """Render the index page for users with superuser permission"""
        return render(request, 'webscraper/admin_index.html')

    def post(self, request):
        """Call the scraping scripts, store data to database, create CSV and store it to media file on POST request """
        store_type = request.POST.get('store')
        stores = {}
        if store_type == 'Burger King':
            burgerking = BurgerKing()
            stores = burgerking.get_stores()
        elif store_type == 'Pizza Hut':
            pizzahut = PizzaHut()
            stores = pizzahut.get_stores()
        elif store_type == 'Starbucks':
            starbucks = StarBucks()
            stores = starbucks.get_stores()
        elif store_type == 'Verizon':
            verizon = Verizon()
            stores = verizon.get_stores()

        if len(stores) > 0:
            self.delete_and_save_store_data(stores, store_type)
            self.create_csv(stores, store_type)
            status = 'success'
            msg = f'{store_type} data fetched successfully'
        else:
            status = 'error'
            msg = f'Something Wrong'
        context = {
            "status": status,
            "msg": msg,
        }
        return render(request, 'webscraper/admin_index.html', context=context)

    def delete_and_save_store_data(self, stores, store_type):
        """
        Delete the existing data for specific store type and insert the new data
        :param stores: dict, store details for specific store type
        :param store_type: str, Store Type
        """
        store_data = []
        store_type = StoreType.objects.get(store_type=store_type)
        for store in stores.values():
            s = Store(
                store_type=store_type,
                store_name=store.get('name'),
                store_address=store.get('address'),
                store_city=store.get('city'),
                store_state=store.get('state'),
                store_zip=store.get('zip'),
                store_phone=store.get('phone'),
                store_latitude=store.get('latitude') if store.get('latitude') else None,
                store_longitude=store.get('longitude') if store.get('longitude') else None,
            )
            store_data.append(s)
        Store.objects.filter(store_type=store_type).delete()
        Store.objects.bulk_create(store_data, len(store_data))

    def create_csv(self, stores, store_type):
        """
        Create CSV file for specific store type and store it into media directory
        :param stores: dict, store details for specific store type
        :param store_type: str, Store Type
        """
        media_path = settings.MEDIA_ROOT
        csv_file = f'{media_path}/{store_type}.csv'
        fields_name = ['name', 'address', 'city', 'state', 'zip', 'phone', 'latitude', 'longitude', 'store_type']
        try:
            with open(csv_file, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=fields_name)
                writer.writeheader()
                for store in stores.values():
                    store['store_type'] = store_type
                    writer.writerow(store)
        except IOError:
            logging.critical("File I/O Error")
