import os
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from store.tasks import send_mail
from store.models import Store, StoreType


class IndexView(LoginRequiredMixin, View):
    """Index page for User"""
    login_url = 'login'

    def get(self, request):
        """Render the index page on GET request. Also in pagination get() method will bw called with store type"""
        store_type = request.GET.get('st') if request.GET.get('st') is not None else ""
        if store_type != "":
            context = self.get_pages(request, store_type)
            return render(request, 'store/index.html', context=context)

        return render(request, 'store/index.html')

    def post(self, request):
        """ Display the search result on POST request """
        store_type = request.POST.get('store')
        context = self.get_pages(request, store_type)
        return render(request, 'store/index.html', context=context)

    def get_pages(self, request, store_type):
        """
        Return content for specific page
        :param request: request, request object
        :param store_type: str, store type
        :return: dict, stores and store_type will be returned as context
        """
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


class SendEmail(View):
    """Send Email to registered user with requested data"""

    def post(self, request):
        """ Send email to the current user with requested data"""
        store_type = request.POST.get('store_type')
        media_path = settings.MEDIA_ROOT
        file_path = f'{media_path}/{store_type}.csv'
        if os.path.isfile(file_path):
            email_id = request.user.email
            send_mail.delay(email_id, file_path, store_type)
            context = {
                'status': 'success',
                'msg': 'Mail send to registered email'
            }
        else:
            context = {
                'status': 'error',
                'msg': 'There are some problem. Try again later'
            }
        return render(request, 'store/index.html', context=context)

class FilterView(View):
    """Perform filteration of stores based on name or city or state for a specific type of store"""

    def post(self,request):
        store_type = request.POST.get('store_type')
        search_key = request.POST.get('search_key')
        
        store_type_id = StoreType.objects.get(store_type=store_type)
        stores = Store.objects.filter( Q(store_type=store_type_id)
                                    & (Q(store_name__icontains=search_key) 
                                    | Q(store_address__icontains=search_key) 
                                    | Q(store_city__icontains=search_key) 
                                    | Q(store_state__icontains=search_key)))
        context = {
            'stores': stores,
            'store_type': store_type,
            'search_key': search_key,
        }
        return render(request, 'store/index.html', context=context)