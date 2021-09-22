from django.urls import path
from store.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
