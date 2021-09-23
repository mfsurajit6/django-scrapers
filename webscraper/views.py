from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from webscraper.scrper import BurgerKing, PizzaHut, StarBucks, Verizon
from store.models import Store, StoreType


class AdminIndexView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        return render(request, 'webscraper/admin_index.html')

    def post(self, request):
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
            self.save_store_data(stores, store_type)
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

    def save_store_data(self, stores, store_type):
        store_data = []
        for store in stores.values():
            s = Store(
                store_type=StoreType.objects.get(store_type=store_type),
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

        Store.objects.bulk_create(store_data, len(store_data))

