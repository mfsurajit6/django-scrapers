import logging
import csv
from celery import shared_task
from django.conf import settings

from store.models import Store, StoreType
from webscraper.scrper import BurgerKing, PizzaHut, StarBucks, Verizon


@shared_task(bind=True, queue='scraper_queue')
def save_store_details(self, store_type):
    """
    Fetch the data for requested store type, save the data and create the CSV file
    :param store_type: str, type os store
    :return : str, success message
    """
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
        delete_and_save_store_data.delay(stores, store_type)
        create_csv.delay(stores, store_type)
        return f'Data fetched for {store_type}'
    else:
        return f'No Data fetched for {store_type}'

@shared_task(bind=True, queue='scraper_queue')
def delete_and_save_store_data(self, stores, store_type):
    """
    Delete the existing data for specific store type and insert the new data
    :param stores: dict, store details for specific store type
    :param store_type: str, Store Type
    :return : str, success message
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
            store_latitude=store.get('latitude') if store.get(
                'latitude') else None,
            store_longitude=store.get('longitude') if store.get(
                'longitude') else None,
        )
        store_data.append(s)
    Store.objects.filter(store_type=store_type).delete()
    Store.objects.bulk_create(store_data, len(store_data))
    return f'{store_type} data saved to databse'


@shared_task(bind=True, queue='scraper_queue')
def create_csv(self, stores, store_type):
    """
    Create CSV file for specific store type and store it into media directory
    :param stores: dict, store details for specific store type
    :param store_type: str, Store Type
    :return : str, success message
    """
    media_path = settings.MEDIA_ROOT
    csv_file = f'{media_path}/{store_type}.csv'
    fields_name = ['name', 'address', 'city', 'state',
                   'zip', 'phone', 'latitude', 'longitude', 'store_type']
    try:
        with open(csv_file, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=fields_name)
            writer.writeheader()
            for store in stores.values():
                store['store_type'] = store_type
                writer.writerow(store)
    except IOError:
        logging.critical("File I/O Error")
    return f'{store_type} csv is created and saved'

@shared_task(bind=True)
def scheduled_scraper(self):
    store_types = StoreType.objects.all()
    for store_type in store_types:
        save_store_details(store_type.store_type)
        