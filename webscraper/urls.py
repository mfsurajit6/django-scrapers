from django.urls import path
from webscraper.views import AdminIndexView


urlpatterns = [
    path('scraper/', AdminIndexView.as_view(), name='admin_index'),
]
