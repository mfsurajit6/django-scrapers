from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, View):
    """Index page for User"""
    def get(self, request):
        """Render the index page on GET request"""
        return render(request, 'store/index.html')
