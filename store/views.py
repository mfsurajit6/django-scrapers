from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from store.models import Store, StoreType


class IndexView(LoginRequiredMixin, View):
    """Index page for User"""
    def get(self, request):
        """Render the index page on GET request"""
        store_type = request.GET.get('st') if request.GET.get('st') is not None else ""
        if store_type != "":
            context = self.get_pages(request, store_type)
            return render(request, 'store/index.html', context=context)

        return render(request, 'store/index.html')

    def post(self, request):
        store_type = request.POST.get('store')
        context = self.get_pages(request, store_type)
        return render(request, 'store/index.html', context=context)

    def get_pages(self, request, store_type):
        store_type_id = StoreType.objects.get(store_type=store_type)
        stores = Store.objects.filter(store_type=store_type_id).order_by(
            'store_state', 'store_city'
        )
        paginator = Paginator(stores, 10)
        page = request.GET.get('page')
        paged_stores = paginator.get_page(page)
        context = {
            'stores': paged_stores,
            'store_type': store_type
        }
        return context
