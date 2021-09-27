from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings

from webscraper.tasks import save_store_details


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
        save_store_details.delay(store_type)
        context = {
            "msg": "Backend task assigned for "+store_type
        }
        return render(request, 'webscraper/admin_index.html', context=context)